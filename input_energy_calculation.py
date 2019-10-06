import numpy as np
import pandas as pd
from pandas import ExcelFile

column = "input_kWh1"

data = pd.read_csv(r'C:\Users\rayan\Downloads\WH_HourlyLoadProfiles-20190924T203804Z-001\WH_HourlyLoadProfiles\CZ3_3BR\test.csv')

def annualEnergyConsumption():   #completed and tested
    return data[column].sum()
    
def monthlyEnergyConsumption(month):  #completed and tested
    sum = 0
    startingPoint = (722 * (month - 1)) #722 rows per month
    endPoint = startingPoint + 722
    for i in range(startingPoint, endPoint):
        sum += data.iloc[i, 8]
    return sum 

def dayEnergyConsumption(month, day):  #completed and tested
    sum = 0
    startingPoint = ((722 * (month - 1)) + 1) + (24 * (day - 1))
    endPoint = startingPoint + 24
    for i in range(startingPoint - 1, endPoint - 1):
        sum += data.iloc[i, 8]
    return sum


    

    

monthlyEnergyConsumption(2)
