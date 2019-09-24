# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:18:54 2018
@author: shubaraghavan
"""

#from HDD_CDD_UValues import *
from Housing_Class1 import *
#from HDD_CDD_Iterate import *
#from HousingTypes import *
import xlrd
import xlsxwriter
import numpy as np
#import seaborn as sns
from matplotlib.pyplot import cm 
from matplotlib import pylab

import matplotlib.pyplot as plt
from matplotlib.pyplot import *

workbook = xlsxwriter.Workbook('SF2_SF4_ExistHomeApril4.xlsx')
worksheet = workbook.add_worksheet()

# plt.style.use('ggplot')
import matplotlib.patches as mpatches
colors = [ 'red','orange','green', 'blue', 'blueviolet', 'yellowgreen', 'darkred','salmon']
Hhatch = ['o', 'x', '*', '+']
bar_width = 1.0
wide = 1.0
gap = .2
diff= 1.0
yrcnt = 0
Stck1 = 1


xTickMarks = ['','','','','','','','','','',''] #,'' ,'','','' ,'','' ,'','' ,'', '','']
#MyList = list(range(1,Numcz+1))
#CompYears = []
CompYears = ('3','4','6','7','8','9','10','12')
MyList = ['3','4','6','7','8','9','10','12']
index = len(CompYears)
print "index", index
#CompYears = MyList
# xTickMarks = []
# xTickMarks[0] =CompYears[0]
# xTickMarks[1] = CompYears[1]
# xTickMarks[2]=CompYears[2]
# xTickMarks[3]=CompYears[3]
# xTickMarks[4]=CompYears[4]
# xTickMarks[5]=CompYears[5]
# xTickMarks[6]=CompYears[6]
# xTickMarks[7]=CompYears[7]

fig1 = plt.figure(figsize=(6.0, 4.0))  #Annual Energy
a1 = fig1.add_subplot(1, 1, 1)
a1.set_xlabel("CA Climate Zones ", fontsize = 9,labelpad =10)
a1.set_xticks((np.array(range(len(CompYears)), dtype=int)*5)+1.5 + gap/2)
xTickNames1 = a1.set_xticklabels(CompYears)
#a1.set_xticks(index + bar_width/2.0)
plt.setp(xTickNames1, rotation=0, fontsize=9)
#
fig2 = plt.figure(figsize=(10.0, 8.0))  #Annual Energy
a2 = fig2.add_subplot(1, 1, 1)
a2.set_xlabel("CA Climate Zones ", fontsize = 14,labelpad =10)
xTickNames2 = a2.set_xticklabels(xTickMarks)
plt.setp(xTickNames2 ,rotation=0, fontsize=15)

fig3 = plt.figure(figsize=(6.0, 4.0))  #Annual Energy
a3 = fig3.add_subplot(1, 1, 1)
a3.set_xticks((np.array(range(len(CompYears)), dtype=int)*5)+1.5 + gap/2)
a3.set_xlabel("CA Climate Zones ", fontsize = 9,labelpad =10)
xTickNames3 = a3.set_xticklabels(CompYears)
plt.setp(xTickNames3, rotation=0, fontsize=9)

fig4 = plt.figure(figsize=(10.0, 8.0))  #Annual Energy
a4 = fig4.add_subplot(1, 1, 1)
a4.set_xlabel("CA Climate Zones ", fontsize = 14,labelpad =15)
xTickNames4 = a4.set_xticklabels(xTickMarks)
plt.setp(xTickNames4, rotation=0, fontsize=15)
HH =1
I = 1 # number of scenarios
N =Numcz
ind = np.arange(N)
Endtime = EndYear       # 2050 
years = 2020
isnew = False # False for old existing home and New for new homes
isretrofit = True  #being retrofitted....make sure this is for AC to HPCond - so cost of NG furnace should be made $0 
isfuelswitch = False
#===========================
# Comapares 2 single family homes in 16 climate zones in the year = years
#=====================================================
for j in range(len(CompYears)):
  jj = MyList[j]
  k = int(jj)
  for cnt in range (0,I):      
   # a1 and a3 compare dual fuel and all-electric homes
   #a2 and a4 are for dual-fuel homes
    a1.set_ylabel(" Annual H & C demand in %0.0f (kWh)" %(years), fontsize = 9,labelpad = 8)
    a3.set_ylabel("GHG Emissions (MMTCO2e) in %0.0f" %(years), fontsize = 9,labelpad =8)
    a2.set_ylabel("Annual H & C demand in %0.0f (kWh)" %(years),  fontsize = 9,labelpad =8)
    a4.set_ylabel("GHG Emissions (MMTCO2e)bin %0.0f" %(years), fontsize = 9,labelpad =8)
    HH = 1  # cz[k,years].HHsize 
    
    HeatPerc = 1 #   HH_withHeat[k,years]
    CoolPerc = 1 # HH_withCool[k,years]   #value = 1 if comparing a single home
    MFScale = 1 #0.72  #1
    MFScale_H = MFScale
    MFScale_C = MFScale
    SFHeatNum =   HH * HeatPerc *cz[k,years].HHShare["SF", years]   #Number of houses with heating in this cz
    SFCoolNum =    HH * CoolPerc *cz[k,years].HHShare["SF",years]
       
    devices1 = []
    devices1 += [ NGHeater(k,size1,size2, years,NGIC, isretrofit,isnew)]
    devices1 += [Cooler(k,size1,size2 , years,ACIC, isnew)]
    SF1 =  SFHomes("SF1",Stck1 , k,size1, size2,years,devices1,isnew)
  
    devices3 = []
    devices3 += [Cond(k,size1,size2,years, HPCapex1, isretrofit, isfuelswitch, isnew)]
    SF3 =  SFHomes("SF3",Stck1 , k,size1, size2,years,devices3)  

    devices4 = []
    devices4 += [Cond(k,size1,size2,years, HPCapex1, isretrofit, isfuelswitch, True)]
    SF4 =  SFHomes("SF4",Stck1 , k,size1, size2,years,devices3)  


    heat1 = MFScale_H * SFHeatNum * SF1.HHenergyUsage_BTU()[0]/kWh_BTU
    cool1 = MFScale_C * SFCoolNum * SF1.HHenergyUsage_BTU()[1]/kWh_BTU
    emis1 = MFScale_H * SFHeatNum * SF1.HHemissions_refrig(years)[0]  #NG emissions
    emis11 = MFScale_C * SFCoolNum  * SF1.HHemissions_refrig(years)[1]  #elec emissions
    emis111 = MFScale_C * SFCoolNum  * SF1.HHemissions_refrig(years)[2]  #refrig emissions
    
    heat3 = MFScale_H * SFHeatNum * SF3.HHenergyUsage_BTU()[0]/kWh_BTU
    cool3 = MFScale_C * SFHeatNum * SF3.HHenergyUsage_BTU()[1]/kWh_BTU
    emis3 = MFScale_H * SFHeatNum * SF3.HHemissions_refrig(years)[0]  #NG emissions
    emis33 = MFScale_C * SFHeatNum  * SF3.HHemissions_refrig(years)[1]  #elec emissions
    emis333 = MFScale_C * SFHeatNum  * SF3.HHemissions_refrig(years)[2]  #refrig emissions

    heat4 = MFScale_H * SFHeatNum * SF4.HHenergyUsage_BTU()[0]/kWh_BTU
    cool4 = MFScale_C * SFHeatNum * SF4.HHenergyUsage_BTU()[1]/kWh_BTU
    emis4 = MFScale_H * SFHeatNum * SF4.HHemissions_refrig(years)[0]  #NG emissions
    emis44 = MFScale_C * SFHeatNum  * SF4.HHemissions_refrig(years)[1]  #elec emissions
    emis444 = MFScale_C * SFHeatNum  * SF4.HHemissions_refrig(years)[2]  #refrig emissions
  
  #  print "numbers",  k, years, SFHeatNum,SFCoolNum, HeatPerc, CoolPerc
    print "Eng", k, years,heat1, cool1,heat3, cool3, emis1, emis11,emis111  ,".", heat4, cool4, emis4, emis44, emis444 #, emis1, emis11,emis3, emis33, emis333
   # print "Rvals", SF4.devices[0].Rval0, SF4.devices[0].Rval1,SF4.devices[0].Rval2, "..", SF1.devices[0].ef, SF1.devices[1].ef_cooler, SF4.devices[0].ef, SF5.devices[0].ef,SF4.devices[0].ef_cooler, SF5.devices[0].ef_cooler
    #
    plt.hold(True)
   # plt.title(" Per SF Home H in year %0.0f (Mod EF imp)" %(years), fontsize = 14)  
    b1 = a1.bar(j*5+1, heat1, width = wide, color = colors[0], align = 'center')
    b1 = a1.bar(j*5+1, cool1 , width = wide, color = colors[1], bottom = heat1, align = 'center')
    

    b1 = a1.bar(j*5+2 + gap, heat3, width = wide, color = colors[2], align = 'center')
    b1 = a1.bar(j*5+2 + gap, cool3 , width = wide, color = colors[3],bottom = heat3, align = 'center')
  #  b1 = a1.bar(k*5+3, heat4, width = wide, color = colors[4], align = 'center')
  #  b1 = a1.bar(k*5+3, cool4 , width = wide, color = colors[5],bottom = heat4, align = 'center')



    b4 = a3.bar(j*5+ 1, emis1 , width = wide, color = colors[0], align = 'center')
    b4 = a3.bar(j*5 +1, emis11, width = wide, color = colors[1],  bottom = emis1,align = 'center')
    b4 = a3.bar(j*5 +1, emis111, width = wide, color = colors[1],hatch = '////',  bottom = emis1 + emis11,align = 'center')
   
    b4 = a3.bar(j*5+2 + gap, emis3 , width = wide, color = colors[2], align = 'center')
    b4 = a3.bar(j*5+2 + gap, emis33, width = wide, color = colors[4],  bottom = emis3 ,align = 'center')
    b4 = a3.bar(j*5+2 + gap, emis333, width = wide, color = colors[4],hatch = '////',  bottom = emis3+ emis33,align = 'center')

 #   b4 = a3.bar(k*5+3, emis4 , width = wide, color = colors[4], align = 'center')
 #   b4 = a3.bar(k*5+3, emis44, width = wide, color = colors[5],  bottom = emis4,align = 'center')
 #   b4 = a3.bar(k*5+3, emis444, width = wide, color = colors[5],hatch = '////',  bottom = emis4 + emis44,  align = 'center')
    
#    a1.set_ylim(0,12000)

 #  b2 = a2.bar(k*5+cnt, heat2, width = wide, color = colors[cnt], hatch = 'x',bottom = heat1, align = 'center') 
    # b2 = a2.bar(k*5, heat1, width = wide, color = 'red', align = 'center')
    # b2 = a2.bar(k*5+1 , cool1 , width = wide, color = 'blue',  align = 'center')
   
    # b4 = a4.bar(k*5, emis1, width = wide, color = 'blue', align = 'center')
    # b4 = a4.bar(k*5+1 , emis11 , width = wide, color = 'darkorange',  align = 'center')
    # b4 = a4.bar(k*5+1 , emis111 , width = wide, color = 'green',  bottom= emis11, align = 'center')


#    a1.set_ylim(0,12000)
#    a2.set_ylim(0,1000)
#    a4.set_ylim(0,3.0)
#    a4.set_ylim(0,0.75)
    
    worksheet.write(2,10*cnt +1,"#HHs w. Heating")
    worksheet.write(2,10*cnt +2,"#HHs w. Cooling" )  
    worksheet.write(2,10*cnt +3,"#HDD")
    worksheet.write(2,10*cnt +4,"#CDD" )                 
    worksheet.write(2,10*cnt+ 5, "SF1 HeatDemand (GWh)")
    worksheet.write(2,10*cnt+6, "SF1 Cool Demand (GWh)")
    worksheet.write(2,10*cnt+7, "SF1 Heat Emis (MMTons)")
    worksheet.write(2,10*cnt+8, "SF1 Cool Emis (MMTons)")

    worksheet.write(2,10*cnt+ 10, "SF4 HeatDemand (GWh)")
    worksheet.write(2,10*cnt+11, "SF4 Cool Demand (GWh)")
    worksheet.write(2,10*cnt+12, "SF4 Heat Emis (MMTons)")
    worksheet.write(2,10*cnt+13, "SF4 Cool Emis (MMTons)")

    worksheet.write(2,10*cnt+16, "Rval0-window")
    worksheet.write(2,10*cnt+17, "Rval1-wall")
    worksheet.write(2,10*cnt+18, "Rval2-roof")
  
  
    worksheet.write(2+k, 10* cnt +1, SFHeatNum )
    worksheet.write(2+k, 10* cnt +2, SFCoolNum )    
    worksheet.write(2+k, 10* cnt +3, SF1.devices[0].HDD)
    worksheet.write(2+k, 10* cnt +4, SF1.devices[0].CDD ) 
    
    worksheet.write(2+k, 10* cnt +5, heat1)  
    worksheet.write(2+k, 10* cnt +6, cool1 )  
    worksheet.write(2+k, 10* cnt +7, emis1 )
    worksheet.write(2+k, 10* cnt +8, emis11 )
    worksheet.write(2+k, 10* cnt +10, heat3)  
    worksheet.write(2+k, 10* cnt +11, cool3 )  
    worksheet.write(2+k, 10* cnt +12, emis3 )
    worksheet.write(2+k, 10* cnt +13, emis33 )

    worksheet.write(2+k, 10* cnt +16, SF1.devices[0].Rval0 )
    worksheet.write(2+k, 10* cnt +17, SF1.devices[0].Rval1 ) 
    worksheet.write(2+k, 10* cnt +18, SF1.devices[0].Rval2 )
#plt.xticks(bins+1, [str(int(k)) for k in bins])    

bins = np.arange(0,16,1)

#B1 = a1.bar(2, 0, width = 0, color = 'white', align = 'center')
#B11 = a1.bar( 2, 0, width = 0, color = 'white', hatch = "x",  align = 'center') 
#l2 = a1.legend([B11,B1], ['Cooling', 'Heating'],loc=2, ncol =1, fontsize = 11 )
l1 = a1.legend([mpatches.Patch(color='orange'), mpatches.Patch(color='red'),\
                      mpatches.Patch(color='blue'), mpatches.Patch(color= 'green')],\
            ['HH2:Elec AC ','HH2:NG Heat', 'HH4:HPSC Cool', 'HH4:HPSC Heat'], loc = 9, ncol= 2,fontsize = 8) 
#a1.add_artist(l2)

#B2 = a4.bar(2, 0, width = 0, color = 'white', align = 'center')
B22 = a3.bar( 2, 0, width = 0, color = 'white', hatch = "////",  align = 'center')    
m2 = a3.legend([B22], ['Ref.Leakage'],loc=1, ncol =1, fontsize = 8 )
m1 =  a3.legend([mpatches.Patch(color='orange'), mpatches.Patch(color='red'),mpatches.Patch(color= 'blueviolet') ],\
            ['HH2: Elec Emis','HH2:NG Emis', 'HH4:Elec Emis'], loc = 9, ncol = 1,fontsize = 8) 
a3.add_artist(m2)

m4 =  a4.legend([mpatches.Patch(color='red'), mpatches.Patch(color='orange'),mpatches.Patch(color= 'green')],\
            ['HH2: NG Emis','HH2: Elec Emis', 'HH2: Refrig Leakage'], loc =9, ncol = 2,fontsize = 11) 
m22 =  a2.legend([mpatches.Patch(color='red'),mpatches.Patch(color= 'blue')],\
            ['HH2: NG Heat','HH2: Elec AC Cool'], loc =1, ncol = 2,fontsize = 11)            
#  b2 = a2.bar(k*5+cnt, heat2, width = wide, color = colors[cnt], hatch = 'x',bottom = heat1, align = 'center') 

fig1.savefig("Eng_2020_existHome.png",bbox_inches='tight')
fig3.savefig("Emis_2020_existHome.png",bbox_inches='tight')
workbook.close()  
