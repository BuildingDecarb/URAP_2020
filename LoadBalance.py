import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange

ER_WH_Raw = pd.read_csv("LoadHourlyProfileData/ER_WH_HourlyProfiles.csv", usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
HP_WH_Raw = pd.read_csv("LoadHourlyProfileData/HP_WH_HourlyProfiles.csv", usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
HP_SH_Raw = pd.read_csv("LoadHourlyProfileData/HP_SH_HourlyProfiles.csv", usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

# helper function: finds number of hours in a month
def hours_in_month(month, year):
    return monthrange(year, month)[1] * 24


# helper function: finds the lower/upper bound hour in a month. Eg. returns (0, 743) for January
def hour_bounds_by_month(month, year):
    lower_bound = 0
    for i in range(1, month):
        lower_bound += hours_in_month(i, year)
    upper_bound = lower_bound + hours_in_month(month, year) - 1
    return (lower_bound, upper_bound)


# See LoadBalanceGraphing.ipynb for graphs

# find average ER_WH per hour for a given month, year, and climate zone
def average_ER_WH(month, year, climate):  # pass in month and climate as integers
    assert climate >= 1 and climate <= 16
    assert month >= 1 and month <= 24
    
    first_hour_of_month = hour_bounds_by_month(month, year)[0]
    last_hour_of_month = hour_bounds_by_month(month, year)[1]
    climate_ER_WH = ER_WH_Raw.loc[first_hour_of_month:last_hour_of_month, str(climate)].to_frame()
    
    average_loads = np.zeros(24)
    hour_count = 0
    for i in climate_ER_WH.values:
        if hour_count > 23:
            hour_count = 0
        
        average_loads[hour_count] += i[0]
        hour_count += 1
            
    num_days_in_month = ((last_hour_of_month+1)-first_hour_of_month) / 24
    return np.divide(average_loads, num_days_in_month)


# find average HP_WH per hour for a given month, year, and climate zone
def average_HP_WH(month, year, climate):  # pass in month and climate as integers
    assert climate >= 1 and climate <= 16
    assert month >= 1 and month <= 24
    
    first_hour_of_month = hour_bounds_by_month(month, year)[0]
    last_hour_of_month = hour_bounds_by_month(month, year)[1]
    climate_HP_WH = HP_WH_Raw.loc[first_hour_of_month:last_hour_of_month, str(climate)].to_frame()
    
    average_loads = np.zeros(24)
    hour_count = 0
    for i in climate_HP_WH.values:
        if hour_count > 23:
            hour_count = 0
        
        average_loads[hour_count] += i[0]
        hour_count += 1
            
    num_days_in_month = ((last_hour_of_month+1)-first_hour_of_month) / 24
    return np.divide(average_loads, num_days_in_month)


# find average HP_SH per hour for a given month, year, and climate zone
def average_HP_SH(month, year, climate):  # pass in month and climate as integers
    assert climate >= 1 and climate <= 16
    assert month >= 1 and month <= 24
    
    first_hour_of_month = hour_bounds_by_month(month, year)[0]
    last_hour_of_month = hour_bounds_by_month(month, year)[1]
    climate_HP_SH = HP_SH_Raw.loc[first_hour_of_month:last_hour_of_month, str(climate)].to_frame()
    
    average_loads = np.zeros(24)
    hour_count = 0
    for i in climate_HP_SH.values:
        if hour_count > 23:
            hour_count = 0
        
        average_loads[hour_count] += i[0]
        hour_count += 1
            
    num_days_in_month = ((last_hour_of_month+1)-first_hour_of_month) / 24
    return np.divide(average_loads, num_days_in_month)