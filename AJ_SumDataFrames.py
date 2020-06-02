from AJ_BuildDataFrames import *
from datetime import datetime, timedelta
from calendar import monthrange
from datetime import date

def grandSum(categories): 
    """
    Takes an array of Years and sums their dayuse attribute.
    Parameters:
        categories (Year[]): an array of Years of different energy end-uses
    Returns:
        total (Year): a Year whose dayuse is the sum of every energy end-use represented in CATEGORIES
    """
    total = Year(name="Total")
   # print "Categories", categories[0].name
    for cat in categories:
        for i in range(0, len(cat.daylist)): #for each day of the year
         #   print "day marker", len(cat.daylist), cat.name
            for j in range(0, 24): #for each hour of the day
                total.daylist[i].use[j] = total.daylist[i].use[j] + cat.daylist[i].use[j]
    return total

def delta(categ1, categ2):
   diff = Year(name = "delta")
   for i in range(0, len(categ1.daylist)):
      # print "delta", len(categ1.daylist)
       for j in range(0,24):
           diff.daylist[i].use[j] = categ1.daylist[i].use[j]  - categ2.daylist[i].use[j]
         #  print "diff", i,j,categ1.daylist[i].use[j],categ2.daylist[i].use[j] ,diff.daylist[i].use[j]
   return diff        
##
categories = [sh_year,wh_year,cool_year,df_year]
categtotal = grandSum(categories)
categ1 = [categtotal]
##
categ2 = [pv_year]
##
netload = delta(categtotal,pv_year)
categ3 = [netload]

max_sh = df_sh[climatezone].max()
hr_maxsh = df_sh[climatezone].idxmax()

max_wh = df_wh[climatezone].max()
hr_maxwh = df_wh[climatezone].idxmax()

max_cool = df['cooling'].max()
hr_maxcool = df['cooling'].idxmax()

max_base = df['total'].max()
hr_maxbase = df['total'].idxmax()

maxcool =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxcool)
maxwh =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxwh)
maxsh =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxsh)
maxbase =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxbase)

#print "max", max_sh, hr_maxsh, max_wh, hr_maxwh, max_cool, hr_maxcool, max_base, hr_maxbase
#print "dates",  maxsh, maxwh,maxcool, maxbase

#max_agg = categtotal['total'].max()
#print "max agg", max_agg

##categories = [sh_year, wh_year, cool_year,df_year] #  [cool_year, pool_year, df_year, sh_year, wh_year]
##total_year = grandSum(categories)
##print "test"  #, total_year
##print("Annual energy use from cooling: %f kWh" % cool_year.sumYear())
###print("Annual energy use from pool pump: %f kWh" % pool_year.sumYear())
###print("Annual energy use from base load: %f kWh" % df_year.sumYear())
##print("Annual energy use from space heating: %f kWh" % sh_year.sumYear())
##print("Annual energy use from water heating: %f kWh" % wh_year.sumYear())
###print("Annual energy use from PV: %f kWh" % pv_year.sumYear())
##print("\n")
##print("Annual energy use from all sources: %f kWh" % total_year.sumYear())
