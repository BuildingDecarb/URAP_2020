#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from DP_EnergyCalculator1 import *

plt.style.use('fivethirtyeight')
sns.set_context("notebook")
import datetime

startDate = datetime.datetime(2019, 1, 1)

thisrate = Rate_Struct()
thatrate = Rate_Struct_C()
climatezone = '13'



#folder = 'DosPalos'
#results = folder + "/" + 'DP_Results'
main = 'DP_Main.csv'
interval = 'DP_IntervalData.csv'


sh = "HP_SH_HourlyProfiles.csv"
wh = "HP_WH_HourlyProfiles.csv"

sh_df = pd.read_csv(sh, usecols= [climatezone])

wh_df = pd.read_csv(wh, usecols= [climatezone])

pv = "13_Fresno.csv"
pv_col = "AC System Output (W)"
pv_df = pd.read_csv(pv, usecols = [pv_col])



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
with_sh = True
with_wh = True
with_pv = True
 ##changed from W to kWh






##print("unique_rows",  len(unique_rows))
#print "Unique row 1", dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"] == unique_rows[0]]


acct_id = []
netdemand1 = []
netdemand2 = []
maxdem = []
engcost1 = []
engcost2 = []
for i in range (0,len(unique_rows)):  #(len(unique_rows)):   # 1st servpt works ok..and 2nd one gives a error..some counting is not going through.
    
    df = dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"] == unique_rows[i]]
    
    df1 = df[['ANON_SERVPNT_ID','base']]
  
    if with_sh == True:
        sh_df.columns = [["SH"]]
        df1["SH"] = sh_df.loc[:,"SH"].values

    if with_wh == True:
        wh_df.columns = [["WH"]]
        df1["WH"] = wh_df["WH"].values
        
    if with_pv == True:
        pv_df.columns = [["PV"]]
       
        df1["PV"] = pv_df["PV"].values/1000
    

    
    
    
    house = House(df1, startDate)
    df1 = house.getAllDataDf()
             # season, date

    maxdemand = getMax(df1,'base')
    print("Monthly Energy Usage and Costs for R1 \n", i)
    result1 = getAnnualEnergyCost(house,thisrate)
    print("Monthly Energy Usage and Costs for R2 \n", i)
    result2 = getAnnualEnergyCost(house,thatrate)
    print("result", i, result1, result2)
    acct_id.append(i)
    netdemand1.append(result1[0])
    engcost1.append(result1[1])
    maxdem.append(maxdemand)

    netdemand2.append(result2[0])
    engcost2.append(result2[1])
    #print "demand & cost", i, netdemand,engcost
    results_df = pd.DataFrame(data={'ID': acct_id,
                                     'NetDemand (kWh)': netdemand1,
                                     'Max Demand (kWh)':maxdem,
                                    'Annual Energy Cost1 ($)': engcost1,
                                    'Annual Energy Cost2 ($)': engcost2                       
                                    })
results_df.to_csv('Results_AllElec_Feb23.csv')

##for i in range (len(unique_rows)):
##    df = dp_interval1.loc[dp_interval1["ANON_SERVPNT_ID"] == unique_rows[i]]
##    df = df[['ANON_SERVPNT_ID','base']]
##    #print "df", i, df
##    house = House(df, startDate)
##    df1 = house.getDateDf()   # season, date
##    maxdemand = getMax(df1,'base')  
##    print i, maxdemand
##    abovethreshold = getAboveThresholdDF(df1,'base', 10)
##    #if abovethreshold[1] >0:
##    #    print i, abovethreshold
    
    
   
