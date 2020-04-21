from AmyJ_Annual_Energy_TotalCustomer import *


def grandSum(categories): 
    """
    Takes an array of Years and sums their dayuse attribute.
    Parameters:
        categories (Year[]): an array of Years of different energy end-uses
    Returns:
        total (Year): a Year whose dayuse is the sum of every energy end-use represented in CATEGORIES
    """
    total = Year(name="Total")
    for cat in categories:
        for i in range(0, len(cat.daylist)): #for each day of the year
            for j in range(0, 24): #for each hour of the day
                total.daylist[i].use[j] = total.daylist[i].use[j] + cat.daylist[i].use[j]
    return total

categories = [sh_year, wh_year, cool_year,df_year, pv_year] #  [cool_year, pool_year, df_year, sh_year, wh_year]
total_year = grandSum(categories)
print "test", total_year
print("Annual energy use from cooling: %f kWh" % cool_year.sumYear())
#print("Annual energy use from pool pump: %f kWh" % pool_year.sumYear())
#print("Annual energy use from base load: %f kWh" % df_year.sumYear())
print("Annual energy use from space heating: %f kWh" % sh_year.sumYear())
print("Annual energy use from water heating: %f kWh" % wh_year.sumYear())
print("Annual energy use from PV: %f kWh" % pv_year.sumYear())
print("\n")
print("Annual energy use from all sources: %f kWh" % total_year.sumYear())
