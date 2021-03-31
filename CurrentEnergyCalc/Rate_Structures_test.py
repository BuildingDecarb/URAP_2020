#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ann_inflation = 0.03  #
years = 10 


SeasonDict = {1: 'Winter', 2: 'Winter', 3: 'Winter', 4: 'Winter', 5: 'Winter', 6: 'Summer', 7: 'Summer',
                     8: 'Summer', 9: 'Summer', 10: 'Winter', 11: 'Winter', 12: 'Winter'}  

month_indices = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6,
                     'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}


month_names= {0:'January', 1:'February', 2:'March', 3: 'April', 4: 'May', 5: 'June', 6: 'July',
                     7: 'August', 8:'September', 9: 'October', 10:'November', 11: 'December' }# reversed

beg = [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016] #hr of the.first day of month
end = [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760] #hr of the..last day of month
#leapYear = [744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040, 8784] #hr of for leap years


class Rate_A:                        #Currently PGE_E_C (https://www.pge.com/tariffs/electric.shtml)
    def __init__(self,name):        #baseline credit allowance for PGE- territory R - which is southern SJValley
        self.name = name        

  
    def peakDays(self):
        return [0, 1, 2, 3, 4]
  
    def offPeakDays(self):
        return [5, 6]    #Weekend
  
    def peakHours(self):   
        return [ 16, 17, 18, 19, 20]
  
    def offPeakHours(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,21, 22,  23]
#______BELOW PGE Residential E-TOU_E..............
  
    def monthlyBaseAmt(self,monthName,cumdem): # fixed customer cost
        dailyMinBillAmt = 0.32854  # fixed cost for a day
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/24   # computing number of days for the month
       # print "test month_days", monthName,month_days
        return dailyMinBillAmt * month_days           # ~fixed cost


    def summer_basicElec(self):  #daily allowance
        return   8.2 # 18.6             #kWh/day

    def winter_basicElec(self):
        return  6.8 # 11.3           #kWh/day

    def summer_AllElec(self):
        return 7.5  #20.9             #kWh/day

    def winter_AllElec(self):
        return  13.6 # 28.1           #kWh/day

    def dailybaseline_Allowance(self,season,elec='base'):
        if elec == 'base':
            if season == 'Summer':
                return self.summer_basicElec()
            else:
                return self.winter_basicElec()
        else:
            if season == 'Summer':
                return self.summer_AllElec()
            else:
                return self.winter_AllElec()
                   

        
    def baselineAllowance(self,monthName,season, cumdem, elec='base'):  #

        basecredit = 0.07  # $/kWh
        dailyAllowance = self.dailybaseline_Allowance(season,elec)
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/24
        monthlyAllowance = month_days * dailyAllowance
      #  print ("baseline allow", monthName, season,month_days, dailyAllowance, monthlyAllowance * basecredit)
        return basecredit * monthlyAllowance          # ~fixed cost

  

    def feedInTariff(self):    #SOLAR excess generation fed into the ground
        return 0.05
    
    def summerPeakRate(self):
        return 0.41418   #$/kWh
   
    def summerOffPeakRate(self):
        return 0.31112
   
    def winterPeakRate(self):
        return 0.32104

    def winterOffPeakRate(self):
        return 0.30372

    def findRate(self,season, day, time, cumdem):

        if (time in self.peakHours()) and (day in self.peakDays()):
                if season == 'Winter':
                        rate = self.winterPeakRate()
                if season == 'Summer': 
                        rate = self.summerPeakRate()
                   
        elif (time in self.peakHours()) and (day in self.offPeakDays()):
                if season == 'Winter':
                    rate = self.winterPeakRate()
                if season == 'Summer': 
                        rate = self.summerPeakRate()
                   
        elif (time in self.offPeakHours()) and (day in self.offPeakDays()):
                if season == 'Winter':
                    rate = self.winterOffPeakRate()
                if season == 'Summer': 
                    rate = self.summerOffPeakRate()
            
        else:
                if season == 'Winter':
                    rate = self.winterOffPeakRate()
                if season == 'Summer': 
                    rate = self.summerOffPeakRate()
        #print "season rate", season, day, time, rate       
        return rate

#PGE_E_TOU_D ++both for summer and winter


class Rate_B(Rate_A):
    def __init__(self,name):
        self.name = name        
 

    def peakHours(self):   
        return [  17, 18, 19, 20]
  
    def offPeakHours(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,16,21, 22,  23]


    def baselineAllowance(self,monthName,season, cumdem, elec='base'):  #

        return 0


    def feedInTariff(self):    #SOLAR excess generation fed into the ground
        return 0.05
 
    def summerPeakRate(self):
        return 0.37644

    def summerOffPeakRate(self):
        return 0.28148

    def winterPeakRate(self):
        return 0.30257

    def winterOffPeakRate(self):
        return 0.28519

#==========================================================================

class Rate_SCE(Rate_A):  #SCE TOU-D_4_9 (Equiv to PGE -E-C)
    def __init__(self,name):
        self.name = name        

    
    def peakHours(self):
        return [ 16, 17, 18, 19, 20, 21]

    def offPeakHour(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,  22,  23]
  
    
#=====the multiplicative factor for computing PV of cost over num_years at inflation===#


class Rate_SCE(Rate_A):
    def __init__(self,name):
        self.name = name     


    def monthlyBaseAmt(self,monthName,cumdem): # fixed customer cost
        dailyMinBillAmt = 0.03  # fixed cost for a day
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/24   # computing number of days for the month
       # print "test month_days", monthName,month_days
        return dailyMinBillAmt * month_days           # ~fixed cost


    def summer_basicElec(self):  #daily allowance
        return 18.6             #kWh/day

    def winter_basicElec(self):
        return 11.3           #kWh/day

    def summer_AllElec(self):
        return 20.9             #kWh/day

    def winter_AllElec(self):
        return 28.1           #kWh/day

    def dailybaseline_Allowance(self,season,elec='base'):
        if 'elec' == 'base':
            if season == 'summer':
                return self.summer_basicElec()
            else:
                return self.winter_basicElec()
        else:
            if season == 'summer':
                return self.summer_AllElec()
            else:
                return self.winter_AllElec()
                   

        
    def baselineAllowance(self,monthName,season, cumdem, elec='base'):  #

        basecredit = 0.07  # $/kWh
        dailyAllowance = self.dailybaseline_Allowance(season,elec)
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/24
        monthlyAllowance = month_days * dailyAllowance
      
        return basecredit * monthlyAllowance          # ~fixed cost

  

    def feedInTariff(self):    #SOLAR excess generation fed into the ground
        return 0.05
    
    def summerPeakRate(self):
        return 0.43   #$/kWh
   
    def summerOffPeakRate(self):
        return 0.27
   
    def winterPeakRate(self):
        return 0.32104

    def winterOffPeakRate(self):
        return 0.27




def npv_cost(inflation, num_years, cost):
    npv = np.pv(inflation, num_years, -cost)
    return npv


#npv = npv_rate(ann_inflation, years,1)
#print ("npv_Rate", npv)


#===========Turlock IRrigation Rate Structure ========================
class rate_TID:
    def __init__(self,name):
        self.name = name        

 
    def peakDays(self):
        return [0, 1, 2, 3, 4]

    def offPeakDays(self):
        return [5, 6]    #Weekend

    def peakHours(self):   
        return [ 16, 17, 18, 19, 20]

    def offPeakHours(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,21, 22,  23]


    def winterPeakRate(self, cumdem):
        if cumdem <= 700:
            return 0.1016
        else:
            return 0.1116

 
    def winterOffPeakRate(self, cumdem):
        if cumdem <= 700:
            return 0.1016
        else:
            return 0.1116    

    def summerPeakRate(self,cumdem):
        if cumdem <= 700:
            return 0.1070
        elif 700 < cumdem <= 1100:
            return 0.1305
        else:
            return 0.1436        
        

    def summerOffPeakRate(self,cumdem):
        if cumdem <= 700:
            return 0.1070
        elif 700 < cumdem <= 1100:
            return 0.1305
        else:
            return 0.1436


    def feedInTariff(self):
        return 0.03


    def monthlyBaseAmt(self, monthName, cumdem):
       fixedCost =  17
       env_charge = 0.0269* cumdem
       monthlycost = fixedCost + env_charge
       return monthlycost

    def baselineCredit(self,monthName, cumdem):
        credit = 0.005 * cumdem
        return credit


    def findRate(self, season, day, time,  cumdem):  #TID Rate - tiered rate structure
        print "peak hours", self.peakHours()
        if (time in self.peakHours()) and (day in self.peakDays()):
                if season == 'Winter':
                        rate = self.winterPeakRate(cumdem)
                if season == 'Summer': 
                        rate = self.summerPeakRate(cumdem)
                   
        elif (time in self.peakHours()) and (day in self.offPeakDays()):
                if season == 'Winter':
                    rate = self.winterPeakRate(cumdem)
                if season == 'Summer': 
                        rate = self.summerPeakRate(cumdem)
                   
        elif (time in self.offPeakHours()) and (day in self.offPeakDays()):
                if season == 'Winter':
                    rate = self.winterOffPeakRate(cumdem)
                if season == 'Summer': 
                    rate = self.summerOffPeakRate(cumdem)
            
        else:
                if season == 'Winter':
                    rate = self.winterOffPeakRate(cumdem)
                if season == 'Summer': 
                    rate = self.summerOffPeakRate(cumdem)
        #print "season rate", season, day, time, rate       
        return rate

    
