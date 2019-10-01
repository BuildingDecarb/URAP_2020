# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 05:36:53 2017
@author: shubaraghavan
"""

from scipy.stats import weibull_min
#from HDD_CDD_UValues import *
from Inputs_Energy import *
from Inputs_ElecRate import *
from RefrigerantCalc import Refrigerant
from AnnualHeatDemand import *
import numpy as np
from numpy import *

HPCond = {} #indexed by year, stock number

HPCondHeatEng= {} # Total Heat Energy usage by stock in a year
HPCondCoolEng = {}  # Total cooling energy usage by stock in a year

class FuelType:
    def __init__(self, name,unitEng,UnitEngCost, UnitEmissions):
        self.name = name
        self.unitEng = unitEng
        self.UnitEngCost = UnitEngCost
        self.UnitEmissions= UnitEmissions
#Time = 2020

UltimYr0 = 15 #MeanLife    #vintage <2000..normal life till ThisYear+3..and then killed
UltimYr1 =  15 #MeanLife      #vintage between 2000 and THisYear =2020..early demise for these ineff adoptions
UltimYr2 = 15 #MeanLife       # after 2020 adoptions are assumed to be efficient ..so will live normal life
#print "UNITNG",UnitNG
NG = FuelType("NG", UnitNG , NGCostYrly, NGEmisYrly)
Elec = FuelType("Elec", UnitElec, ElecCostYrly, ElecEmisYrly)

Ref1 = Refrigerant(2088, 1, 0.005, 0.05, 0.2)  #R-410A
Ref2 = Refrigerant(675, 1, 0.005, 0.05, 0.2)   #HFC-32  https://www.epa.gov/sites/production/files/2016-12/documents/international_transitioning_to_low-gwp_alternatives_in_res_and_com_ac_chillers.pdf
Ref3 = Refrigerant(3, 1, 0.005, 0.05, 0.2)     #1

Ref11 = Refrigerant(1725, 1, 0.005, 0.1, 0.3)  #..
Ref12 = Refrigerant(650, 1, 0.005, 0.1, 0.3)   #...
Ref13 = Refrigerant(1, 1, 0.005, 0.1, 0.3)

class Device:
    def __init__(self, name, fuel, ef, ef_cooler, C, outputTemp=125, s1, s2, Rval0, Rval1, Rval2, vintage, lt, IC, OM, hasRefrigerant=False, refrigerant=Refrigerant()):
        self.name = name
        self.fuel = fuel
        self.ef = ef  # Efficiency
        self.ef_cooler = ef_cooler
        self.C = C  # Climate zone number
        self.HDD = cz[C, vintage].hdd  # cz is a dict mapping climate zone number to climatezone object
        self.CDD = cz[C, vintage].cdd
        self.inputTemp = cz[C, vintage].inputTemp
        self.outputTemp = outputTemp
        self.s1 = s1  # surface area of wall
        self.s2 = s2  # surface area of roof
        self.Rval0 = Rval0  # insulation of window
        self.Rval1 = Rval1  # insulation of walls
        self.Rval2 = Rval2  # insulation of roof
        self.vintage = vintage  # Year of installation...typically assumed happens beginning of a year
        # self.StockSize = StockSize  #Original Num is the number of waterheaters created in the 'vintage'year
        self.lt = lt  # Lifetime
        self.IC = IC  # Initial Cost could be just Capex or could be Capex+initial cost to build infrastructure
        self.OM = OM  # Operations and Maintenance
        self.hasRefrigerant = hasRefrigerant
        self.refrigerant = refrigerant
        self.IncTemp = self.outputTemp - self.inputTemp  #cz[C,vintage].IncTemp
        self.dailyVol = 50

    def weib0(self):   #before vintage year = 2005
        x = range(0, self.lt+UltimYr0+1)
        shape = 2.1
        loc = 1.0
        w = weibull_min.cdf(x,shape,loc,scale = self.lt+2  )
      #  print "w2",w
        return(w)

    def weib1(self):   #before vintage year = 2005
        x = range(0, self.lt+UltimYr0+1)
        shape = 2.1
        loc = 1.0
        w = weibull_min.cdf(x,shape,loc,scale =self.lt+2 )
      #  print "w2",w
        return(w)

    def weib2(self):

        x = range(0, self.lt+UltimYr0+1)
        shape = 2.1
        loc = 1.0
        w = weibull_min.cdf(x,shape,loc,scale = self.lt +2)
      #  print "w2",w
        return(w)
#following outputs conditional prob of dying any specific year based on weibul distr

    def dead_prob0(self,yr):
       # print "dead_prob Input", yr, self.name, self.vintage ,  self.lt,  UltimYr2
        if yr >= self.vintage + self.lt + UltimYr0 :                 #past life then dead
           return 1.0
        else:
           dead_yr = self.weib0()[yr - self.vintage] #cumulative dead up tothis year
           dead_yr1 = self.weib0()[yr+1 - self.vintage]# cumulative dead next year
           dead_thisyr = max(0,dead_yr1 - dead_yr )  #dead this year
           if dead_yr == 0 or dead_yr1 ==0:  #if cumulative death is 0 then prob of death is 0
               return 0.0
           elif round(dead_yr,0)==1 and round(dead_yr1,0)==1:
               return 1
           else:
               p = (dead_thisyr)/(1-dead_yr)  #prob of death this year
           #    print "dead_prob0",yr,self.vintage, dead_thisyr,dead_yr, dead_yr1, p  #,dead_thisyr, 1-dead_yr  #/dead_yr
               return p

    def dead_prob1(self,yr):
       # print "dead_prob Input", yr, self.name, self.vintage ,  self.lt,  UltimYr2
        if yr >= self.vintage + self.lt + UltimYr1 :                 #past life then dead
           return 1.0
        else:
           dead_yr = self.weib1()[yr - self.vintage] #cumulative dead up tothis year
           dead_yr1 = self.weib1()[yr+1 - self.vintage]# cumulative dead next year
           dead_thisyr = max(0,dead_yr1 - dead_yr )  #dead this year
           if dead_yr == 0 or dead_yr1 ==0:  #if cumulative death is 0 then prob of death is 0
               return 0.0
           elif round(dead_yr,0)==1 and round(dead_yr1,0)==1:
               return 1
           else:
               p = (dead_thisyr)/(1-dead_yr)  #prob of death this year
            #   print "dead_prob1",yr,self.vintage, dead_thisyr,dead_yr, dead_yr1,p  #,dead_thisyr, 1-dead_yr  #/dead_yr
               return p  #

    def dead_prob2(self,yr):
       # print "dead_prob Input", yr, self.name, self.vintage ,  self.lt,  UltimYr2
        if yr >= self.vintage + self.lt + UltimYr2 :                 #past life then dead
           return 1.0
        else:
           dead_yr = self.weib2()[yr - self.vintage] #cumulative dead up tothis year
           dead_yr1 = self.weib2()[yr+1 - self.vintage]# cumulative dead next year
           dead_thisyr = max(0,dead_yr1 - dead_yr )  #dead this year
           if dead_yr == 0 or dead_yr1 ==0:  #if cumulative death is 0 then prob of death is 0
               return 0.0
           elif round(dead_yr,0)==1 and round(dead_yr1,0)==1:
               return 1
           else:
               p = (dead_thisyr)/(1-dead_yr)  #prob of death this year
           #    print "dead_prob",yr, dead_thisyr,dead_yr, dead_yr1,p  #,dead_thisyr, 1-dead_yr  #/dead_yr
               return p  #condition

#the following based on the above cond prob. hastens the demise of older vintages
    def death_prob(self, yr):
         if yr > self.vintage:
             life = yr - self.vintage
         else:
             return 0
         if self.vintage <= 2000 and life > 40 :
             return 1
       #  elif self.vintage >2000 and self.vintage <=ThisYear and life
         elif self.vintage <= 2000 and yr < Phase11:
          #   print "P0", yr, self.vintage, self.dead_prob0(yr)
             return self.dead_prob0(yr)
         elif self.vintage >2000 and self.vintage <= ThisYear and  yr < Phase11:  #this year >2018 and appliance installed between 2000 and 2018
          #   print "P1", yr, self.vintage, self.dead_prob1(yr)
             return self.dead_prob1(yr)
         else:
           #   print "P2", yr, self.vintage, self.dead_prob2(yr)
              return self.dead_prob2(yr)

    def dead_alive(self,yr):
         p = self.death_prob(yr)
         N =1   #coin tossed N times..
         n=1
         s =sum(np.random.binomial(n, p,N)==1)/N  #   flipping a coin - with prob =p heads, device dies
      #   print "prob", yr, p,s
         return s

    def deadsofar(self, yr):

        if yr > self.vintage and yr < self.vintage+ self.lt + UltimYr2:

             if self.vintage <= 2000 and yr < Phase11:
              #   print yr, self.vintage
                 return self.weib0()[yr-self.vintage]
             elif self.vintage > 2000 and self.vintage <= ThisYear and yr <= Phase11:
               #   print yr, self.vintage
                  return self.weib1()[yr-self.vintage]
             else:
                #  print yr, self.vintage
                  return self.weib2()[yr-self.vintage]

        elif yr >= self.vintage + self.lt + UltimYr2:
            return 1
        else:
            return 0

    def numAlive(self,yr):
       return (1 - self.deadsofar(yr))

    def AnnualWaterEngUsage(self, dailyVol,IncTemp):
         #   print "WH ENgy Test", dailyVol, IncTemp
            return dailyVol * IncTemp * UnitBTU *  365/self.ef   #

    def AnnualHeatEngUsage_BTU(self):  #does not include auxiliary elec usage by NG furnace
         if self.ef == 0.0 or self.name == "":
             return 0.0
         else:

             engdemand = AnnualEngDemand(self.fuel, self.HDD, self.s1,self.s2, self.Rval0, self.Rval1, self.Rval2, self.ef)
             if self.fuel.name == "NG":
                  add_demand = 0   #the additional Elec usage is only used for calculating
                #  add_demand = NG_AnnualElecUsage * kWh_BTU
                  engdemand +=  add_demand
             return engdemand

    def AnnualHeatEngUsageTotal_BTU(self):  #for feeding into cost calculation...
         if self.ef == 0.0 or self.name == "Cooler":
             return 0.0
         else:
             engdemand = AnnualEngDemand(self.fuel, self.HDD,  self.s1,self.s2, self.Rval0, self.Rval1, self.Rval2,self.ef)
             if self.fuel.name == "NG":
                 add_demand = 0   #the additional Elec usage is only used for calculating
                 add_demand = NG_AnnualElecUsage * kWh_BTU
                 engdemand +=  add_demand
             return engdemand

    def AnnualCoolEngUsage_BTU(self):
           if self.name == "Cooler" or self.name == "Cond":
              engdemand = AnnualCoolingDemand(self.fuel, self.CDD,  self.s1,self.s2,self.Rval0, self.Rval1, self.Rval2,self.ef_cooler)
           else:
               engdemand = 0.0
      #     print "Cooling Test", self.name, engdemand
           return engdemand

    def annualHeatEngUsage(self): #Annual Energy in kWh     THIS CONTAINS ELEEC Blower usage
            demand = self.AnnualHeatEngUsage_BTU()
            if self.fuel.name == "NG":
                add_demand = NG_AnnualElecUsage  # electrical Blower energy in kWh
                return (demand/kWh_BTU) + add_demand
            elif self.fuel.name == "Elec":
                return demand/kWh_BTU

    def AnnualEngCost(self, yr, eng):            #'eng' Contains NG blower usage
#==============================================================================
             demand = eng #in BTU
           #  print "Cost", yr, demand
             if self.fuel.name == "NG":
                 demand = demand/Therm_BTU

                 if "WH" in self.name:
                     elecCost = 0
                     ngCost = demand  * NGCostYrly[yr]
                 else:
                     elecCost = NG_AnnualElecUsage * ElecCostYrly[yr]
                     ngCost = (demand - NG_AnnualElecUsage/Therm_kWh)  * NGCostYrly[yr]
                 totalCost = ngCost+elecCost
               #  print "NG It is",
             elif self.fuel.name == "Elec":
                 ngCost = 0
                 demand = demand/kWh_BTU
                 elecCost = demand * self.fuel.UnitEngCost[yr]
                 totalCost = ngCost + elecCost
#==============================================================================
        #     print "\n TestCost", yr, self.name, self.fuel.name, demand, self.fuel.UnitEngCost[yr], NG_AnnualElecUsage,ngCost, elecCost
        #     print "\n"
             return totalCost

    def AnnEmissions(self,yr, eng):  # eng contains NG blower usage;
                                      #result in tons  with  REFRIGERANT
            demand = eng             #in BTU  # also eng can be heating and/or cooling energy..
            ngEmis = 0
            elecEmis = 0
            if self.fuel.name == "NG":
                 if "WH" in self.name:
                     elecEmis = 0
                     demand = demand/Therm_BTU
                     ngEmis = demand * self.fuel.UnitEmissions[yr]/1000
                  #   print "WH", self.name, demand, ngEmis, elecEmis
                 else: # this is a NG space heater
                     elecEmis=   NG_AnnualElecUsage * ElecEmisYrly[yr]/1000  # This is the NG electric blower's energy
                     ngdemand = (demand- NG_AnnualElecUsage)/Therm_BTU
                     ngEmis = ngdemand * self.fuel.UnitEmissions[yr]/1000
                 #    print "SH",self.name,demand, ngEmis, elecEmis
                # totalEmis = ngEmis  +  elecEmis
            elif self.fuel.name == "Elec":  #in kWh
                 demand = demand/kWh_BTU
                 elecEmis = demand * self.fuel.UnitEmissions[yr]/1000
                 if self.hasRefrigerant == True:
                     refleak = self.AvgRefLeaks(yr) #already converted to tons
                     elecEmis += refleak
            totalEmis = elecEmis +ngEmis
            #print "\n Elec EMIS",self.name, demand, self.fuel.name,ngEmis, elecEmis
            return ngEmis, elecEmis, totalEmis


    def AnnTotalEmissions(self,yr, eng):  #in tons with REFRIGERANTS
       # if self.hasRefrigerant == False:
            return self.AnnEmissions(yr,eng)[2]
       # else:
       #     return ( self.AnnEmissions(yr,eng)[2]+ self.AvgRefLeaks(yr)  )

    def annualizedEmissions(self, vint,eng):  #in tons (THIS IS THE AVERAGE EMISSIONS..NOT DISCOUNTED
        result = {}
      #  result1 = {}
        for i in range(vint, vint+self.lt):
            result[i] = self.AnnTotalEmissions(i,eng)  #INCLUDING DIRECT AND INDIRECT
       #     result1[yr] = self.AnnEmissions(yr)
        annEmis = sum(result.values())/self.lt
        return (annEmis)


    def RefLeaks(self, yr ):
        result = {}
        if (self.hasRefrigerant == True):
            leakages = self.refrigerant.RefLeakage(yr, yr+self.lt)
            for i in range( yr, yr + self.lt+1):
                result[i]=leakages[i]
        return result

    def AvgRefLeaks(self,yr):  #in tons of CO2 eq
        result = {}
        avgleak = 0
        if (self.hasRefrigerant == True):
            result = self.RefLeaks(yr)  #in tons
            #for i in range(vint, vint+ self.lt):
             #   avgleak = avgleak + result[i]/(1+CCDiscRate)**(i-vint+1)
            avgleak = sum(result.values())/self.lt
        else:
            avgleak = 0
        return avgleak


    def annualCarbonCost(self, vint, eng, UnitCarbonPrice=20):  #$20/ton is the default rate for Carbon...if not specified when calling the func
        result = {}
        for i in range(vint, vint+self.lt):
            if self.hasRefrigerant == True:
                result[i] = UnitCarbonPrice * (self.AnnualEmissions(i, eng)  )
            else:
                result[i] = UnitCarbonPrice * (self.AnnEmissions(i, eng) )
        return result

    def averageCarbonCost(self, vint,eng,  UnitCarbonPrice=20):
        result = {}
        result = self.annualCarbonCost(vint, eng, UnitCarbonPrice)
        return sum(result.values())/self.lt

    def NPVEmissions_Refrigerant(self, yr):
         if self.hasRefrigerant == True:
             result = 0
             RefLeek = self.RefLeaks(yr)
             for i in range(yr, yr+self.lt+1):
                 result = result + RefLeek[i]/(1+DiscRate)**(i-yr+1)
         else:
             result = 0
         return result

    def NPVEmissions_Indirect(self, yr, eng):
        # print "NPV_Indirect", yr, eng, DiscRate, self.lt
         result = 0
         for i in range(yr, yr+self.lt+1):
            # print "NPV_INdirect", yr, i, self.AnnEmissions(i,eng)[2]  #thisis the total emissions
             result = result + self.AnnEmissions(i, eng)[2]/(1+DiscRate)**(i-yr+1)
         return result

    def NPVEmissions(self, yr, eng):  #NPV OF EMISSIONS USED FOR COMPUTING NPV OF CARBONCOST
      #  print "NPVEMissions", yr, eng
        NPVEm = self.NPVEmissions_Indirect(yr, eng)+ self.NPVEmissions_Refrigerant(yr)
        return NPVEm

    def lcc(self, yr, eng, UnitCarbonPrice =21):  #levelized
        return (self.NPVEmissions(yr, eng)*UnitCarbonPrice + self.calcNPV(yr,eng) )

    def totalCapex(self):      #total cost of the stock of vintage yr
        return self.StockSize * self.IC

#================================================================================
#Life cycle cost (LCC) comprises of the 3 functions below
    def NPVCost(self,yr):  #Without energy cost with capital cost fixed ahead
        NPV = self.IC
      #  print "START", NPV, yr, self.lt
        for I in range(yr, self.lt +yr):
             NPV = NPV + (self.OM[I-yr])/(1+DiscRate)**(I-yr+1)
        return NPV

    def NPVCost_LT(self,yr, horizon):  #Without energy cost with capital cost fixed ahead
        NPV = self.IC
      #  print "START", NPV, yr, self.lt
        for I in range(yr, horizon +yr):
             NPV = NPV + (self.OM[I-yr])/(1+DiscRate)**(I-yr+1)
        return NPV

    def NPVEngCost(self,yr,eng):  #Energy cost alone
        NPV = 0
        for I in range(yr, self.lt+yr):
             NPV = NPV + (self.AnnualEngCost(I,eng))/(1+DiscRate)**(I-yr+1)
        return NPV

    def NPVCC(self,vint, eng,CarbonCost= 55):  #NPV of carbon cost
       # print "NPVCC", vint, eng
        return self.NPVEmissions(vint,eng)*CarbonCost
#===================================================================================

    def calcNPV(self,yr,eng):   # with energy cost with capital cost fixed ahead
         NPV = self.IC
         for I in range(yr, self.lt+ yr):
            # print I, self.OM[I-ThisYear], self.AnnualEngCost(I)
             NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I,eng))/(1+DiscRate)**(I-yr+1)
         return NPV

    def calcNPV_Capex(self, yr, Capex,eng):  #changing capex
         NPV = Capex
         for I in range(yr,self.lt +yr):
              NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I,eng))/(1+DiscRate)**(I-yr+1)
         return NPV

    def calcNPV_LifeTime(self, yr, lifetime,eng):  #changing can specify a difff lifetime other than self.lt
         NPV = self.IC
         for I in range(yr,lifetime +yr):
              NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I,eng))/(1+DiscRate)**(I-yr+1)
         return NPV

    def annualizedNPV(self,yr,eng):
        return self.calcNPV(yr,eng)/self.lt

    def CCBreakEven(self, Hx, yr,eng1,eng2):  #breakeven carbon cost
         X = (- self.calcNPV(yr,eng1)/self.lt+ Hx.calcNPV(yr,eng2)/Hx.lt)
         Y = ( - Hx.NPVEmissions(yr,eng2)/Hx.lt + self.NPVEmissions(yr,eng1)/self.lt )
     #    print "CCBreakeven",yr, self.name, Hx.name, X, Y

         breakeven = X/Y
         if Y ==0:
             return ( (Hx.calcNPV(yr,eng2)/Hx.lt)/(self.calcNPV(yr,eng1)/self.lt))
         if X <=0 and Y<0:
             return breakeven
         elif X >0 and Y >=0:
             return breakeven
         elif X <= 0 and Y > 0:
             return breakeven  #negative cost of carbon..as new tech is cheaper
         else:
             return breakeven  #X >= 0 and Y <0..Hx.NPV > self.NPV and Hx.Emis > self.Emis


    def payback1(self, Hx,yr,eng1,eng2):
         N= 1
         maxN = max(self.lt, Hx.lt)
         X = Hx.IC - self.IC
         Y =  (self.OM[0] + self.AnnualEngCost(yr,eng1)) - (Hx.OM[0] + Hx.AnnualEngCost(yr,eng2))
         if X == 0 and Y >=0:
             return 0
         elif X == 0 and Y < 0:
             while N < maxN and Y <0 :
                Y = Y + (self.OM[N] + self.AnnualEngCost(yr+N,eng1)) - (Hx.OM[N] + Hx.AnnualEngCost(yr+N,eng2))
                N = N +1
             return N

         elif round(X/Y,0)==1:  #if X == Y
             return 1
         elif abs(X/Y) >1:
             while N < maxN and abs(X/Y) >1 :
                 Y = Y + (self.OM[N] + self.AnnualEngCost(yr+N,eng1)) - (Hx.OM[N] + Hx.AnnualEngCost(yr+N,eng2))
                 N = N +1
         #       print "INT", N, X/Y
         if N == maxN and (X/Y) > 1:
                 return maxN
         elif round(X/Y,0) == 1:
                return N
         else:
                 return N

class NGWH1(Device,object):
    def __init__(self, C,yr):
        super(NGWH1, self).__init__("NGWH", NG, NGWH_EF, 0,C, size1,size2, yr,  WH_LT, NGWHIC, OM_NG)

    def AnnualHeatEngUsage_BTU(self) :
        return super( NGWH1,self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)

class NGWH2(Device,object):
    def __init__(self, C,yr):
        super(NGWH2, self).__init__("NGWH", NG, NGWH_EF, 0,C, size1,size2, yr,   WH_LT, NGWHIC, OM_NG)

    def AnnualHeatEngUsage_BTU(self) :
        return super( NGWH2,self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)

class ERWH1(Device,object):
    def __init__(self, C,yr):
        super(ERWH1, self).__init__("ERWH", Elec, EL_EF, 0,C, size1,size2, yr,   WH_LT, ERWHIC, OM_EL)
      #  self.dailyVol = 50
       # self.IncTemp =75
    def AnnualHeatEngUsage_BTU(self):
        return super(ERWH1, self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)


class HPWH1(Device,object):
    def __init__(self, C,yr):
        super(HPWH1, self).__init__("HPWH", Elec, HPWH1_EF, 0,C, size1,size2, yr,  WH_LT, HPWHIC, OM_HP,True, Ref11 )

    def AnnualHeatEngUsage_BTU(self):
    #    print "HP Water Vol", self.dailyVol
        return super(HPWH1, self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)

class HPWH2(Device,object):
    def __init__(self,C,yr):
        super(HPWH2, self).__init__("HPWH", Elec, HPWH2_EF, 0,C, size1,size2, yr,  WH_LT, HPWHIC, OM_HP,True, Ref12 )
        self.dailyVol = 50
        self.IncTemp =75
    def AnnualHeatEngUsage_BTU(self):
        return super(HPWH2, self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)

class HPWH3(Device,object):
    def __init__(self, C,yr):
        super(HPWH3, self).__init__("HPWH", Elec, HPWH3_EF, 0,C, size1,size2, yr,  WH_LT, HPWHIC, OM_HP,True, Ref13 )
        self.dailyVol = 50
        self.IncTemp =75
    def AnnualHeatEngUsage_BTU(self):
        return super(HPWH3, self).AnnualWaterEngUsage(self.dailyVol, self.IncTemp)

class NGHeater0(Device, object):
    def __init__(self, C, s1,s2,r0,r1,r2, yr, cost=NGIC, is_retrofit = True, is_new = False):
        super(NGHeater0, self).__init__("NGH", NG, NG0_EF, 0,C, s1,s2, r0,r1,r2, yr,  NG_LT, cost, OM_NG)
        #self.r0 = R0val[C,ThisYear-15]  #window
        #self.r1 = R1val[C,vintage]  # wall
        #self.r2 = R2val[C,vintage]  # roof

    def AnnualHeatEngUsage_BTU(self):
        return super(NGHeater0, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class NGHeater1(Device, object):
    def __init__(self, C, s1,s2, r0,r1,r2,  yr, cost = NGIC, is_retrofit = True, is_new = False):
        super(NGHeater1, self).__init__("NGH", NG, NG1_EF, 0,C, s1,s2,r0,r1,r2,  yr,  NG_LT, cost, OM_NG)
        self.k1 = 1000
    def AnnualHeatEngUsage_BTU(self):
        return super(NGHeater1, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class NGHeater2(Device, object):
    def __init__(self, C,s1,s2,r0,r1,r2, yr, cost = NGIC, is_retrofit = True, is_new = False):
        super(NGHeater2, self).__init__("NGH", NG, NG2_EF,0, C, s1,s2,r0,r1,r2,  yr,  NG_LT, cost, OM_NG)
        self.k1 = 1000
    def AnnualHeatEngUsage_BTU(self):
        return super(NGHeater2, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class NGHeater3(Device, object):
    def __init__(self, C, s1,s2,r0,r1,r2, yr, cost = NGIC, is_retrofit = True, is_new = False):
        super(NGHeater3, self).__init__("NGH", NG, NG3_EF,0, C, s1,s2,r0,r1,r2,  yr,  NG_LT, cost, OM_NG)
        self.k1 = 1000
    def AnnualHeatEngUsage_BTU(self):
        return super(NGHeater3, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class ERHeater0(Device, object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ERIC, is_new= False):
        super(ERHeater0, self).__init__("ERH", Elec, E0_EF,0, C, s1,s2,r0,r1,r2,  yr,  EL_LT,cost, OM_EL, False)  # the false here is for Refrigerant
        self.k1 = 1000
    def AnnualHeatEngUsage_BTU(self):
        return super(ERHeater0, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class ERHeater1(Device, object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ERIC, is_new = False):
        super(ERHeater1, self).__init__("ERH", Elec, E_EF,0, C, s1,s2,r0,r1,r2,  yr,  EL_LT, cost, OM_EL, False)

    def AnnualHeatEngUsage_BTU(self):
        return super(ERHeater1, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class HP1(Device, object):
    def __init__(self, C, s1,s2,yr):
        super(HP1, self).__init__("HPH", Elec, HP1_EF, 0,C, s1,s2,r0,r1,r2,  yr,  HP_LT, HPIC1, OM_HP, True, Ref1)

    def AnnualHeatEngUsage_BTU(self):
        return super(HP1, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class HP2(Device, object):
    def __init__(self, C, s1,s2,yr):
        super(HP2, self).__init__("HPH", Elec, HP2_EF,0, C, s1,s2,r0,r1,r2,  yr,  HP_LT, HPIC2, OM_HP, True, Ref2)
#        self.k1= k1
    def AnnualHeatEngUsage_BTU(self):
        return super(HP2, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class HP3(Device, object):
    def __init__(self, C, s1,s2,yr):
        super(HP3, self).__init__("HPH", Elec, HP3_EF,0, C, s1,s2,r0,r1,r2,  yr,  HP_LT, HPIC3, OM_HP, True, Ref3)

    def AnnualHeatEngUsage_BTU(self):
        return super(HP3, self).AnnualHeatEngUsage_BTU()
    def heaterOnlyFunction(self):
        print "only works for heater"

class Cooler0(Device,object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ACIC, is_new = False):
        super(Cooler0, self).__init__("Cooler", Elec, 0,AC0_EF, C,s1,s2, r0,r1,r2, yr,  AC_LT, cost, OM_HP, True, Ref1)
      #  self.k = 1000
    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cooler0, self).AnnualCoolEngUsage_BTU()

class Cooler1(Device,object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ACIC, is_new = False):
        super(Cooler1, self).__init__("Cooler", Elec, 0,AC1_EF, C,s1,s2,r0,r1,r2,  yr,  AC_LT, cost, OM_HP, True, Ref1)
      #  self.k = 1000
    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cooler1, self).AnnualCoolEngUsage_BTU()
class Cooler2(Device,object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ACIC, is_new = False):
        super(Cooler2 ,self).__init__("Cooler", Elec, 0,AC2_EF, C,s1,s2,r0,r1,r2,  yr,  AC_LT, cost, OM_HP, True, Ref2)

    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cooler2, self).AnnualCoolEngUsage_BTU()

class Cooler3(Device,object):
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost = ACIC, is_new = False):
        super(Cooler3, self).__init__("Cooler", Elec, 0,AC3_EF,C,s1,s2, r0,r1,r2, yr,  AC_LT, cost, OM_HP, True, Ref3)

    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cooler3, self).AnnualCoolEngUsage_BTU()
#========================

#=====================
class Cond1(Device, object):  #assuming this is going to be all "ELectric" with no NG in it
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost=HPCapex1, is_retrofit=False, is_fuel_switch=False):
        self.cost = cost
        self.is_retrofit = is_retrofit  # if the cond is replacing Elec ER or NG
        self.is_fuel_switch = is_fuel_switch  # if switching from NG to Elec

        super(Cond1, self).__init__("Cond", Elec, HP1_EF,HP_AC1_EF, C, s1,s2,r0,r1,r2,  yr,  HP_LT, cost, OM_HPCond, True, Ref1)
        self.EF_Cool=self.ef
    def AnnualHeatEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond1, self).AnnualHeatEngUsage_BTU()
    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond1, self).AnnualCoolEngUsage_BTU()

    def AnnualTotalEngUsage_BTU(self):
        heatingenergy = self.AnnualHeatEngUsage_BTU()
        coolingenergy =  self.AnnualCoolEngUsage_BTU()
        totalenergy =    heatingenergy + coolingenergy
      #  print "test1", yr, totalenergy
        return totalenergy
    def annualTotalEngUsage_kWh(self):
         totalenergy = self.AnnualTotalEngUsage_BTU()
      #   print "test2",yr, totalenergy
         eng_kWh = totalenergy/kWh_BTU
         return eng_kWh
       #return super(HPCond, self).annualEngUsage()
    def heaterOnlyFunction(self):
        print "only works for heater"

class Cond2(Device, object):  #assuming this is going to be all "ELectric" with no NG in it
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost=HPCapex2, is_retrofit=False, is_fuel_switch=False):
        self.cost = cost
        self.is_retrofit = is_retrofit
        self.is_fuel_switch = is_fuel_switch

        super(Cond2, self).__init__("Cond", Elec, HP2_EF,HP_AC2_EF, C, s1,s2, r0,r1,r2, yr,  HP_LT, cost, OM_HPCond, True, Ref2)

    def AnnualHeatEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond2, self).AnnualHeatEngUsage_BTU()
    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond2, self).AnnualCoolEngUsage_BTU()

    def AnnualTotalEngUsage_BTU(self):
        heatingenergy = self.AnnualHeatEngUsage_BTU()
        coolingenergy =  self.AnnualCoolEngUsage_BTU()
        totalenergy =    heatingenergy + coolingenergy
      #  print "test1", yr, totalenergy
        return totalenergy
    def annualTotalEngUsage_kWh(self):
         totalenergy = self.AnnualTotalEngUsage_BTU()
         eng_kWh = totalenergy/kWh_BTU
         return eng_kWh

       #return super(HPCond, self).annualEngUsage()
    def heaterOnlyFunction(self):
        print "only works for heater"

class Cond3(Device, object):  #assuming this is going to be all "ELectric" with no NG in it
    def __init__(self, C, s1,s2,r0,r1,r2,yr, cost=HPCapex3, is_retrofit=False, is_fuel_switch=False):
        self.cost = cost
        self.is_retrofit = is_retrofit  # is the Cond replacing NG or Elec ER rather than another Cond
        self.is_fuel_switch = is_fuel_switch  # Gas to Elec?

        super(Cond3, self).__init__("Cond", Elec, HP3_EF,HP_AC3_EF ,C, s1,s2,r0,r1,r2,  yr,  HP_LT, cost, OM_HPCond, True, Ref3)

    def AnnualHeatEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond3, self).AnnualHeatEngUsage_BTU()
    def AnnualCoolEngUsage_BTU(self):
      #  print "cooling", self.AnnualCoolEnergyUsage_BTU()
        return super(Cond3, self).AnnualCoolEngUsage_BTU()

    def AnnualTotalEngUsage_BTU(self):
        heatingenergy = self.AnnualHeatEngUsage_BTU()
        coolingenergy =  self.AnnualCoolEngUsage_BTU()
        totalenergy =    heatingenergy + coolingenergy
      #  print "test1", yr, totalenergy
        return totalenergy
    def annualTotalEngUsage_kWh(self):
         totalenergy = self.AnnualTotalEngUsage_BTU()
         eng_kWh = totalenergy/kWh_BTU
         return eng_kWh

       #return super(HPCond, self).annualEngUsage()
    def heaterOnlyFunction(self):
        print "only works for heater"

def NGHeater(C, s1,s2, yr, cost, is_retrofit = False, is_new = False):
    if is_new == False:  #this is if the house is new
        r0 = R0present
        r1 = R1present
        r2 = R2present
        add_cost = 0
    else:
        r0 = R0future
        r1 = R1future
        r2 = R2future
        add_cost = NGNewHomeCost  # ## additional pipeline cost for new homes
   # print "NG TEST", s1,s2,yr, C, cz[C,yr].hdd, s1,s2,yr

    totalcost = cost + add_cost
    if yr < ThisYear:
        return NGHeater0(C, s1,s2, r0,r1,r2,yr, totalcost, is_retrofit, is_new)
    elif yr >=ThisYear and yr <= Phase11:
       return NGHeater1( C, s1,s2, r0,r1,r2,yr, totalcost, is_retrofit, is_new)
    elif yr > Phase11 and yr <= Phase2:
        return  NGHeater2(  C, s1,s2,r0,r1,r2, yr,totalcost, is_retrofit, is_new)
    else:
        return  NGHeater3(  C, s1,s2, r0,r1,r2,yr,totalcost, is_retrofit, is_new)

def ERHeater(C, s1,s2, yr,cost, is_new = False):
    if is_new == False:   # existing shell R values
        r0 = R0present
        r1 = R1present
        r2 = R2present
        add_cost = 0
    else:
        r0 = R0future    # future R values of shell
        r1 = R1future
        r2 = R2future
        add_cost = 0
   # print "NG TEST", s1,s2,yr, C, cz[C,yr].hdd, s1,s2,yr
    totalcost = cost + add_cost
    if yr < ThisYear-2:
        return ERHeater0(C, s1,s2,r0,r1,r2, yr, totalcost, is_new)
    else:
        return ERHeater1(  C, s1,s2, r0,r1,r2,yr,totalcost, is_new)

def HP(C, s1,s2, yr):
    if yr <= Phase1:
        return HP1( C, s1,s2, yr)
    elif yr > Phase1 and yr <= Phase2:
        return  HP2(  C, s1,s2, yr)
    else:
        return  HP3(  C, s1,s2, yr)

def Cooler(C, s1,s2, yr, cost, is_new = False):   #is_new == True means new home, false means retrofit
    if is_new == False:
        r0 = R0present
        r1 = R1present
        r2 = R2present
        add_cost =0
    else:            #
        r0 = R0future
        r1 = R1future
        r2 = R2future
        add_cost = HomeUpgradeCost
    totalcost = cost + add_cost

    if yr < ThisYear :
        return Cooler0(C,s1,s2,r0,r1,r2,yr, totalcost, is_new)
    elif yr >= ThisYear and yr <= Phase11:
        return Cooler1( C, s1,s2,r0,r1,r2, yr, totalcost, is_new)
    elif yr > Phase11 and yr <= Phase2:
        return  Cooler2(  C, s1,s2,r0,r1,r2, yr, totalcost, is_new)
    else:
        return  Cooler3(  C, s1,s2,r0,r1,r2, yr, totalcost, is_new)

def Cond(C, s1, s2, yr, cost, is_retrofit=False, is_fuel_switch=False,  is_new = False):
    cost_fuel_switch = 0
    cost1 =0
    if is_new == False: # not new home
        r0 = R0present
        r1 = R1present
        r2 = R2present
    else:               #new home....cost of HPConditioner
        r0 = R0future
        r1 = R1future
        r2 = R2future
    if is_retrofit ==True:  # ERH to HPCond for example
            cost1  = 0
    else:
            cost1 = 0
    if is_fuel_switch == True:
                cost_fuel_switch = FuelSwitchCost
    else:
                cost_fuel_switch = 0
  #  print "Cond R Values", r0,r1,r2
    if yr <=  Phase11:
          totalCost = HPCapex1 + cost1+ cost_fuel_switch
          return Cond1( C, s1,s2,r0,r1,r2,  yr, totalCost, is_retrofit, is_fuel_switch)
    elif yr > Phase11 and yr <= Phase2:
          totalCost = HPCapex2 + cost1+ cost_fuel_switch
          return Cond2(C, s1,s2,r0,r1,r2,  yr, totalCost, is_retrofit, is_fuel_switch)
    else:
          totalCost = HPCapex3 + cost1+ cost_fuel_switch
          return Cond3(C, s1,s2,r0,r1,r2,  yr, totalCost, is_retrofit, is_fuel_switch)

def HPWH(C,yr):
    if yr <= Phase1:
        return HPWH1( C,yr)
    elif yr > Phase1 and yr <= Phase2:
        return  HPWH2(  C,yr)
    else:
        return  HPWH3(  C,yr)

def NGWH(C,yr):
    if yr <= Phase1:
        return NGWH1( C,yr)
    elif yr > Phase1 and yr <= Phase2:
        return  NGWH2(  C,yr)
    else:
        return  NGWH3(  C,yr)

def ERWH(C,yr):
    if yr <= Phase1:
        return ERWH1( C,yr)
    elif yr > Phase1 and yr <= Phase2:
        return  ERWH1(  C,yr)
    else:
        return  ERWH1(  C,yr)
# #==============================================================================
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import *
# import matplotlib.patches as mpatches
# fig1 = plt.figure(figsize=(10.0, 8.0))
# a1 = fig1.add_subplot(1,1, 1)

# fig2 = plt.figure(figsize=(10.0, 8.0))
# a2 = fig2.add_subplot(1,1, 1)
# colors = [ 'orange', 'purple', 'g','blue',  'violet','k']
# cnt = 0
# this = 1980
# for yr0 in range(this,2050,10):
#    s=0
#    k= 3
#   # Heat = NGHeater(k,size1,size2 , yr0)  # a heater created every 10 years
#    Heat1 = Cooler(k,size1, size2, yr0)
#   # Heat2 = NGHeater(k,size1,size2, yr0)
#    dev1 = [Heat1]*1
#    for years in range(yr0,EndYear+5):
#        num = 0
#        for d in dev1:
#            num += 1
#            if d.vintage > years:  # heater not created
#                plot.hold(True)
#                plot.hold(True)
#                p = 0.0
#                dead1 = 1-d.deadsofar(years)  #actually live

#                a1.scatter(years , p,   s = 5, color = 'white')
#                a2.scatter(years , dead,   s = 5, color = 'red')
#            else:
#                p = d.death_prob(years) # prob of death ..once heater is created..
#                s = d.dead_alive(years)
#                dead = 1-d.deadsofar(years)

#                a1.scatter(years , p,   s = 5, color = 'red')
#                a2.scatter(years , dead,   s = 5, color ='green')
#            print "p",   years, d.vintage, d.death_prob(years), p, s

#    cnt +=1
# fig1.tight_layout()
# plt.show()
# fig2.tight_layout()
# plt.show()
###yr = ThisYear
#k = 3
##Stck = 100
## #
#devices = []
#devices += [ NGHeater(k,size1,size2, yr)]
##devices += [HPWH1(50,70,k)]
##devices += [HP1(k,size1,size2,yr)]
##
##waterEng = devices[1].AnnualHeatEngUsage_BTU()
##WHCost = devices[1].AnnualEngCost(yr,waterEng)
##WHEmis = devices[1].AnnEmissions(yr,waterEng)
##WHNPVEmis = devices[1].NPVEmissions(yr,waterEng)
###WHAnnEmis = devices[1].annualizedEmissions(yr,waterEng)
##
#SHEng = devices[0].AnnualHeatEngUsage_BTU()
#print "SH Stats", k, ThisYear, devices[0].lt,SHEng/Therm_BTU  #, SHCost, SHEmis, SHNPVEmis
##SHCost =devices[0].AnnualEngCost(yr,SHEng)
#SHEmis = devices[0].AnnEmissions(yr,SHEng)
#SHNPVEmis = devices[0].NPVEmissions(yr,SHEng)
#
#SHEng1 = devices[2].AnnualHeatEngUsage_BTU()
#SHCost1 =devices[2].AnnualEngCost(yr,SHEng1)
#SHEmis1 = devices[2].AnnEmissions(yr,SHEng1)
#SHNPVEmis1 = devices[2].NPVEmissions(yr,SHEng1)
##SHAnnEmis = devices[0].annualizedEmissions(yr,SHEng)
#print "WH Stats", k, ThisYear,devices[1].lt, waterEng//Therm_BTU, WHCost,WHEmis, WHNPVEmis

#print "HP SH Stats", k, ThisYear, devices[2].lt,SHEng1/kWh_BTU, SHCost1, SHEmis1, SHNPVEmis1

# cnt = len(devices)
#
# #for device in devices:
# #    for yrs in range(ThisYear, EndYear):
# #          print yrs, device.name, device.deadsofar(yrs), device.numAlive(yrs)
# #print size(devices)
#
# #for device in devices:
# #      print device.name, device.annualEngUsage(),device.AnnualEngCost(yr),device.AnnEmissions(yr),device.AnnTotalEmissions(yr) , device.annualizedEmissions(device.vintage)
#     # if (type(device) == Heater):
#     #     device.heaterOnlyFunction()
#k = 3
## yr = ThisYear
## vintage = yr
## Stck = 1
## #print "I", size1, size2, cz[C,vintage].hdd, cz[C, vintage].cdd, R1val[C], R2val[C]
###


#import matplotlib.pyplot as plt
#from matplotlib.pyplot import *
#import matplotlib.patches as mpatches
##fig = plt.figure(figsize=(10.0, 8.0))
##axes1 = fig.add_subplot(1,1, 1)
#====================================================
#print "eng", C, yr, eng1
#print "emis", SHeater.AnnEmissions(yr, eng1), SHeater.AnnTotalEmissions(yr, eng1), SHeater.AvgRefLeaks(yr)
#print "I", NG_EF, size1, size2, cz[C,vintage].hdd, cz[C, vintage].cdd, R1val[C], R2val[C]
#print "df1", SHeater.name, SHeater.annualEngUsage(), SHeater.AnnualEngCost(2020), SHeater.AnnEmissions(2020) #

#SHeater =Device("NG", NG, NG_EF, C, size1,size2, yr, Stck, NG_LT, NGIC, OM_NG, False)

#SCond = HPCond(C, size1, size2, yr, Stck)
#print "SpaceConditioner", yr, C, SCond.AnnualCoolingEngUsage_BTU(), SCond.AnnualHeatingEngUsage_BTU()


#print "II", NG_EF, size1, size2, cz[C,vintage].hdd, cz[C, vintage].cdd, R1val[C], R2val[C]
#print "df2", SHeater.name, SHeater.annualEngUsage(), SHeater.AnnualEngCost(yr), SHeater.AnnEmissions(yr)
