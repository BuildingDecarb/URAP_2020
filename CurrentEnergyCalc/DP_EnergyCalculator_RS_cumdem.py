#!/usr/bin/env python
# coding: utf-8

# In[1]:
#Anagha Mandayam's code

###===============================================

#IMPORTS
import csv
import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from Rate_Structures_test import *


# In[2]:
#===========================================================================================

class House:
    #dataframe = hourly energy loads or any dataframe that you would like to pass int
    #date = your startday: 1st day of the hourly hours
    def __init__(self, dataframe, date): 
        self.dataframe = dataframe  
        self.date = date
        
# Instance Methods
    def dateSeason(self):
    #Descritpion: returns date array and season array      
        date_index = []
        season_index = []

        for i in range(len(self.dataframe)):
            new_date = self.date + datetime.timedelta(hours = i)
            date_index.append(new_date)
            season = SeasonDict.get(new_date.month)
            season_index.append(season)
        return date_index, season_index
    
    def getDateDf(self):
    #Descritpion: returns an hourly dataframe with an added date column
        d, s = self.dateSeason()
      #  print "dframe", self.dataframe
        dframe = self.dataframe.copy()
        dframe.insert(0, 'Date', d)
        dframe.insert(1, 'Season', s)
        return dframe


### all hourly energy demand columns captured
    def getAllDataDf(self):
        df = self.getDateDf()

        df['total'] = df['base']
        if 'SH' in df.columns:
            df['total'] += df['SH']
        if 'WH' in df.columns:
            df['total'] += df['WH']
              
        return df        
               
########################            
    
    def getMonthDf(self, monthName):
    #Description: returns a dataframe with all the values for only the month passed in. 
    # Ex: passing in January gives the first 744 rows for that month
        if 'Date' in self.dataframe.columns:
            dframe = self.dataframe   
        else:
            dframe = self.getAllDataDf()        


        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        #print ("results of getMonthDF  ", monthName, dframe[monthBeg: monthEnd])
        return dframe[monthBeg: monthEnd]
    
    def getSeasonDf(self, seasonName): 
    #Description: returns a dataframe for the season passed in.
    # Winter defined as Jan - April, Nov - Dec
    # Summer defined as May - October
        jan = self.getMonthDf('January')
        feb = self.getMonthDf('February')
        mar = self.getMonthDf('March')
        apr = self.getMonthDf('April')
        may = self.getMonthDf('May')
        jun = self.getMonthDf('June')
        jul = self.getMonthDf('July')
        aug = self.getMonthDf('August')
        sept = self.getMonthDf('September')
        octo = self.getMonthDf('October')
        nov = self.getMonthDf('November')
        dec = self.getMonthDf('December')
        
        if seasonName == 'Winter':
            months = [jan, feb, mar, apr, nov, dec]
        elif seasonName == 'Summer': 
            months = [may, jun, jul, aug, sept, octo]    
        return pd.concat(months)
    
    def selectColumnDf(self, cool, base, sh, wh, pv):
    #Description: returns a dataframe with certain columns 
    # Ex: passing in TRUE, FALSE, TRUE, TRUE gives you a dataframe with base, cool, sh and wh
        if 'Date' in self.dataframe.columns:
            dframe = self.dataframe
        else:
            dframe = self.getAllDataDf()
            
        if cool == False:
            dframe.drop('cooling', inplace = True, axis = 1)
        if base == False:
            dframe.drop('base', inplace = True, axis = 1)
        if sh == False:
            dframe.drop('SH', inplace = True, axis = 1)
        if wh == False:
            dframe.drop('WH', inplace = True, axis = 1)
        if pv == False:
            dframe.drop('PV', inplace = True, axis = 1)          
      
        return dframe

    #Shuba.edits incomplete...error check!!
    

def getMax(dframe, enduse):  #get the max demand and date for an end-use for a certain timeframe
       
        df_enduse = dframe[enduse]
        max_enduse = df_enduse.max()
        idmax = dframe[enduse].idxmax()
        hr_max = dframe.loc[idmax,'Date']
       # print ("max...", enduse, max_enduse, idmax,hr_max)
        return max_enduse, hr_max

#outputs DF with 'enduse' demand above the threashold
def getAboveThresholdDF(dframe, enduse, threshold):
     # df_enduse = dframe[enduse]
      df_new = dframe[dframe[enduse]>threshold]
      total_highdemand = df_new[enduse].sum()
     
      num_hrs = len(df_new)
   #   print("total_highdemand", num_hrs, total_highdemand)
      return df_new, num_hrs

#### returns monthly energy  cost - given month name, dataframe and rate structure 

def getMonthlyEnergyCost(month,data,rs):
    index = month_indices.get(month)
    monthBeg = beg[index]
    monthEnd = end[index]
    dates = data['Date'].tolist()
    seasons = data['Season'].tolist()
    hourlyRate= []
    gridDemand = []
   
    net_elec = []   #only to compute cost: electricity either hours when you pay or get paid (this is +ve if grid supplies and -ve if excess PVGen fed into the grid
    cum_demand = 0
    cum_excessGen = 0
    cum_selfConsump = 0
    cumPVGen = 0
    cum_NEM_Income = 0.0   # Net metering income...excess generation fed into the grid earns FeedInTariff
    for i in range(monthBeg, monthEnd):
        
            time = i%24
            day = dates[i-monthBeg].weekday()
            season = seasons[i-monthBeg]
          
             # function defined in Rate_Structure1.py
      #     print "netdata", data["nettotal"]
            cum_demand +=  data['total'][i]
            if ('PV' in data.columns):
                if (data['PV'][i] >=0):
                    cumPVGen += data['PV'][i] #PV Generation, net metering income for every hour
                    if (data['PV'][i] >= data['total'][i]):
                        excessGen = (data['PV'][i] - data['total'][i])
                        cum_excessGen += excessGen
                        net_elec.append(-excessGen)
                        cum_selfConsump += data['total'][i]
                        gridDemand.append(0)        # as self PV Gen > total ..self consuming
                        nem = rs.feedInTariff()
                        hourlyRate.append(nem)
                        cum_NEM_Income  += excessGen * nem            
                    else:
                        grid_consump = data['total'][i] - data['PV'][i]
                        cum_selfConsump += data['PV'][i]
                        gridDemand.append(grid_consump)
                        net_elec.append(grid_consump)
                        rate = rs.findRate(season,day, time, cum_demand)  #
                        hourlyRate.append(rate)
            else:
                 gridDemand.append(data['total'][i])
                 net_elec.append(data['total'][i])
                 rate = rs.findRate(season,day, time, cum_demand)  #
                 hourlyRate.append(rate)
    
    TotalNetDemand = sum(gridDemand)
   # print "test", hourlyRate  #, gridDemand, net_elec

    cost = np.dot(hourlyRate,net_elec)   #net_elec will be -ve when feeding the grid, else +ve..
  #  print "cost, netdemand : ", cost, cumPVGen,cum_excessGen,cum_selfConsump, TotalNetDemand, cum_demand

      
    monthlyfixedCost= rs.monthlyBaseAmt(month,cum_demand)
    monthcredit = rs.baselineAllowance(month,season, cum_demand, 'base')
    EnergyCharge = cost.sum()
    
    totalcost = EnergyCharge +monthlyfixedCost - monthcredit

    
    
  #  print('For ', month,  ': Energy dem & cost ',  TotalNetDemand,cum_excessGen, "totalCost($)=",  round(monthlyfixedCost,2),round(monthcredit,2), round(totalcost,2))
    return  cum_demand, TotalNetDemand,cumPVGen, cum_excessGen, cum_NEM_Income, monthlyfixedCost, monthcredit, EnergyCharge,totalcost


# Calls the Monthly Annual Energy function abo,ve and saves results in file and returns value
def getAnnualEnergyCost_cumdem(house,rate_str, cnt):
    df = house.getAllDataDf()  #this inserts 'date, season and all energy columns' to the datafram
    
    if 'Date' in df.columns:
        data = df.copy()
    else:
        data = house.getAllDataDf()
    
    thismonth = []    
  
    totalConsumption = []
    totalnetDemand = []
    totalPVGen = []
    excess_PVGen = []
    NEM_Income = []
    
    fixedCost = []
    credit = []
    energyCharge = []
    totalcost = []
  
    
    for i in range(0,12):
        data = house.getMonthDf( month_names[i])        # month dataframe..returns dframe indexed with indices of original dataframe
   #     print "MONTH..:", i, month_names[i] , data
        result = getMonthlyEnergyCost(month_names[i], data, rate_str)
        
        thismonth.append(month_names[i])
        totalConsumption.append(result[0])
        totalnetDemand.append(result[1])
        totalPVGen.append(result[2])
        excess_PVGen.append(result[3])
        NEM_Income.append(result[4])

        fixedCost.append(result[5])
        credit.append(result[6])
        energyCharge.append(result[7])
        totalcost.append(result[8])
       
        
    results_df = pd.DataFrame(data={'Month': thismonth,                                   
                                        'TotalConsumption': totalConsumption,
                                        'NetDemand':   totalnetDemand,
                                        'TotalPVGen': totalPVGen,
                                        'excess_PVGen': excess_PVGen,
                                        'NEM_Income':  NEM_Income,
                                        'Fixed_Cost': fixedCost,
                                        'Baseline_Credit': credit,
                                        'Energy_Charge': energyCharge,
                                         'Energy_Cost': totalcost
                                        })
    name = str(rate_str.name)
    cnt = str(cnt)
    results_df.to_csv(   'DPY_3SizedUsers_PGE_Terr_T '  + name+ "_"+cnt +'_Base.csv')  #
    
  #  print "\n Total Annual Energy & Cost are ", sum(totalConsumption), sum(totalengcost)
    return results_df  






