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
    result = Year(name="Total")
   # print "Categories", categories[0].name
    for cat in categories:
       # print "day marker", len(cat.daylist), cat.name
        for i in range(0, len(cat.daylist)): #for each day of the year
            
            for j in range(0, 24): #for each hour of the day
                result.daylist[i].use[j] = result.daylist[i].use[j] + cat.daylist[i].use[j]
    result.distributeSeason()
    result.distributeWeekday(categories[0].firstday)
    return result

#difference in hourly energy loads
#ERROR>>>NEED TO DEBUG
def delta(categ1, categ2):
   diff = Year(name = "delta")
   for i in range(0, len(categ1.daylist)):
       
      # print "delta", len(categ1.daylist)
       for j in range(0,24):
           diff.daylist[i].use[j] = categ1.daylist[i].use[j]  - categ2.daylist[i].use[j]
         #  print "diff", i,j,categ1.daylist[i].use[j],categ2.daylist[i].use[j] ,diff.daylist[i].use[j]
   diff.distributeSeason()
   diff.distributeWeekday(categ2.firstday)       
   return diff        
##


