# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:22:53 2018
@author: shubaraghavan
"""
from Inputs import *
import xlrd
# Read in UValues for buildings (walls, roof and windows) and Inc Temp for water heater

workbook = xlrd.open_workbook('HDD_CDD_CA.xlsx')
sheet_name = workbook.sheet_names()
UVals= workbook.sheet_by_name(sheet_name[1])  #U values and

R0val  = {} # R0val[C,vintage]
R1val = {}
R2val = {}

#right now this is fixe
for i in range (1, Numcz+1):
    R0past = 1.0/UVals.cell(45,8).value   # window
    R1past = 1.0/UVals.cell(44,8).value    #walls
    R2past = 1.0/UVals.cell(43,8).value   #roof
    
    R0present = 1.0/UVals.cell(45,11).value 
    R1present = 1.0/UVals.cell(44,11).value
    R2present = 1.0/UVals.cell(43,11).value 
    
    
    R0future = 1.0/UVals.cell(45,13).value
    R1future = 1.0/UVals.cell(44,13).value 
    R2future = 1.0/UVals.cell(43,13).value 
    
    
    for yr in range(PastYear-30,ThisYear-40):    
       
       R0val[i,yr] = 1.0/UVals.cell(45,3).value   #1.0/HDD_CDD.cell(23+1,11).value   # window
       R1val[i,yr] = 1.0/UVals.cell(44,3).value   #1.0/HDD_CDD.cell(23+1,6).value
       R2val[i,yr] =   1.0/UVals.cell(43,3).value
       
    for yr in range(ThisYear -40,ThisYear-5):    #upto 2000
       
       R0val[i,yr] = R0past   #1.0/HDD_CDD.cell(23+1,11).value   # window
       R1val[i,yr] = R1past   #1.0/HDD_CDD.cell(23+1,6).value
       R2val[i,yr] =  R2past  
   
    for yr in range(ThisYear -5,ThisYear+2):     
      
       R0val[i,yr] = R0present  #1.0/HDD_CDD.cell(23+1,11).value   # window
       R1val[i,yr] = R1present   #1.0/HDD_CDD.cell(23+1,6).value
       R2val[i,yr] =  R2present
        
    for yr in range(ThisYear+2,EndYear+1):            

       R0val[i,yr] = R0future   #1.0/HDD_CDD.cell(23+1,11).value   # window
       R1val[i,yr] = R1future
       R2val[i,yr] =  R2future
     
