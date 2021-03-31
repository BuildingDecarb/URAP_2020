#!/usr/bin/env python
# coding: utf-8

# In[1]:
#Anagha Mandayam's code
###=============================
## Shuba's edits Jan 2, 2022
##  0. Made month and season arrays global variables. error in
#######    Rate_Structures.py has rate structure designs
######



## 
#### Could you pl. Add plots for monthly average - one random weekday, weekday for every month, 


##   THIS can come later...no rush
## CAN YOU please WRITE A FUNCTION TO OUTOUT THE NUMBER OF 'EVENTS' (CONTINUOS 3-4 HOURS) WHERE
## THE DEMAND OF AN END=USE (BASE OR COOLING OR HEATING) IS ABOVE A CERTAIN THRESHOLD
## A SERIES OF FUNCTIONS CAN OUTPUT- SEVERAL INFO # OF TIMESLOTS, TOTAL HOURS, AVERAGE HOURLY DEMAND DURING THESE HIGH USAGE
## PERIODS, TOTAL DEMAND AND SO ON
## >>>THIS CAN CALL THE FUNCTION GETABOVETHRESHOLDDF
###===============================================

#IMPORTS
import csv
import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from Rate_Structures1 import *


# In[2]:
#===========================================================================================
#Shuba's reading files  # 'elec' files have 2 extra hourly loads for Space and Water heating (2 extra colummns of data than the 'base' versions)
##folder = 'TestProfiles_perHH'
##results_folder = folder + "/" + 'Results'
##
##filename =  'pge-res-PGF1-res_misc-noKW-nonCare-0.3_0.4_SHWHPV' #change to appropriate filename WITHOUT .csv tag
###filename=  'pge-res-PGF1-res_misc-noKW-nonCare-0.5_0.6_SHWHPV' #change to appropriate filename WITHOUT .csv tag
###filename=  'pge-res-PGF1-res_misc-noKW-nonCare-0.7_0.8_SHWHPV' #change to appropriate filename WITHOUT .csv tag
###filename=  'pge-res-PGF1-res_misc-noKW-nonCare-0.8_0.9_SHWHPV' #change to appropriate filename WITHOUT .csv tag
##
##
####filename=  'sce-res-SCEN-res_misc-noKW-nonCare-0.3_0.4_SHWHPV' #change to appropriate filename WITHOUT .csv tag
###filename=  'sce-res-SCEN-res_misc-noKW-nonCare-0.5_0.6_SHWHPV' #change to appropriate filename WITHOUT .csv tag
####filename=  'sce-res-SCEN-res_misc-noKW-nonCare-0.7_0.8_SHWHPV' #change to appropriate filename WITHOUT .csv tag
####filename =  'sce-res-SCEN-res_misc-noKW-nonCare-0.9_1.0_SHWHPV' #change to appropriate filename WITHOUT .csv tag
####sub = filename[8:12]
####care = filename[27:-8] #care or nonCare
####length = len(filename)
####decile = filename[length-7:]
##
###filename = 'MPT_TID_Data'
##
#### The data of interest in this run of the code:
##
##
##
##thisfile = folder + "/" + filename+ '.csv'
###
##df = pd.read_csv(thisfile, usecols=['base','SH','WH','PV'])      #- base load includes cooling
###df = pd.read_csv(thisfile, usecols=['cooling','base','SH','WH'])  #electrified
###df = pd.read_csv(thisfile, usecols=['cooling','base','SH','WH', 'PV'])  #electrified + Solar PV
##
##
###df = pd.read_csv(thisfile, usecols=['base'])                #MPT  base load includes cooling
###df = pd.read_csv(thisfile, usecols=['base', 'SH','WH'])      #MPT elec- base load includes cooling
##

#Seasons -months defined in Rate STructure

month_indices = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6,
                     'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}


month_names= {0:'January', 1:'February', 2:'March', 3: 'April', 4: 'May', 5: 'June', 6: 'July',
                     7: 'August', 8:'September', 9: 'October', 10:'November', 11: 'December' }# reversed

beg = [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016] #first day of month
end = [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760] #last day of month
#leapYear = [744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040, 8784] #for leap years


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
        #print(df)
       
        df['total'] = df['base']
        if 'SH' in df.columns:
            df['total'] += df['SH']
        if 'WH' in df.columns:
            df['total'] += df['WH']
        if 'PV' in df.columns:
            df['nettotal'] =df['total'] - df['PV']
        else:
            df['nettotal'] = df['total']
         
        return df        
               


######################################
    #Shubas note INPUT? Not used?..not clear as well
    def getHourlyDf(self):
    #Description: returns a dataframe with all the values for only the certian time passed. 
    # Ex: passing in 0 gives the 0, 24, 48, etc. values which is at midnight each day
        if 'Date' in self.dataframe.columns:
            dframe = self.dataframe
            
        else:
            dframe = self.getDateDf()          
        time = self.getTime()
        if time < 24:
            return dframe.iloc[time::24, :]
        else: 
            print('Invalid time parameter')

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
    cum_demand = 0  #cumulative Net demand after self consumption from PV
    cum_excessGen = 0
    cum_NEM_Income = 0.0
    cumPVGen = []# Net metering income...excess generation fed into the grid earns FeedInTariff
    for i in range(monthBeg, monthEnd):

            time = i%24
            day = dates[i-monthBeg].weekday()
            season = seasons[i-monthBeg]       
             # function defined in Rate_Structure1.py
             
            data = data.reset_index(drop = True)
            ##print(data)
            array = []
            for j in range(monthBeg, monthEnd):
                array.append(j)
                 ##set each index to a speciic value
            data["hours"] = array
            data = data.set_index("hours")
           
            
            if 'PV' in data.columns and data['PV'][i] >=0:
                cumPVGen += data['PV'][i]                        #PV Generation, net metering income for every hour 
                
           # data = data.reset_index(drop = True)
           
           
           
            
      
            
        
         
            if data['nettotal'][i] >= 0:
               
                cum_demand +=  data['nettotal'][i]
                rate = findRate(season,day, time,rs)  #
                hourlyRate.append(rate)
      
            if data['nettotal'][i] < 0 and  'PV' in data.columns:
                nem = rs.feedInTariff()   #for now fixed feed in tariff defined in Rate structure
                hourlyRate.append(nem)
                cum_excessGen -= data['nettotal'][i]  #This is will be -ve
                cum_NEM_Income -= data['nettotal'][i] * nem
           
           # print "cum demand.",i, rate, data['Date'][i],   data['total'][i],
           
           
           
   

           
    cost = data['nettotal'] * hourlyRate #a vector of hourly cost of energy, if nettotal is >0, you are paying, if <0, you are paid NEM

    
    
    
    max_dem = data['nettotal'].max()

    monthlybaseAmt= rs.monthlyBaseAmt(month)
    monthcredit = rs.baselineCredit(month)
    totalcost = cost.sum() +monthlybaseAmt - monthcredit 
    
    TotalConsumption = data['total'].sum()
    TotalNetDemand = data['nettotal'].sum()
   # print('For ', month,  ': Energy dem & cost ',  TotalConsumption,TotalNetDemand, '$', monthlybaseAmt, monthcredit,cum_NEM_Income ,"totalCost=", str(round(totalcost.sum(),2)))
    return  TotalConsumption, TotalNetDemand, totalcost
 


# Calls the Monthly Annual Energy function above and saves results in file and returns value
def getAnnualEnergyCost(house,rate_str):
    
    df = house.getAllDataDf()  #this inserts 'date, season and all energy columns' to the datafram
    
    
    if 'Date' in df.columns:
        data = df.copy()
    else:
        data = house.getAllDataDf()

    thismonth = []    
    engcost = []
    fixedcost = []
    totalnetDemand = []

    PVGen = []
    excess_PVGen = []
    totalConsumption = []
    avg_unitCost = []
    for i in range(0,12):
        data = house.getMonthDf( month_names[i])
       
        
        
               # month dataframe..returns dframe indexed with indices of original dataframe
    #    print "MONTH..:", i, month_names[i] , data
        result = getMonthlyEnergyCost(month_names[i], data, rate_str)
        thismonth.append(month_names[i])
       
        totalConsumption.append(result[0])
        engcost.append(result[1])
       
        
    results_df = pd.DataFrame(data={'Month': thismonth,
                                        
                                        'TotalConsumption (kWh)': totalConsumption,
                                         'Energy Cost ($)': engcost
                                        })
    results_df.to_csv(   'DPY_March2_2021' +'.csv')  #
    
 #   print "\n Total Annual Energy & Cost are ", sum(totalConsumption), sum(engcost)
    return sum(totalConsumption),  sum(engcost)






