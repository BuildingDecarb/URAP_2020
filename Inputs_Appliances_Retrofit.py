#Inputs
#----------
#Following report CEC NG use in Residential WH
#http://www.energy.ca.gov/2013publications/CEC-500-2013-060/CEC-500-2013-060.pdf
# Avg hot water draw in gallons/day is ~56 pp 225 of the report (given by climate zone)
#Avg increase in temp is 75...assuming 55/gal/day
import pandas as pd
import numpy as np
from numpy import *
from Inputs_Years import *

LR_HP = 0 #0.15   #Learning Rate for HP Conditioner
HPCumulativeFloor = 2500  #(actually this is sample_size (%) of the total sample).currently set at 1%..will be 5000...1/2 million...
MeanLife = 22  # mean life of appliances
NG_LT = 22
EL_LT = 22
HP_LT = 15
AC_LT = 15  #Cooler lifetime
WH_LT = 13  #water heater
#===================================================
NG_AnnualElecUsage = 100     #400 #kWh/year#
#==================================================
NG0_EF =  0.78 #weighted avg. EF of existing stock
NG_EF = 0.78 # 0.95 #avg efficiency of existing fleet
#==============================================================================
NG1_EF =  0.95
NG2_EF = 0.95
NG3_EF = 0.95
#==============================================================================
E0_EF = 0.98
E_EF = 0.98  #this already exists & does not improve 
E2_EF= 0.98
E3_EF = 0.98

AC0_EF = 2.8    #2.8   #weighted avg. efficicency of exisitng stock
AC1_EF =  3.8
AC2_EF =   4.3
AC3_EF =  4.8      

HP1_EF =  3.0  #heat pumps heating COP
HP2_EF = 3.5  #3.5
HP3_EF = 4.4  # Adv HP using this as the eff of Transcrital CO2, http://www.rehva.eu/fileadmin/hvac-dictio/05-2012/p50-52_shecco.pdf

HP_AC0_EF =  AC0_EF #  2.8  #EAI-Navigant June 2018 Appliances standards update
HP_AC1_EF =  AC1_EF #3.8
HP_AC2_EF = AC2_EF  #4.3
HP_AC3_EF  = AC3_EF # 4.8

HPWH1_EF =  2.4
HPWH2_EF = 3.0
HPWH3_EF = 3.5

NGWH_EF = 0.8
ERWH_EF  = 0.8

NGWHIC = 1000
HPWHIC = 1900

HomeUpgradeCost = 0    #5000  #This is not used...could be for upgrading house shell
NGNewHomeCost = 1500  #Extending a NG pipeline

NGCapex = 1200  #Furnace  # EIA Navigant 2018
NGInstallCost = 2 * NGCapex     # Rocky Mountain Inst, 2018, Billiomoria, et. al, 2018
NG2Capex = NGCapex
NGIC = NGCapex  + NGInstallCost        #1700     # NG Storage Installed Cost (US EIA/DOE - Buildings Ppt -Navigant Presentation April 2014)
NGICNewHome = NG2Capex + NGInstallCost + NGNewHomeCost      # High eff NGWH cost, from E3 

ElecInstallCost = 600
ERHCapex = 600 #installed
ERIC = ERHCapex + ElecInstallCost           # Elec Resistance Installed Cost (US EIA/DOE - Buildings Ppt -Navigant Presentation April 2014)

FuelSwitchCost  = 1500

# Below are HP Conditioners
HPCapex = 2000
HPInstallCost1 = 3 * HPCapex   # Billiomoria, et.al 2018, RMI
HPInstallCost2 = 3 * HPCapex   # Billiomoria, et.al 2018, RMI
HPInstallCost3 = 3 * HPCapex   # Billiomoria, et.al 2018, RMI
HPCapex1 = HPCapex + HPInstallCost1
HPCapex2 = HPCapex + HPInstallCost2   #ditto
HPCapex3 = HPCapex  + HPInstallCost3

HPCapexFloor = 7200  #the floor equals the cost of replacement of AC today..ACIC below

#HPCOnditioner O&M assumed 2 *HP  
HPIC1 = HPCapex1 + FuelSwitchCost   #$5000 - for retrofit
HPIC2 = HPCapex2 + FuelSwitchCost
HPIC3 = HPCapex3 + FuelSwitchCost

HPCondIC1  = HPIC1 
HPCondIC2 = HPIC2 
HPCondIC3 = HPIC3 

HPCondICNew = HPCondIC1 - FuelSwitchCost

ACCapex = 1800
ACInstallCost = 3 * ACCapex     # RMI - Billiomoria, et.al, 2018
ACIC =  ACCapex + ACInstallCost   #

#print "Existing Homes", NGIC, ACIC, HPCondIC1, HPCondIC2, HPCondIC3

Units = [1]*(EndYear - ThisYear+1)

OM_NG = multiply(50, Units)
OM_EL = multiply(0,Units)
#OM_ING = multiply(85, Units) #USEIA-Navigant March 2014
OM_HP = multiply(50,Units)  #USEIA-Navigant March 2014AdvHPWH_LearningRate =  0.1 #0.05
OM_HPCond = multiply(50,Units)

#PastYear = ThisYear - 10