#AmyJiang's code
#The doc that stores information about the total number of customers in each dataset.
from AJ_Day_Year_Class import *

folder = 'anonymized_1in10_actual_actual_2014'  #EDIT THIS TO READ THE RIGHT FILE..in the anonymized data folder.
summary_file = folder + "/"  + folder + "_cluster_summary.csv"  
customersumm = pd.read_csv(summary_file, index_col=1, header=0)
##______CLIMATE ZONE-----------------
###############################################

##-------------------------------------
#The doc that stores energy use data. 
#filename =  'pge-res-PGF1-res_misc-noKW-nonCare-0.4_0.5' #change to appropriate filename WITHOUT .csv tag
filename  = 'sce-res-SCEN-res_misc-noKW-nonCare-0.4_0.5'
customers = customersumm.loc[filename, 'customer_count']
customers = float(customers.replace(',', ''))
cust_cnt = 1.0/customers

sh = "HP_SH_HourlyProfiles.csv"         
wh = "HP_WH_HourlyProfiles.csv"
filename = folder + "/" + filename + '.csv'
df = pd.read_csv(filename)
df = df * cust_cnt    #energy demand per household


print "Inputs", customers,climatezone, pv_size

filename = 'PVCellData' + "/" + "CZ13Fresno_Solar.csv"
df_pv = pd.read_csv(filename)
print "testtest", df_pv.loc[12,'AC System Output (W)']
pv_year = Year(pv_size*df_pv/1000.0, 'PV Profile','AC System Output (W)')
pv_year.distributeSeason()
pv_year.distributeWeekday(jan1)

#Sets up energy use Year for the base load, with cooling and pool pump use subtracted. 
df['base'] = df['total'] - df['cooling'] #- df['pboolpump']
base_year = Year(df, "Base Load", 'base')    #this is a class defined in Day_Year_Class which assigns to days and months
base_year.distributeSeason()
base_year.distributeWeekday(jan1)

#Energy use Year for cooling.
cool_year = Year(df, "Cooling", 'cooling')
cool_year.distributeSeason()
cool_year.distributeWeekday(jan1)

#Energy use Year for pool pump. 
pool_year = Year(df, "Pool Pump", 'poolpump')
pool_year.distributeSeason()
pool_year.distributeWeekday(jan1)

#Energy use Year for space heating.
df_sh = pd.read_csv(sh)
sh_year = Year(df_sh, "Space Heating", climatezone)
sh_year.distributeSeason()
sh_year.distributeWeekday(jan1)

#Energy use Year for water heating.
df_wh = pd.read_csv(wh)
wh_year = Year(df_wh, "Water Heating", climatezone)
wh_year.distributeSeason()
wh_year.distributeWeekday(jan1)



