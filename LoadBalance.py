import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange
import PVCellDemandData as pvdd

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
# average for PV watts data on 1 kW size
def average_PV(month, year, climate):
    hourMap = pvdd.averageHourlyKWInMonth(climate, month)
    kW_list = np.zeros(24)
    for hour in range(24):
        kW_list[hour] = hourMap[hour]
    return kW_list

#Function that returns difference between demand and supply
def heatingDemandOnPVSupply(month, year, climate):
    supply = np.trapz(average_PV(month, year, climate))
    demand = np.trapz(cumulative_average_SH_and_WH(month, year, climate))
    return demand - supply




# sum over ER_WH, HP_WH, and HP_SH values
def cumulative_average_SH_and_WH(month, year, climate):
    ER_WH_values = average_ER_WH(month, year, climate)
    HP_WH_values = average_HP_WH(month, year, climate)
    HP_SH_values = average_HP_SH(month, year, climate)
    
    temp_sum = np.sum([ER_WH_values, HP_WH_values], axis=0)
    return np.sum([temp_sum, HP_SH_values], axis=0)



# find average ER_WH, HP_WH, and HP_SH per month per hour for each climate zone.
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
    assert month >= 1 and month <= 12
    
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
    assert month >= 1 and month <= 12
    
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

def graph_averagePV_every_month_every_climate():
    fig = plt.figure()
    fig.set_size_inches(40, 24)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    for climate in range(1, 17):
        ax = fig.add_subplot(4, 4, climate)
        plt.title("Climate:" + str(climate))
        for month in range(1, 13):
            ax.set_ylim(0, 1)
            if (climate == 1):
                ax.plot(x, average_PV(month, 2019, climate), label = "Month:" + str(month))
            else:
                ax.plot(x, average_PV(month, 2019, climate))
    legend = fig.legend()

def graph_averagePV_sums():
    fig = plt.figure()
    fig.set_size_inches(40, 24)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    for climate in range(1, 17):
        monthData = []
        y_pos = np.arange(len(months))
        ax = fig.add_subplot(4, 4, climate)
        plt.title("Climate:" + str(climate))
        for month in range(1, 13):
            monthTotal = np.trapz(average_PV(month, 2019, climate))
            monthData.append(monthTotal)
        plt.bar(y_pos, monthData, align='center', alpha=0.5)
        plt.xticks(y_pos, months)
    plt.show()


def graph_HP_SH_By_Climate_And_Month():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    fig.set_size_inches(28.5, 20.5)

    for i in range(16):
        ax = fig.add_subplot(4, 4, i+1)
        ax.set_ylim(0, 1.5)
        for j in range(12):
            houraveragebymonthclimate = average_HP_SH(j+1, 2019, i+1)
            plt.title("Climate: " + str(i+1))
            if i == 1:
                ax.plot(x, houraveragebymonthclimate, label = "Month:" + str(j))
            else:
                ax.plot(x, houraveragebymonthclimate)
                
    legend = fig.legend()

def graph_HP_WH_By_Climate_And_Month():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    fig.set_size_inches(28.5, 20.5)

    for i in range(16):
        ax = fig.add_subplot(4, 4, i+1)
        ax.set_ylim(0, 1.3)
        for j in range(12):
            houraveragebymonthclimate = average_HP_WH(j+1, 2019, i+1)
            plt.title("Climate: " + str(i+1))
            if i == 1:
                ax.plot(x, houraveragebymonthclimate, label = "Month:" + str(j))
            else:
                ax.plot(x, houraveragebymonthclimate)
                
    legend = fig.legend()

def graph_HP_SH_WH_By_Climate_And_Month():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    fig.set_size_inches(28.5, 20.5)

    for i in range(16):
        ax = fig.add_subplot(4, 4, i+1)
        for j in range(12):
            houraveragebymonthclimate = cumulative_average_SH_and_WH(j+1, 2019, i+1)
            plt.title("Climate: " + str(i+1))
            if i == 15:
                ax.set_ylim(0, 2.5)
                ax.plot(x, houraveragebymonthclimate, label = "Month:" + str(j))
            else:
                ax.set_ylim(0, 1.5)
                ax.plot(x, houraveragebymonthclimate)
                
    legend = fig.legend()


# Solar output at a specific hour - load usage at specific hour graphed for each climate zone
def graphPVMinusLoadUsage():
    average_HP_SH(1, 2019, 1)
    average_PV(1, 2019, 1)

    fig = plt.figure()
    fig.set_size_inches(40, 24)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    for climate in range(1, 17):  # for now, only look at January
        hourData = []
        y_pos = np.arange(24)
        ax = fig.add_subplot(4, 4, climate)
        plt.title("Climate:" + str(climate))
        for hour in range(0, 24):
            hourDiff = average_PV(1, 2019, climate)[hour] - average_HP_SH(1, 2019, climate)[hour]
            hourData.append(hourDiff)
        plt.bar(y_pos, hourData, align='center', alpha=0.5)

    plt.show()