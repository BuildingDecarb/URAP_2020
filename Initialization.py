
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import *
#import matplotlib.patches as mpatches #for stack plots

#from Inputs import *
#from Inputs_ElecRate import *
##from Inputs_Energy import *
from Housing_Class1 import *
#from Appliances_Class import *
#==============================================================================
import numpy as np
import copy
import datetime

aggregageDevices = {}  # indexed by year and device type holds the number of devices of that type

def getDead(p1_homes, homeType, fuelName, k, yr):

    return sum([homes.devices[0].annualreplacement(yr) for homes in p1_homes if (homes.cznum ==k and homes.type == homeType and homes.devices[0].fuel.name== fuelName)])

def computeInitialSnapshot():
   
    HomesSnapShot = {}
    year = PastPastYear
   
    for k in range(1,Numcz+1):  # number of CZs
        print('BeginInitstamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())) 
      #for i in range(0,1):
        p_homes = []

        hhsize = cz[k,ThisYear].HHsize *  samplesize * 10**6   #number of households today in cz j  #samplesize defined in Inputs.py
        num_heaters = HH_withHeat[k,ThisYear]  #% of heating in CZ k (current saturation)
        num_coolers = HH_withCool[k,ThisYear]   #current cooling saturation per CZ
#=============Below stock with heating====================================        ##==============================================================================
        Stck_SFNG =  hhsize * P1  * num_heaters       #P1 is the % of SF, hese are houses with Heating and cooling (NG based heating P1 is assinged in Inputs.py
        Stck_SFER =  hhsize *   P2 * num_heaters    # P2 is %of ER houses and this is  STck_SFER are the #of homes iwth ER based heating can have cooling too
 #==============Below Stock wiht cooling ===================================================
        Stck_SFNGCool = int(round(hhsize *   num_coolers  ))  #Houses with cooling 
  #      Stck_SFERCool =   int(round(SFShare  * hhsize *  P2*  num_coolers  ))  #houes with cooling
##==============================================================================
#        hhtotal += Stck_SFNG + Stck_SFER + Stck_MFNG+ Stck_MFER
       # print "initinit", k, year, hhsize, P1, P2, num_heaters, num_coolers, Stck_SFNG, Stck_SFER, Stck_SFNGCool
        is_new = False           # old homes are created here.
        r0 = R0present
        r1 = R1present
        r2 = R2present

        NG1 =  Device("NGH", NG, NG0_EF, 0,k, size1,size2,r0,r1,r2, year , NG_LT, NGIC, OM_NG)
        E1 = Device("ERH", Elec, E0_EF,0, k, size1,size2, r0,r1,r2, year ,EL_LT, ERIC, OM_EL)
        E1_Cool = Device( "Cooler", Elec, 0, AC0_EF, k,size1,size2,r0,r1,r2,  year, EL_LT ,ACIC, OM_EL, True, Ref1)
        
        NGHeat1 = [NG1]    # NG Heating alone
        NGHeatCool1 = [NG1,E1_Cool]   #NG Heating and A.C Cooling

        ERHeat1 = [E1]  #ERW heating
        #ERHeatCool1 = [E1,E1_Cool]

        SFNG_HH = int(round(Stck_SFNG - Stck_SFNGCool) )   # Houses with just NG heating
        SFER_HH = int(round(Stck_SFER) )    # Houses with just ER heating
        homesL1 = []
        for _ in range(SFNG_HH):
            homesL1.append(SFHomes("SFNG",SFNG_HH,k, size1, size2, year, NGHeat1,False))   #is_new== False, means an  old home.,,not used

        for _ in range(Stck_SFNGCool):
            homesL1.append(SFHomes("SFNGCool",Stck_SFNGCool, k,size1, size2, year,NGHeatCool1,False))
        
        for _ in range(SFER_HH):
            homesL1.append(SFHomes("SFER",SFER_HH, k,size1, size2, year,ERHeat1,False))

      
        p_homes.extend(homesL1)

        if (year, k) in HomesSnapShot:
            HomesSnapShot[(year,k)] = updateHomeStats(HomesSnapShot[(year, k)], HomesStats(year, k, copy.copy(p_homes)))
        else:
            HomesSnapShot[(year,k)] = HomesStats(year, k, copy.copy(p_homes))
       # print "Initialization", k, year, hhsize, Stck_SFNG, Stck_SFER, "..",SFNG_HH, Stck_SFNGCool, SFER_HH

       # SnapShotYear = HomesSnapShot[(year,k)]

    #   if (year, k) not in HomesSnapShot:
    #         continue

    #   for home in HomesSnapShot[(year,k)].homes:
    #         hometype = home.type
    #         dev = home.devices

    #         if home.type not in HomesSnapShot[(year,k)].aggregateHomeStats:
    #                   HomesSnapShot[(year,k)].aggregateHomeStats[hometype] = AggregateStats()

    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].num += 1
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].numdev = len(dev)
    #         engheat = home.HHenergyUsage_BTU()[0]/kWh_BTU   #heating energy
    #         engcool = home.HHenergyUsage_BTU()[1]/kWh_BTU   # cooling energy

    #         hhng = home.HHenergyUsage_units()[0]  #NG usage in kWh
    #         hhelec = home.HHenergyUsage_units()[1]   #electricity usage
    #         hhemis1 = home.HHemissions(year)[0]
    #         hhemis2 = home.HHemissions(year)[1]
    #         hhengcost1 = home.HHEnergyCost(year)[0]   #NG Cost
    #         hhengcost2 = home.HHEnergyCost(year)[1]
    #         hhcapcost = home.HHDevicesCapCost(year)
           

    #   #      print "mid test", k,year, hometype, hhng,hhelec, engheat, engcool, hhemis1, hhemis2

    #         cnt =   HomesSnapShot[(year,k)].aggregateHomeStats[hometype].num
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].eng1 += hhng
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].eng2 += hhelec
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].heateng += engheat
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].cooleng += engcool
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].emis1 += hhemis1
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].emis2 += hhemis2
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].engCost1 += hhengcost1
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].engCost2 += hhengcost2
    #         HomesSnapShot[(year,k)].aggregateHomeStats[hometype].replaceCost += hhcapcost
           
    #         for d in dev:
    #             dname = d.name
    #             devcnt =   getDeviceCountinHome(HomesSnapShot[(year,k)], dname, hometype, year)
    #             HomesSnapShot[(year,k)].aggregateHomeStats[hometype].aggDevices[year, dname] = devcnt
    #             devstypes   =    getDevices(HomesSnapShot[(year,k)], hometype)
    #             #devsyear  =    getDevicesYear(HomesSnapShot[(year,k)], dname, year)
    #             devcountyear   =    getDeviceCountYear(HomesSnapShot[(year,k)], dname,year)
    #           #  print "Dev stats", year,cnt, hometype,dname, devcnt,  devcountyear

    return HomesSnapShot

