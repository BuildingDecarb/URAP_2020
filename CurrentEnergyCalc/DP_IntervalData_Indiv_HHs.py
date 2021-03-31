#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


#from DP_EnergyCalculator1 import *
from DP_EnergyCalculator_RS_cumdem import *


plt.style.use('fivethirtyeight')
sns.set_context("notebook")
import datetime

startDate = datetime.datetime(2019, 1, 1)

#thisrate = rate_TID("TID")
R1 = Rate_A("PGE_C")
R2 = Rate_B("PGE_D")


climatezone = '13'
pv_size = 3.0

folder = 'DosPalos'

main = 'DP_Main.csv'
interval = folder +"/" + 'DP_IntervalData.csv'

pv = folder + "/" + "13_Fresno.csv"
pv_col = "AC System Output (W)"
pv_df = pd.read_csv(pv, usecols = [pv_col])

sh = "HP_SH_HourlyProfiles.csv"
wh = "HP_WH_HourlyProfiles.csv"

sh_df = pd.read_csv(sh, usecols= [climatezone])
wh_df = pd.read_csv(wh, usecols= [climatezone])


dp_main = pd.read_csv(main)
dp_interval1 = pd.read_csv(interval)
#print "dp interval", dp_interval1
acct_list = dp_main.loc[dp_main["MultiFam"] == "INDIV"]["ANON_SERVPNT_ID"].unique()
dp_interval1 = dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"].isin(acct_list)]
temp = dp_interval1.groupby('ANON_SERVPNT_ID').count()

temp = temp.reset_index()
temp = temp.loc[temp["usg_dt"] == 8760]

acct_lists = temp["ANON_SERVPNT_ID"]

dp_interval1 = dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"].isin(acct_lists)]
#print "dp interval", dp_interval1
dp_interval1 = dp_interval1[["ANON_SERVPNT_ID","usg_dt", "INT_HOUR", "base"]]
dp_interval1.base = np.where(dp_interval1.base < 0, 0,dp_interval1.base)

unique_rows = dp_interval1["ANON_SERVPNT_ID"].unique()

##add SH/WH/PV
with_sh = False
with_wh = False
with_pv = False
 
plt.figure(figsize = (10,10))
x = range(0,12)
colors = ['y','orange','cyan','pink','violet','lightgreen', 'lightblue','b','r','darkred','darkblue','darkgrey', 'k']

p = []  #energy at diff percentiles
k = []  #acct_ids

group_tot = dp_interval1.groupby("ANON_SERVPNT_ID").sum()
group_tot = group_tot.reset_index()
group_tot = group_tot[["ANON_SERVPNT_ID", "base"]]   #Grouped based on total annual energy

ID = []
totalConsumption = []
totalnetDemand = []
totalPVGen = []
excess_PVGen = []
NEM_Income1 = []
NEM_Income2 = []
totalengcost1 = []
totalengcost2 = []
homes_energy1 = {}   #results for a home on rate structure 1
homes_energy2 = {}   #results for a home on rate structure 2

df_eng = pd.DataFrame() 
df_cost = pd.DataFrame()
##df_eng.index = range(0,12)
##df_cost.index = range(0,12)
## SMall, Med, Large Usage homes (149410111,148010084, 74510037)
#list_of_Med Users IDs = (81310050,148010084, 103410018, 17210022 ,83610114,257210059, 179210079,230010054, 98910029,31310110,114410058,209710007	141710079)
i = 0
for j in (149410111,148010084, 74510037):  #len(unique_rows)):
   
    print "unique", j
    homes_energy1[i] = j  #unique_rows[i]
    homes_energy2[i] = j #unique_rows[i]
    ID.append(j)
    df = dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"] ==j]
    df1 = df[['ANON_SERVPNT_ID','base']]
    df1.index = range(0, 8760)   ##create the index with 0 through 8759 here.
    
    if with_sh == True:
        sh_df.columns = [["SH"]]
        df1["SH"] = sh_df.loc[:,"SH"].values

    if with_wh == True:
        wh_df.columns = [["WH"]]
        df1["WH"] = wh_df["WH"].values
            
    if with_pv == True:
        pv_df.columns = [["PV"]]
    
        df1["PV"] = pv_df["PV"].values* pv_size/1000

    house = House(df1, startDate)
    df1 = house.getAllDataDf()
    homes_energy1[i] = getAnnualEnergyCost_cumdem(house,R1, i)
    homes_energy2[i] = getAnnualEnergyCost_cumdem(house,R2, i)
#    print "test", homes_energy1[i]['TotalConsumption']
#    df_eng.loc[i] = homes_energy1[i]['TotalConsumption']
#    df_cost.loc[i] = homes_energy1[i]['Energy_Cost']
#    print "df", df_eng, df_cost
    
    totalConsumption.append(homes_energy1[i]['TotalConsumption'].sum())
    totalnetDemand.append(homes_energy1[i]['NetDemand'].sum())
    totalPVGen.append(homes_energy1[i]['TotalPVGen'].sum())
    excess_PVGen.append(homes_energy1[i]['excess_PVGen'].sum())
    NEM_Income1.append(homes_energy1[i]['NEM_Income'].sum())
    totalengcost1.append(homes_energy1[i]['Energy_Cost'].sum())
    maxdata = getMax(df1, "base")
    print "max data", maxdata[0], maxdata[1]
   
##    totalConsumption.append(homes_energy2[i]['TotalConsumption'].sum())
##    totalnetDemand.append(homes_energy2[i]['NetDemand'].sum())
##    totalPVGen.append(homes_energy2[i]['TotalPVGen'].sum())
##    excess_PVGen.append(homes_energy2[i]['excess_PVGen'].sum())
    NEM_Income2.append(homes_energy2[i]['NEM_Income'].sum())
    totalengcost2.append(homes_energy2[i]['Energy_Cost'].sum())
  #  print "home1_energy",i,  homes_energy[i]['Energy_Cost'].sum()
  #  print "engcost", NEM_Income1, NEM_Income2, len(NEM_Income1),len(NEM_Income2)
    i +=1

result_df = pd.DataFrame(data = {'ID': ID,
                                  'TotalConsumption': totalConsumption,
                                        'NetDemand':   totalnetDemand,
                                        'TotalPVGen': totalPVGen,
                                        'excess_PVGen': excess_PVGen,
                                        'NEM_Income_R1':  NEM_Income1,
                                         'Energy_Cost_R1': totalengcost1,
                                          'NEM_Income_R2':  NEM_Income2,
                                         'Energy_Cost_R2': totalengcost2
                                 })

result_sorted_df = result_df.sort_values( by=['TotalConsumption'])
result_sorted_df.to_csv('DPV_3sizedHHs_' + 'PGE_D_E_'+ 'Base.csv')

##dfmap = df_eng
##plt.imshow(dfmap, cmap ="RdYlBu")
##plt.colorbar()
##plt.xticks(range(len(dfmap)), dfmap.columns)
##plt.yticks(range(len(dfmap)), dfmap.columns) 

##dfmap1 = result_df[['Energy_Cost_R1']]
##plt.imshow(dfmap1, cmap ="RdYlBu")
##plt.colorbar()
##plt.xticks(range(len(dfmap1)), dfmap1.columns)
##plt.yticks(range(len(dfmap1)), dfmap1.columns) 

##result_sorted_df = result_df.sort_values( by=['TotalConsumption'])
##result_sorted_df.to_csv('DPV_AllHomes_' + 'SCE_'+ 'Base_ascending.csv')
##
##plt.show()
##plt.show()

#new_df = result_sorted_df.iloc[0,:]
#print "new_df", new_df

#print "results", totalnetDemand, totalengcost               
    
##month_total = []
##month_max = []
##plt.figure(figsize = (10,10))
##x = range(0,12)
##for i in range (0,12):
##   
##    data = house.getMonthDf( month_names[i])
##    print "data sum",i, data['base'].sum()
##    month_total.append( data['base'].sum())
##    month_max.append(data['base'].max())
##     
##   # plt.plot( i, data['base'].sum(), color ='red', linewidth = 2)
###plt.plot( x, month_total, color ='red', linewidth = 2)
##plt.plot(x, month_max, color = 'blue', linewidth= 2)
##
