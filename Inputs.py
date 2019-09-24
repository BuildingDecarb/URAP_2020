#Inputs
#----------
#Following report CEC NG use in Residential WH
#http://www.energy.ca.gov/2013publications/CEC-500-2013-060/CEC-500-2013-060.pdf
# Avg hot water draw in gallons/day is ~56 pp 225 of the report (given by climate zone)
#Avg increase in temp is 75...assuming 55/gal/day
import pandas as pd
import numpy as np
from numpy import *

from Inputs_Appliances_Retrofit import *

VacancyRate = 0.0  #0.072 as of 1/1/2015
  # 13.9 Million 0 #s households as of 1/1/2016
#NumHHTotal =  13.9 * 10**6
PopGrowth =   0.0082   # 0.0082
DiscRate = 0.04
#---------------------------------------------------------------------
samplesize = .0025       # percentage of the 13.9 million houses that is simulated
#-----------------------------------------------------------------
SFH = 1.0  #  0.58    # *NumHH Single fam- 
MFH = (1.0-SFH)   #  * NumHH  Multi fam
SFGrowth = 0.5 # % of share of houses that are SF..PLACEHOLDER for now..same Growth for all CZs for now

P1 = 0.86  #SF with NG in ThisYear
P2 = 1.0 - P1  # SF with Elec
Q1 = 1.0 #0.9   # MF with NG
Q2 = 1.0 - Q1

#NumHH = NumHHTotal * (1-VacancyRate)
#HHThisYear = NumHH

Numcz = 16 #number of CZs 10 (actually 16, for now 10 -for ease)
NumHHCZ = {}

#dimensions of a single family home
windowPerc = 0.15
size1 =    ( 42*10*4  +  25*10*4) *(1-windowPerc) # surface area of the 4 outer walls 2100 sf home 2 storied  #    42 * 50 * (1-windowPerc) -1 story
size0 = windowPerc * size1
size2 =  42*25  #roof area   # for 1 story 42 * 50   #

#below is for a Multi-family home
# windowPercMF = windowPerc
size11 = (38 * 10 *4  + 22 * 10*2)*(1-windowPerc)  #*2 one less wall exposed to the elemetns of weather
size00 = windowPerc * size11
size22 = 38 * 22    # roof area
# #right now this is fixed

##-----------------------------------------------------------------------------
#Below are the inputs for Heating technologies     
#REF- Lutz et al 2011; LBNL Using National survey data to estimate lifetimes of residential appliances
#MEanlife of furnaces are around 24-25 years
#Meanlife of heat pumps ~ 15
