import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from calendar import monthrange
'''
Converts date to a range of 24 indices in the dataframe
'''
def date_to_range(date):
    day_of_year = date.timetuple().tm_yday - 1
    return (day_of_year * 24, (day_of_year + 1) * 24)

'''
Yields a python range iterator for dates that makes it easier to go through dates
'''
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def season(d):
    if d.month >= 5 and d.month < 9:
        return 'summer'
    return 'winter'

def energy_usage(data, month, climate_zone):
    total = 0
    days_in_month = monthrange(1, month)[1]
    for d in range(1, days_in_month + 1):
        day = date(1, month, d)
        r = date_to_range(day)
        for idx in range(r[0], r[1]):
            total += data.loc[idx].iloc[climate_zone]
    return total
# pricing scheme has a flat rate,
# tiers is a list of two-tuples: (monthly threshold: price above that threshold)
# tou is a list of peak rate, peak begin time, peak end time, off-peak rate
class Scheme:
    def __init__(self, scheme, flat_rate=None, tiers=None, tou=None):
        self.scheme = scheme
        self.flat_rate = flat_rate
        self.tiers = [15, 0.22376, 0.28159, 0.49334]
        self.tou = [0.25354, 0.20657, 0.18022, 0.17133]

    def cost(self, data, climate_zone, begin_date, end_date, div=1):
        total = 0
        if self.scheme == 'flat_rate':
            for d in daterange(begin_date, end_date):
                for idx in range(date_to_range(d)[0], date_to_range(d)[1]):
                    total += self.flat_rate * data.iloc[idx, climate_zone]
            return total
        elif self.scheme == 'tiered':
            baseline = self.tiers[0]
            tier1 = self.tiers[1]
            tier2 = self.tiers[2]
            tier3 = self.tiers[3]
            
            total_cost = 0
            for d in daterange(begin_date, end_date):
                total_energe_use = 0
                for idx in range(date_to_range(d)[0], date_to_range(d)[1]):
                    total_energe_use += data.iloc[idx, climate_zone]
                total_energe_use /= div
                if total_energe_use <= baseline:
                    total_cost += total_energe_use * tier1
                elif total_energe_use > baseline and total_energe_use <= 4 * baseline:
                    total_cost += baseline * tier1 + (total_energe_use - baseline) * tier2
                else:
                    total_cost += baseline * tier1 + 3 * baseline * tier2 + (total_energe_use - 4 * baseline) * tier3
            return total_cost
        elif self.scheme == 'tou':
            speak = self.tou[0]
            soffpeak = self.tou[1]
            wpeak = self.tou[2]
            woffpeak = self.tou[3]
            speaksum, soffpeaksum, wpeaksum, woffpeaksum = 0, 0, 0, 0
            for d in daterange(begin_date, end_date):
                idx = date_to_range(d)[0]
                if season(d) == "summer":
                    if d.weekday() < 5: # Is a weekday
                        speaksum = speaksum + sum(data.iloc[idx+14:idx+19,climate_zone])
                        soffpeaksum = soffpeaksum + sum(data.iloc[idx:idx+14,climate_zone]) + sum(data.iloc[idx+19:idx+24,climate_zone])
                    else:
                        soffpeaksum = soffpeaksum + sum(data.iloc[idx:idx+24,climate_zone])
                else:
                    if d.weekday() < 5:
                        wpeaksum = wpeaksum + sum(data.iloc[idx+14:idx+19,climate_zone])
                        woffpeaksum = woffpeaksum + sum(data.iloc[idx:idx+14,climate_zone]) + sum(data.iloc[idx+19:idx+24,climate_zone])
                    else:
                        woffpeaksum = woffpeaksum + sum(data.iloc[idx:idx+24,climate_zone])
            return speaksum * speak + soffpeaksum * soffpeak + wpeaksum * wpeak + woffpeaksum * woffpeak
