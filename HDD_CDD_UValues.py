# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:22:53 2018
@author: shubaraghavan
"""
from Inputs import *
import xlrd
# Read in UValues for buildings (walls, roof and windows) and Inc Temp for water heater
class climatezone:
    def __init__(self,num,hdd,cdd, IncTemp, HHsize,HHGrowthRate, HHShare):
        self.num = num # integer 1 -16 denoting climate zone
        self.hdd = hdd   #heating degree days
        self.cdd = cdd   #cooling degree days
        self.IncTemp = IncTemp #the delta of outlet to inlet temp for hot water.
        self.dailyVol = 50
        self.HHsize = HHsize  # Number of households in CZ as % of state
        self.HHGrowthRate = HHGrowthRate
        self.HHShare = HHShare  #for now SF and MF
    
workbook = xlrd.open_workbook('HDD_CDD_CA.xlsx')
sheet_name = workbook.sheet_names()
HDD_CDD = workbook.sheet_by_name(sheet_name[0])  # HDD and CDD and population
housedata = workbook.sheet_by_name(sheet_name[2]) #HouseSpecs
AppSaturation = workbook.sheet_by_name(sheet_name[3])
HH_withHeat = {}  #heating saturation global var
HH_withCool = {}  # cooling saturation global var
cz = {}

VacancyRate = 0 # housedata.cell(7,3).value  # as of 1/1/2015   
NumHHTotal =  housedata.cell(6,3).value   # 13.9 Million 0 #s households as of1/1/2016
DiscRate = 0.04

SFH = 1 #.58    # *NumHH Single fam- 
#MFH = (1.0-SFH)   #  * NumHH  Multi fam
MFScale_H = 1 #0.77  # 0.58/.75  for NG heating from RASS
MFScale_C = 1 # 0.83  #0.58/.70   for central heating from Rass
###===============================================================================
#SFH = share of SF Homes, if 1.0 is the SF energy value then 0,42 is the energy value of MF
#MFScale scales the Total state energy (assuming all SF homes) to including MF homes
#=================================================================================================
NumHH = NumHHTotal * (1-VacancyRate)
NumHH = int(NumHH)
HHThisYear = NumHH
NumHHCZ = {}
hhShare = {}

#right now this is fixe
for i in range (1, Numcz+1):

    hdd = HDD_CDD.cell(1+i,1).value
    cdd = HDD_CDD.cell(1+i,5).value
    hdd_EndYear = HDD_CDD.cell(1+i,2).value
    cdd_EndYear = HDD_CDD.cell(1+i,6).value
    IncTemp       = housedata.cell(11+i,10).value
    hhsize_thisyear = housedata.cell(11+i,3).value             #* NumHH in millions in each CZ.
    growthrate =  housedata.cell(11+i,4).value
    hhShare["SF", ThisYear] = 1.0  #   ALL SF homes for now
  #  hhShare["MF",ThisYear] =  1.0 - hhShare["SF",ThisYear] 
    hddchangeRate = HDD_CDD.cell(1+i,3).value
    cddchangeRate =  HDD_CDD.cell(1+i,7).value
      # print "CHANGE", ThisYear, EndYear,hdd_EndYear, cdd_EndYear, R0val[i,ThisYear] ,R1val[i,ThisYear] ,R2val[i,ThisYear]  
    HH_withHeat[i,ThisYear] =   AppSaturation.cell(4+i,2).value  #% of houses with heating
    HH_withCool[i,ThisYear] = AppSaturation.cell(4+i,3).value   # Cooling saturation
    
    heatSaturationInc =  AppSaturation.cell(4+i,6).value    #annual increase in heating applinance saturation in a specific climate zone
    coolSaturationInc =  AppSaturation.cell(4+i,7).value    #annual increase in cooling saturation in a climate zone    
    hhsize_last = hhsize_thisyear
    cz[i,PastYear]= climatezone( i,hdd, cdd, IncTemp, hhsize_thisyear,growthrate, hhShare)
    #print "test cz",i,  cz[i,PastYear].HHsize/10**6, HH_withHeat[i,ThisYear], HH_withCool[i,ThisYear]

    for yr in range(PastYear-30,ThisYear-40):    
       Thishhsize =  hhsize_thisyear  
       hhShare["SF",yr] = SFH
   #    hhShare["MF", yr] = 1.0 - hhShare["SF",yr]  
       HH_withHeat[i,yr] = HH_withHeat[i,ThisYear]
       HH_withCool[i,yr]  =HH_withCool[i,ThisYear]
       cz[i,yr ] = climatezone( i,hdd, cdd, IncTemp, hhsize_thisyear,growthrate, hhShare)
   # print "past values", i, yr, cz[i,yr].HHShare["SF",yr]* Thishhsize, cz[i,yr].hdd, cz[i,yr].cdd, 1.0/R0val[i,yr], 1.0/R1val[i,yr], 1.0/R2val[i,yr]
    for yr in range(ThisYear -40,ThisYear-19):    #upto 2000
       Thishhsize =  hhsize_thisyear  
       hhShare["SF",yr] = SFH
  #     hhShare["MF", yr] = 1.0 - hhShare["SF",yr]  
       HH_withHeat[i,yr] = HH_withHeat[i,ThisYear]
       HH_withCool[i,yr]  =HH_withCool[i,ThisYear]  
       cz[i,yr ] = climatezone( i,hdd, cdd, IncTemp, hhsize_thisyear,growthrate, hhShare)
   
    for yr in range(ThisYear -19,ThisYear):     #2010 to be included
       Thishhsize =  hhsize_thisyear  
       hhShare["SF",yr] = SFH
    #   hhShare["MF", yr] = 1.0 - hhShare["SF",yr]   
       HH_withHeat[i,yr] = HH_withHeat[i,ThisYear]
       HH_withCool[i,yr]  =HH_withCool[i,ThisYear]   
       cz[i,yr ] = climatezone( i,hdd, cdd, IncTemp, hhsize_thisyear,growthrate, hhShare) 
   
    for yr in range(ThisYear,EndYear+1):             #NO population growth and NO change in Thermal insulation
       hhsize_last = hhsize_thisyear    
       Thishhsize =  hhsize_thisyear  *(1 + growthrate)**(yr-ThisYear)     
       hhShare["SF",yr] = SFH
    #   hhShare["MF", yr] = 1.0 - hhShare["SF",yr] 
       HH_withHeat[i,yr] =  min(1.0, HH_withHeat[i,ThisYear] *(1+ heatSaturationInc)**(yr-ThisYear))
       HH_withCool[i,yr] = min(1.0, HH_withCool[i,ThisYear]* (1 + coolSaturationInc)**(yr-ThisYear))
       hdd_yr = hdd   * (1+hddchangeRate)**(yr-ThisYear)
       cdd_yr = cdd   * (1+cddchangeRate)**(yr-ThisYear)     
       cz[i,yr ] = climatezone( i,hdd_yr, cdd_yr, IncTemp, Thishhsize,growthrate, hhShare)
  
     
  # print "past values", i, yr, cz[i,yr].HHShare["SF",yr]* Thishhsize, cz[i,yr].hdd, cz[i,yr].cdd, 1.0/R0val[i,yr], 1.0/R1val[i,yr], 1.0/R2val[i,yr]
#for yr in range(ThisYear+1, ThisYear+15): 
#       for i in range(1, Numcz+1):            
#           print yr, i,  HH_withHeat[i,yr], HH_withCool[i,yr], cz[i,yr].HHsize