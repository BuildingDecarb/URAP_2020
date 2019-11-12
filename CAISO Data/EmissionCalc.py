"""DISCLAIMER: The data calculations in this file are obtained using the first of each month as a representative
for the entire month. Additionally, it has not yet been integrated with the housing class"""

import pandas as pd

monthly_emissions = pd.read_csv("month_table.csv")
months = {"Jan": 0,
          "Feb": 1,
          "Mar": 2,
          "Apr": 3,
          "May": 4,
          "Jun": 5,
          "Jul": 6,
          "Aug": 7,
          "Sep": 8,
          "Oct": 9,
          "Nov": 10,
          "Dec": 11}
days_in_months = {1: 31,
          2: 28,
          3: 31,
          4: 30,
          5: 31,
          6: 30,
          7: 31,
          8: 31,
          9: 30,
          10: 31,
          11: 30,
          12: 31}

def get_total_emissions_from_table(): #This would be like if each month only had ONE DAY
    total = 0
    for i in range(1, monthly_emissions.shape[1]): #Iterates through each column--hours 1 to 24
        for j in range(11): #Iterates through each month
            total += monthly_emissions.iloc[j, i]
    return total

def get_annual_emissions():
    return get_emissions_month_range("Jan", "Nov")

def get_emissions_hour_range(st_month, end_month, st_hour = 1, end_hour =24):
    st_month_num = months[st_month]
    end_month_num = months[end_month]
    month_total = 0
    total = 0
    for i in range(st_hour, end_hour + 1): #Iterates through each column--hours 1 to 24
        for j in range(st_month_num, end_month_num + 1): #Iterates through each month
            month_total += monthly_emissions.iloc[j, i]
            if j == end_month_num:
                temp = month_total * days_in_months[j + 1]
                total += temp
                month_total = 0
    return total

def get_emissions_month_range(st_month, end_month):
    return get_emissions_hour_range(st_month, end_month) # Will just do the whole day


print(get_annual_emissions())
print(get_emissions_hour_range("Jun", "Jun"))