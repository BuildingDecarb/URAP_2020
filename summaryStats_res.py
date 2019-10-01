import pandas as pd

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

    #summary_df['kwh_ann_tot'] = summary_df['kwh_ann_tot'].apply(lambda x: int(x.strip().replace(',', '')))
    summary_df['customer_count'] = summary_df['customer_count'].apply(lambda x: int(x.strip().replace(',', '')))
   # print(summary_df.dtypes)

    sectors = ['res']
    car = ['Care', 'nonCare']
    utils = ['pge', 'sce', 'sdge']
    #kwbin =['0.5_0.6' ] #  , '0.0_0.1', '0.1_0.2', '0.2_0.3', '0.3_0.4', '0.4_0.5']

    query_df = summary_df[
        (summary_df['sector'].isin(sectors)) &   #if sectors name is in 'sector' 
        (summary_df['care'].isin(car)) & 
         # (summary_df['kwh_bin'].isin(kwbin)) & 
        (summary_df['util'].isin(utils)) &
      #   (summary_df['kwh_bin'].isin(bins)) &
        (True) # for ease of adding/removing conditions above
    ]

    for i, row in query_df.iterrows():
       # print "test", i, "+cluster", folder      
    #    print "cluster", row["cluster"]
        clust = row["cluster"]
        filename = folder + "/" + clust + ".csv"
   #     print "filename", i, filename
        cluster_df = pd.read_csv(filename)   #for every file
        #print "cluster_df", cluster_df
        for col in cluster_df.columns:   #read the relevant columns
           # sum_cols.add(col_sum)
    #        print "col", col
            query_df.loc[i, col + "_sum"] = cluster_df[col].sum()
          #  hourly_demand = cluster_df[col]
   # print "test1", query_df.head(5)   
    query_df =  query_df.drop(query_df.columns[query_df.columns.str.contains('Unnamed',case = False)],axis = 1)
    query_df = query_df.drop([ 'poolpump_penetration','battery_kwh_per_customer', 'hour_ending_sum', 'poolpump_sum'], axis =1)

    query_df.to_csv("WH_Output" + "/" + 'res_summary_Feb4.csv')



           
        

    


