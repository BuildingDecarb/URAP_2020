#Shuba's edits
from AJ_EngGraphing import *
#import LoadProfiles_Inputs   # a file with utility rate structures


# has 2 outputs, 1st is the total annual cost, 2nd is the monthly cost vector
def flat(totalyear, price=0.190):

    totaluse = 0
    i= 1
    monthlycost = []
    for day in totalyear.daylist:
        totaluse = totaluse + sum(day.use)
        if i in monthend:
          #  print "monthend test", i, totaluse, price*totaluse
            monthlycost.append(totaluse*price)
            totaluse = 0
        i = i+1
    totalcost = sum(monthlycost)    
    return totalcost, monthlycost


# has 2 outputs, 1st is the total annual cost, 2nd is the monthly cost vector
def tier(totalyear, baseline=15, tier1=0.22376, tier2=0.28159, tier3=0.49334):
    # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-1.pdf
    totaluse = 0
    i= 1
    monthlycost = []
    for day in totalyear.daylist:
        totaluse = totaluse + sum(day.use)
        if i in monthend:
            monthlycost.append(min(baseline*30, totaluse) * tier1 + max(0, totaluse - baseline*30 ) * tier2 + max(0, totaluse -4*baseline*30) * (tier3 - tier2))
            totaluse = 0
        i = i + 1
    totalcost = sum(monthlycost)    
    return totalcost, monthlycost

# has 2 outputs, 1st is the total annual cost, 2nd is the monthly cost vector
def tou(load, speak=0.25, soffpeak=0.20, wpeak=0.20, woffpeak=0.15):
    # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_EL-TOU.pdf
    speaksum = 0
    soffpeaksum = 0
    wpeaksum = 0
    woffpeaksum = 0
    days1 = []
    days2 = []
    days3 = []
    days4 = []   #NOT WORKING - all clumped
    i = 1
    for day in load.daylist:
        if day.season == "summer":
            if day.weekday == "weekday":
               # print "summer weekday" 
                speaksum = speaksum + sum(day.use[15:20])
                soffpeaksum = soffpeaksum + sum(day.use[:15]) + sum(day.use[20:])
            else:
               # print "summer weekend"
                soffpeaksum = soffpeaksum + sum(day.use)
        else:
            if day.weekday == "weekday":
               # print "winter weekday"
                wpeaksum = wpeaksum + sum(day.use[15:20])
                woffpeaksum = woffpeaksum + sum(day.use[:15]) + sum(day.use[20:])
            else:
             #   print "winter weekend"
                woffpeaksum = woffpeaksum + sum(day.use)
        if i in monthend:
           # print "Monthend",i, speaksum, soffpeaksum, wpeaksum, woffpeaksum
            days1.append(speaksum)
            days2.append(soffpeaksum)
            days3.append(wpeaksum)
            days4.append(woffpeaksum)
            speaksum = 0
            soffpeaksum = 0
            wpeaksum = 0
            woffpeaksum = 0
        i = i + 1
        monthlycost = processtou([days1, days2, days3, days4], [speak, soffpeak, wpeak, woffpeak])
    return sum(monthlycost), monthlycost

def processtou(monthly, prices):
    """
    Helper function to calculate energy cost by month for a Year of energy use, following the time of use pricing scheme.
    Parameters:
        monthly (int[][]): [speak use, soffpeak use, wpeak use, woffpeak use]x12 for each month
        prices (int[]): [speak price, soffpeak price, wpeak price, woffpeak price]
    Returns:
        monthlycost (int[]): energy cost by month for a TOU pricing scheme
    """
    monthlycost = []
    for i in range(0, len(monthly[0])):
    #    print " price", prices[0], prices[1], prices[2],prices[3]  #en(monthly[0])        #, len(monthly[1]), len(monthly[2]), len(monthly[3]
        monthlycost.append(monthly[0][i] * prices[0] + monthly[1][i] * prices[1] + monthly[2][i] * prices[2] + monthly[3][i] * prices[3])
    return monthlycost

#categ = [sh_year, wh_year] #  [cool_year, pool_year, df_year, sh_year, wh_year]
#heating = grandSum(categ)

#categ1 = [ cool_year,df_year ]
#baseload = grandSum(categ1)

#allcateg = [ sh_year, wh_year,cool_year,df_year ]
#total = grandSum(allcateg)

#print "flat cost", flat(baseload)
#print "tier cost", tier(baseload)
#print "TOU cost baseload", tou(baseload)

#print "\n flat cost heat", flat(heating)
#print "tier cost heat", tier(heating)
#print  " \n TOU cost heat ", tou(heating)
#print "\n TOU cost total", tou(total)








