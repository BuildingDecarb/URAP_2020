import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from calendar import monthrange
'''
Converts date to a range of 24 indices in the dataframe
'''
def date_to_range(date):
    day_of_year = date.timetuple().tm_yday
    return (day_of_year * 24, (day_of_year + 1) * 24)

'''
Yields a python range iterator for dates that makes it easier to go through dates
'''
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
# pricing scheme has a flat rate,
# tiers is a list of two-tuples: (monthly threshold: price above that threshold)
# tou is a list of peak rate, peak begin time, peak end time, off-peak rate
class Scheme:
    def __init__(self, scheme, flat_rate=None, tiers=None, tou=None):
        self.scheme = scheme
        self.flat_rate = flat_rate
        self.tiers = tiers
        self.tou = tou
        self.list_of_price = [15, 0.22376, 0.28159, 0.49334]

    def cost(self, data, climate_zone, begin_date, end_date):
        total = 0
        if self.scheme == 'flat_rate':
            for d in daterange(begin_date, end_date):
                for idx in range(date_to_range(d)[0], date_to_range(d)[1]):
                    #print(idx, data.iloc[idx, climate_zone])
                    total += self.flat_rate * data.iloc[idx, climate_zone]
            return total
        elif self.scheme == 'tiered':
            baseline = self.list_of_price[0]
            tier1 = self.list_of_price[1]
            tier2 = self.list_of_price[2]
            tier3 = self.list_of_price[3]
            begin_index = date_to_range(begin_date)[0]
            end_index = date_to_range(end_date)[1]
            total_energe_use = 0
            for i in range(begin_index, end_index):
                total_energe_use += data.loc[i].iloc[climate_zone]
            total_cost = 0
            if total_energe_use <= baseline:
                total_cost = total_energe_use * tier1
            elif total_energe_use > baseline and total_energe_use <= 4 * baseline:
                total_cost = baseline * tier1 + (total_energe_use - baseline) * tier2
            else:
                total_cost = baseline * tier1 + 3 * baseline * tier2 + (total_energe_use - 4 * baseline) * tier3
            return total_cost
        elif self.scheme == 'tou':
            speak = self.list_of_price[0]
            soffpeak = self.list_of_price[1]
            wpeak = self.list_of_price[2]
            woffpeak = self.list_of_price[3]
            #return price_func('tou').cost(data, climate_zone, begin_date, end_date)

class price_func:
    def __init__(self, scheme, list_of_price=None):
        self.scheme = scheme
        self.list_of_price = list_of_price
        if scheme == 'tiered':
            self.list_of_price = [15, 0.22376, 0.28159, 0.49334]
        elif scheme == 'tou':
            self.list_of_price = [0.25354, 0.20657, 0.18022, 0.17133]
        print(self.list_of_price)
    
    def cost(self, data, climate_zone, begin_data, end_data):
        if self.scheme == 'tiered':
            baseline = self.list_of_price[0]
            tier1 = self.list_of_price[1]
            tier2 = self.list_of_price[2]
            tier3 = self.list_of_price[3]
            begin_index = date_to_range(begin_date)[0]
            end_index = date_to_range(end_date)[1]
            total_energe_use = 0
            for i in range(begin_index, end_index):
                print(i)
                total_energe_use += data.loc[i].iloc[climate_zone]
            total_cost = 0
            if total_energe_use <= baseline:
                total_cost = total_energe_use * tier1
            elif total_energe_use > baseline and total_energe_use <= 4 * baseline:
                total_cost = baseline * tier1 + (total_energe_use - baseline) * tier2
            else:
                total_cost = baseline * tier1 + 3 * baseline * tier2 + (total_energe_use - 4 * baseline) * tier3
            return total_cost
        elif self.scheme == 'tou':
            speak = self.list_of_price[0]
            soffpeak = self.list_of_price[1]
            wpeak = self.list_of_price[2]
            woffpeak = self.list_of_price[3]
            
