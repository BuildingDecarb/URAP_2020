import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from calendar import monthrange
from PricingScheme import *

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
            total += data.loc[idx].iloc[climate_zone]
    return total

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
june = energy_usage(sh_data, 6, 9)
jan = energy_usage(sh_data, 1, 9)
#print(june, jan)
c = cost(wh_data, date(1, 1, 1), date(1, 3, 1), 2, Scheme(scheme='tou'))
print(c)
