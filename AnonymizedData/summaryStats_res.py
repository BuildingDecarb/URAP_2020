import pandas as pd
from buildingtest import Building
from datetime import datetime, timedelta
from calendar import monthrange
from datetime import date
import numpy as np
from matplotlib.pyplot import cm 
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as mpatches #for stack plots
import pandas as pd
import numpy as np
from numpy import *

#thie code looks up the total customer country from the annnoymous summary and then goes through the directory of load profiles and computes the total for
#each sub-category..and summarizes in the summary file

if __name__ == "__main__":
    folder = 'anonymized_1in10_actual_actual_2014'
   # print "folder", folder
    summary_file = folder + "/"  + folder + "_cluster_summary.csv"
   # print "file1", summary_file
    summary_df = pd.read_csv(summary_file)
  #  print "Begin", summary_df.columns
    summary_df = summary_df.drop(['cluster_oldname', 'weather_station', 'bev_count', 'bev_work_count','phev_count', 'phev_work_count' ], axis =1)
       
    loads = dict()
    #summary_df['kwh_ann_tot'] = summary_df['kwh_ann_tot'].apply(lambda x: int(x.strip().replace(',', '')))
    summary_df['customer_count'] = summary_df['customer_count'].apply(lambda x: int(x.strip().replace(',', '')))
   # print(summary_df.dtypes)

    sectors = ['res']
    car = ['Care']
   # utils = ['pge', 'sce', 'sdge']
    utils1 =['sce']
    slaps = ['SCEN']
    bins =['0.6_0.7' ] #  , '0.0_0.1', '0.1_0.2', '0.2_0.3', '0.3_0.4', '0.4_0.5']

    query_df = summary_df[
        (summary_df['sector'].isin(sectors)) &   #if sectors name is in 'sector' 
        (summary_df['care'].isin(car)) & 
         # (summary_df['kwh_bin'].isin(kwbin)) & 
        (summary_df['util'].isin(utils1)) &
        (summary_df['slap'].isin(slaps)) &
        (summary_df['kwh_bin'].isin(bins)) &
        (True) # for ease of adding/removing conditions above
    ]
    year = 2014
    for i, row in query_df.iterrows():
    #    print "test", i, "+cluster", folder      
    #    print "cluster", row["cluster"]
        clust = row["cluster"]
        slaps = row['slap']

        filename = folder + "/" + clust + ".csv"
        cluster_df = pd.read_csv(filename)   #for every file
        customer_cnt = row["customer_count"]

        print "countcountcount", customer_cnt, filename
        p1 = []
        for col in cluster_df.columns:   #read the relevant columns
         #   print "TESTETSER"
            query_df.loc[i, col + "_sum"] = cluster_df[col].sum()
            hourly_demand = cluster_df[col]
           
            name = col + "_loads"
       #     print "test1 Col Name", col, name, hourly_demand[2] 
          #  loads[(name,year)]  = Building(name, 0,  hourly_demand)  #load profile for that year
            decile = row["kwh_bin"]
            
           

            if name == "cooling_loads":
             #   print " \n TESETTESTE", decile
                loads[(name,year)]  = Building(name, 0,  hourly_demand)   #load profile for that year
                
                dailyload1 = loads[(name,year)]
                fig1 = plt.figure(figsize = (10.0,6.0))
                cust_cnt = 1.0/customer_cnt
                for j in range(1,13):
                     
                         fig1.add_subplot(4,3,j)
                        
                         
                         monthlyload1 = [ cust_cnt * x for x in  dailyload1.avg_hourly( month =j) ] ##avged over days of the the entire month..
        
                         b1 = plt.plot(monthlyload1, color = 'b', label = slaps+ "_Care"+ "_"+ decile + "_" + name)
                       
                         p1.append([b1])
                 
                plt.legend(ncol=2, fontsize = 8)
                plt.tight_layout(pad=.0001,w_pad=.001,h_pad=.001)  
                fig1.tight_layout()
                fig1.savefig('plots1/'+ name +  "_"  + slaps+"_Care_"+ decile +  '_fig.png')  

            
          #  hourly_demand = cluster_df[col]
   # print "test1", query_df.head(5)   
    query_df =  query_df.drop(query_df.columns[query_df.columns.str.contains('Unnamed',case = False)],axis = 1)
   # query_df = query_df.drop([ 'hvac_penetration', 'weather_station','bev_count','bev_work_count','phev_count','phev_work_count','poolpump_penetration','battery_kwh_per_customer', 'hour_ending_sum', 'poolpump_sum'], axis =1)

    query_df.to_csv('res_SCEN_Care_0.6_0.7_CoolingLoads_Feb17_2020.csv')



           
        

    


