# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:18:54 2018
@author: shubaraghavan
"""
from scipy.stats import weibull_min
#from Housing_Class_NewHomes import *
from Housing_Class1 import *

import xlrd
import xlsxwriter
import itertools
import numpy as np
#import seaborn as sns
from matplotlib.pyplot import cm 

import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as mpatches

bar_width = 0.25
wide = 1.0
diff= 0.25
xTickMarks = ['','','','','','','','','','','','','' ,'','','' ,'','' ,'','' ,'', '','']
# MyList = list(range(1,Numcz+1))
# CompYears = MyList

# xTickMarks[1] =CompYears[1]
# xTickMarks[2] = CompYears[5]
# xTickMarks[3]=CompYears[8]
# xTickMarks[4]=CompYears[11]
# xTickMarks[5]=CompYears[15]
#xTickMarks[6]=CompYears[5]   
Stck1 = 1
#==========================
years = 2021
CarbonCost  =  50
#============================
fig1 = plt.figure(figsize=(8.0, 8.0))  #Annual Energy
a1 = fig1.add_subplot(1, 1, 1)
xTickNames1 = a1.set_xticklabels(xTickMarks)
plt.setp(xTickNames1, rotation=0, fontsize=15)
#plt.title('SF Homes: LCC of H&C in 2018 ')
a1.set_xlabel('Climate Zones 1- 16', fontsize = 14,labelpad =10)
a1.set_ylabel("15-year NPV of heating & cooling costs of Existing homes($) ", fontsize = 14,labelpad =30)
plt.title("HH2 vs HH4 New Home %0.0f ($)" %(years), fontsize = 14)
#plt.title('Comparison: New SF2 ')

# fig2 = plt.figure(figsize=(8.0, 8.0))  #Annual Energy
# a2 = fig2.add_subplot(1, 1, 1)
# xTickNames2 = a2.set_xticklabels(xTickMarks)
# plt.setp(xTickNames2, rotation=0, fontsize=15)
# a2.set_xlabel('Climate Zones 1- 16 ', fontsize = 14,labelpad =10)
# a2.set_ylabel("Differences in 15-year NPV of Costs ($) ", fontsize = 14,labelpad =15)
# plt.title("HH2 vs. HH4 in %0.0f ($)" %(years), fontsize = 14)

# fig3 = plt.figure(figsize=(8.0, 8.0))  #Annual Energy
# a3 = fig3.add_subplot(1, 1, 1)
# xTickNames3 = a3.set_xticklabels(xTickMarks)
# plt.setp(xTickNames3, rotation=0, fontsize=15)
# a3.set_xlabel('Climate Zones 1- 16', fontsize = 14,labelpad =10)
# a3.set_ylabel("Difference in NPV of H&C ($) ", fontsize = 14,labelpad =15)
# plt.title('SF2: Existing HOme replaces AC & NG Furnace with HPSC ')

#plt.title("Heating & Cooling Costs of New SF homes %0.0f with CarbonCost of %0.0f ($/kg)" %(years, CarbonCost), fontsize = 12)
p1 = []
p2 = []
p3 = []
cnt = 0
horizon =  AC_LT #lifetime of an AC or HP
isretrofit = False
isfuelswitch = False # converting AC to Cond...does not need elec upgrade is the assumption..so is false
isnew = False  #new home  REMEMBER FOR AN EXISTING HOME>>>MAKE NGIC = 0 AS WE ASSUME ONLY AC REPLACED BY COND>>AND NG CONTINUES TO WORK
for k in (3, 6,9, 12):          
        cnt += 1
    
   # for years in range(ThisYear+1, EndYear+1,10):
    #  HH = cz[k,years].HHsize  #Millions
        HH = 1   # One unit         
#        HH = cz[k,years].HHsize  #Millions

#        HH_Heat = HH* HH_withHeat[k,ThisYear]  #Number of HHs with heating
#        HH_Cool = HH* HH_withHeat[k,ThisYear]   #Number of HHs with cooling       
        devices1 = []
       # devices1 += [ NGHeater(k,size1,size2, years,NGIC,isretrofit, isnew)]
        devices1 += [Cooler(k,size1,size2 , years,ACIC, isnew)]
        
        SF1 =  SFHomes("SF1",Stck1 , k,size1, size2,years, devices1,isnew)          
        devices3 = []
        devices3 += [Cond(k,size1,size2,years,HPCapex1, isretrofit, isfuelswitch, isnew)]
        SF3 =  SFHomes("SF4",Stck1 , k,size1, size2,years,devices3, isnew)        
   
        npv1 = SF1.HHDevicesCapCost(years)  /(1000)  #/SF1.devices[0].lt   #Capital cost + O&M
        npv3 = SF3.HHDevicesCapCost(years)  /(1000) 
        Engnpv1 = SF1.HHNPVEnergyCost_LT(years, horizon) /(1000)
        Engnpv3 = SF3.HHNPVEnergyCost_LT(years,horizon)  /(1000)
        CCnpv1 = SF1.HHNPVEmissionsCost_LT(years,horizon, CarbonCost) /(1000)
        CCnpv3 = SF3.HHNPVEmissionsCost_LT(years, horizon,CarbonCost)  /(1000)

        npv_diff = npv3 - npv1
        eng_diff = Engnpv3 - Engnpv1
        CC_diff = CCnpv3 - CCnpv1
        lcc_diff = npv_diff + eng_diff + CC_diff         
        lcc1 = SF1. HHLCC( years,CarbonCost) 
        lcc3 = SF3. HHLCC( years,CarbonCost) 
        
       # ef1 = SF1.devices[0].ef
        ef11 = SF1.devices[0].ef_cooler
        ef3 = SF3.devices[0].ef
        ef33 = SF3.devices[0].ef_cooler
     
        print "NG + AC ",years, k, npv1,  Engnpv1,CCnpv1, "HPSC", npv3, Engnpv3, CCnpv3
     #   print " efficiencies",  ef11, ef3, ef33
       # print "HDDs, CDDs",SF1.devices[0].HDD,SF1.devices[1].HDD ,SF3.devices[0].HDD, SF1.devices[0].CDD, SF1.devices[1].CDD, SF3.devices[0].CDD
        plt.hold(True)
        plt.hold(True)
        plt.hold(True)
        B1 = a1.bar(3*k+2, npv1, width = wide, color = 'red', align = 'center')
        B2 = a1.bar(3*k +2, Engnpv1, width = wide, color = 'hotpink',hatch = '',bottom = npv1, align = 'center')  

        B3 = a1.bar(3*k + 2, CCnpv1 , width = wide, color = 'hotpink', hatch = '\\\\',bottom = npv1+ Engnpv1 ,align = 'center')
        C1 = a1.bar(3*k +3, npv3, width = wide, color = 'darkgreen', align = 'center')
        C2 = a1.bar(3*k +3, Engnpv3, width = wide, color = 'yellowgreen',hatch = '',bottom = npv3 ,align = 'center')    
        C3 = a1.bar(3*k+ 3 ,CCnpv3 , width =wide, color = 'yellowgreen', hatch = '\\\\', bottom = npv3 +  Engnpv3 ,align = 'center')
        p3.append([B1,B2,B3,C1,C2,C3])       
          
      #  B555 = a1.bar(k+ 2, 0, width = 0, color = 'white', hatch = "\\\\",  align = 'center')    
      #  p1.append([B1,B2, B3])
     #   l2 = a1.legend([B555], ['Carbon Cost'],loc=1, ncol =1, fontsize = 12 )
        l1 = a1.legend([ mpatches.Patch(color='hotpink'),mpatches.Patch(color='red'),mpatches.Patch(color='yellowgreen'),mpatches.Patch(color='darkgreen') ],\
                      ['NG & Elec Cost','Elec AC Capex','HPSC Energy Cost','HPSC Capex'], loc=2 , ncol=2 ,fontsize = 12)   
   #     a1.add_artist(l2)               
        
        # D1 = a3.bar(3*k +3, npv_diff, width = wide, color = 'red', align = 'center')
        # D2 = a3.bar(3*k +3, eng_diff, width = wide, color = 'yellow',hatch = '',bottom = npv_diff ,align = 'center')    
        # D3 = a3.bar(3*k+ 3 , CC_diff , width =wide, color = 'green', hatch = '\\\\', bottom = npv_diff+eng_diff ,align = 'center')
        # p3.append([D1,D2,D3])       
       # B111 = a3.bar(k+ 2, 0, width = 0, color = 'white', hatch = "\\\\",  align = 'center')    
       
       # l2 = a3.legend([B111], ['Carbon Cost'],loc=1, ncol =2, fontsize = 12 )
       # l1 = a3.legend([ mpatches.Patch(color='yellowgreen'),mpatches.Patch(color='darkgreen')],\
       #               ['HPCond Energy Cost','HP-Cond Capex' ], loc=2 , ncol=1 ,fontsize = 12)   
     #   a3.add_artist(l2)               
        
    #     B22 = a2.bar(4*k+0.5 ,  npv_diff, width = wide, color = 'red', align = 'center' )
    #     B23= a2.bar(4*k +1.5, eng_diff, width= wide, color = 'orange',  align = 'center')
    #     B24 = a2.bar(4*k +2.5 , CC_diff, width = wide, color = 'blue',  align = 'center' )
    #     p2.append([ B23, B24])
    #    # B555 = a2.bar(k+ 2, 0, width = 0, color = 'white',   align = 'center')    
    # #    l2 = a2.legend([B555],loc=1, ncol =1, fontsize = 12 )
    #     l1 = a2.legend([mpatches.Patch(color='red'), mpatches.Patch(color='orange') , mpatches.Patch(color='blue')],\
    #                   ['Diff in Capex','Diff in NPV of Energy Cost' , 'Diff in NPV of Carbon Cost' ], loc=4 , ncol=1 ,fontsize = 10)   

     #   a2.add_artist(l2)    
    #    fig1.tight_layout()  
     #   fig2.tight_layout()
plt.show()
plt.show()        


