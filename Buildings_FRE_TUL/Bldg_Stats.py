import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from Bldg_Read_test import *
from matplotlib.pyplot import figure

name = "TUL"           #"FRE"   #'KER', 'TUL' 'Kern_Bodfish', 'Kern_Weedpatch', 'Kern_Losthills'
name1 = name
filename = name +"2016.csv"

cnty = pd.read_csv(filename)
building_types = cnty['Typef'].unique()
avg_statistic_per_bldgtype(cnty, name, 'Typef', 'EEUIC', 'Building Elec Cooling (kWh/sqf)', 'Avg. Cooling Elec Intenstiy per Building Type in  ' + name1 + ' County')
avg_statistic_per_bldgtype(cnty, name, 'Typef', 'NGEUISH', 'Building NG SH (kWh/sqf)', 'Avg.NG Space heating Intenstiy per Building Type in  ' + name1 +' County')
avg_statistic_per_bldgtype(cnty, name, 'Typef', 'NGEUIWH', 'Building NG WH (kWh/sqf)', 'Avg.NG Water heating Intenstiy per Building Type in  ' + name1 + ' County')

avg_statistic_per_bldgtype(cnty, name, 'Typef', 'BLDGAREA', 'Building Area (sqf)', 'Avg Building Area of Each Type in  ' + name1 + ' County')

avg_bldgarea = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'BLDGAREA')[0]

#print "test4",avg_bldgarea
avg_ngeuish = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'NGEUISH')[0]
avg_ngeuiwh = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'NGEUIWH')[0]
avg_ngeuic = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'NGEUIC')[0]
avg_eeuic = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'EEUIC')[0]
avg_eeuipc = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'EEUIPC')[0]
bldg_count = avg_statistic_per_bldgtype_no_plot(cnty, 'Typef', 'EEUIPC')[1]

tul_df = pd.DataFrame(data={'Building Types':building_types, 
                        'Avg. Building Area':avg_bldgarea,
                        'Avg. Natural Gas Space Heating':avg_ngeuish,
                        'Avg. Natural Gas Water Heating':avg_ngeuiwh,
                        'Avg. Natural Gas Cooling':avg_ngeuic,
                        'Avg. Electric Cooling':avg_eeuic,
                        'Avg. Process Cooling':avg_eeuipc,
                        'Total Bldgs':bldg_count    
                       })



tul_df.to_csv('plots/' + name+ '_bldgs_March71.csv')

building_count = []
for i in range(cnty['Typef'].unique().size):
        bldgtype = cnty['Typef'].unique()[i]
        building_count.append(cnty[cnty['Typef']==bldgtype]['BLDGAREA'].count())
        print "cnt", bldgtype,  building_count[i]
      
total_ngui = avg_ngeuish + avg_ngeuiwh
print "total", total_ngui
fig1 = plt.figure(figsize=(18, 6))
plt.title("Total NG for Space & Water Heating in"+ name1 + " County", fontsize= 15)
plt.xlabel("Building Types", fontsize = 10)
plt.ylabel('Space & Water heating (kWh/sqf)', fontsize = 10)
bar1 = plt.bar(cnty['Typef'].unique(), avg_ngeuish, color= 'r')
bar2 = plt.bar(cnty['Typef'].unique(), avg_ngeuiwh, bottom = avg_ngeuish, color= 'orange')
#bar3 = plt.bar(cnty['Typef'].unique(), avg_eeuic, bottom= avg_ngeuish+avg_ngeuiwh, color = 'blue')
plt.legend(( bar2,bar1), ('NG WH', 'NG SH'), fontsize = 10)
##bars = plt.bar(cnty['Typef'].unique(), avg_ngeuish + avg_ngeuiwh)
##i = 0
##for bar in bars:
##       
##        yval = bar.get_height()
##        plt.text(bar.get_x()+0.3, yval + (yval*0.01), str(building_count[i]))# + " Buildings")
##        i += 1

fig1.tight_layout()    

fig1.savefig('plots/'+ name1 +  "_NG_Total_UEC" +  '_Aprilfig.png')

# Conerting NG usage to electricity

EF1 =1 # 0.67/4.0
EF2 = 1.0

elec_sh = avg_ngeuish * EF1
elec_wh = avg_ngeuiwh * EF1
elec_sc = avg_eeuic * EF2
fig1 = plt.figure(figsize=(18, 6))
plt.title("Unit Electricity Intensity for cooling & heating")
plt.xlabel("Building Types")
plt.ylabel('Energy Intensity: Heating & Cooling (kWh/sqf)')
bar1 = plt.bar(cnty['Typef'].unique(), elec_sh, color= 'r')
bar2 = plt.bar(cnty['Typef'].unique(), elec_wh, bottom = elec_sh, color= 'orange')
bar3 = plt.bar(cnty['Typef'].unique(), elec_sc, bottom = elec_sh+elec_wh, color= 'blue')

plt.legend((bar3,bar2,bar1), ('Coolng', 'Water Heating', ' Space Heating'))

fig1.tight_layout()    

fig1.savefig('plots/'+ name +  "Elec_heating_cooling" +  '_Apri30fig.png')






