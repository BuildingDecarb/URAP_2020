# This will:
# 1. Read LoadHourlyProfileData/HP_SH and HP_WH
# 2. Store that data in a dataframe
# 3. 
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from calendar import monthrange
from PricingScheme import *
# TODO: figure out how to import PricingScheme class

wh_data, sh_data = None, None
def process_data():
    global wh_data, sh_data
    sh_data = pd.read_csv("LoadHourlyProfileData/HP_SH_HourlyProfiles.csv")
    wh_data = pd.read_csv("LoadHourlyProfileData/HP_WH_HourlyProfiles.csv")

def energy_usage(data, month, climate_zone):
    total = 0
    days_in_month = monthrange(1, month)[1]
    for d in range(1, days_in_month + 1):
        day = date(1, month, d)
        r = date_to_range(day)
        for idx in range(r[0], r[1]):
            print(idx)
            total += data.loc[idx].iloc[climate_zone]
    return total

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

# begin_date/end_date: use python datetime.date class
# pricing scheme will have a flat_rate, 
# tiers is a list of two-tuples: (threshold: price above that threshold)
# tou is a list of 3-tuples: (begin_time, end_time, rate)

'''
Calculates the cost of energe usage per month
'''
def cost(data, begin_date, end_date, climate_zone, pricing_scheme):
    # Take the appropriate column and data from climate_zone
    # Create data_climate_zone
    # PricingScheme.py
    return pricing_scheme.cost(data, climate_zone, begin_date, end_date)

process_data()
eu = energy_usage(wh_data, 6, 8)
eu_2 = energy_usage(sh_data, 3, 15)
c = cost(wh_data, date(1, 1, 1), date(1, 3, 1), 5, PricingScheme(scheme='flat_rate'))
print(eu, eu_2)
print(c)
