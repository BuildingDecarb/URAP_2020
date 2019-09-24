# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 20:34:28 2016

@author: shubaraghavan
"""
#returns energy in BTU

#https://www.e-education.psu.edu/egee102/node/2070
#http://www.sensiblehouse.org/nrg_heatloss.htm

from HDD_CDD_UValues import *
from UValues import *
def AnnualEngDemand(fuel, HDD,  size1, size2,Rval0, Rval1, Rval2, heaterEF):
   
#==============================================================================
#    HDD is the sum of all [houly average degrees below the thermostat 
#    set temp] in ayear    
#    Rval - ft2·°F·hr/Btu
#     Size1   #surface area of walls
#     Size2  #surface area of roof, floor
#==============================================================================
  #  print "HDD", HDD,Rval0, Rval1, size1,size2, windowPerc,heaterEF
    Rval3 = 0.048   # floor
    HeatLoss3 = 0  
    windowArea= windowPerc * size1
    size1 = (1-windowPerc)* size1  #wall area without window
    HeatLoss0 = (HDD *24.0 *windowArea)/Rval0   #window    
    HeatLoss1 = (HDD *24.0 * size1) /(Rval1)  # walls #BTU
    HeatLoss2 = (HDD *24.0 * size2) /(Rval2)  #Roof
   # HeatLoss3 = (HDD *24.0 * size2) /(Rval3)  #Flooe
  #  HeatLoss3 =  (HDD *24.0 * size2) /Rval2      #floor
  #  print "HeatLoss", HeatLoss1, HeatLoss2
    AnnualHeatRequired = HeatLoss3 + HeatLoss1 + HeatLoss2  + HeatLoss0 #+HeatLoss3
    AnnualHeatDemand = AnnualHeatRequired/heaterEF
   # print "Annual Heat Demand", Rval0, Rval1, Rval2, HDD, heaterEF, AnnualHeatRequired, AnnualHeatDemand
   # print "AnnualHeatDemand in kBTU", fuel.name,AnnualHeatDemand/1000, "\n"
    #print "Ann HD", AnnualHeatDemand
    return AnnualHeatDemand
#==============================================================================
#     if fuel.name == 'NG':
#         return (AnnualHeatDemand/Therm_BTU)
#     elif fuel.name =='Elec':
#         return AnnualHeatDemand/kWh_BTU    
#    
#=============================================================================
def AnnualCoolingDemand(fuel, CDD,  size1,size2,Rval0, Rval1, Rval2, coolerEF):
    
   # print "HDD", CDD,Rval0, Rval1, size1,size2,windowPerc, coolerEF
    Rval3 = 0.048
    HeatLoss3 = 0 
    windowArea= windowPerc * size1
    size1 = (1-windowPerc)*size1
    HeatLoss0 = (CDD *24.0 *windowArea)/Rval0   #window    
    HeatLoss1 = (CDD * 24.0 * size1) /(Rval1)  # walls #BTU
    HeatLoss2 = (CDD * 24.0 * size2) /(Rval2)  #Roof
   # HeatLoss3 = (CDD * 24.0 * size2) /(Rval3)  #Roof
  #  HeatLoss3 =  (CDD * 24.0 * size2) /Rval2      #floor
  #  print "HeatLoss", HeatLoss1, HeatLoss2
    AnnualCoolRequired = HeatLoss3 + HeatLoss1 + HeatLoss2 + HeatLoss0 # +HeatLoss3
    AnnualCoolDemand = AnnualCoolRequired/coolerEF
   # print "Annual Cool Demand", AnnualHeatDemand
   # print "AnnualCoolDemand in kBTU", fuel.name,AnnualHeatDemand/1000, "\n"
   
    return AnnualCoolDemand

    