import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *


#Calculate the average "statistic" for each building type
def avg_statistic_per_bldgtype(cnty, name, building_type, statistic, ylabel, title):
    
    from matplotlib.pyplot import figure
    avg_datas = np.array([], dtype=np.float64)
    building_count = []
    
    
    print "# of builidngs", cnty[building_type].unique().size , statistic
    for i in range(cnty[building_type].unique().size):
        
        
        bldgtype = cnty[building_type].unique()[i]
        avg_data = cnty[cnty[building_type]==bldgtype][statistic].mean(skipna=True)
        building_count.append(cnty[cnty[building_type]==bldgtype][statistic].count())
        
        print "cnt", bldgtype, avg_data, building_count[i]
        avg_datas = np.append(avg_datas, avg_data)

    fig1 = plt.figure(figsize=(18, 6))
    plt.title(title)
    plt.xlabel("Building Type")
    plt.ylabel(ylabel, fontsize = 12)
    bars = plt.bar(cnty[building_type].unique(), avg_datas)
    i = 0
    for bar in bars:
       
        yval = bar.get_height()
        plt.text(bar.get_x()+0.3, yval + (yval*0.01), str(building_count[i]))# + " Buildings")
        i += 1

    fig1.tight_layout()
   # plt.show()
    
    fig1.savefig('plots/'+ name +  statistic +  '_March71fig.png')  
    return avg_datas

#
def avg_statistic_per_bldgtype_no_plot(cnty, building_type, statistic):
    from matplotlib.pyplot import figure
    avg_datas = np.array([], dtype=np.float64)
    building_count = []
 

    for i in range(cnty[building_type].unique().size):
        bldgtype = cnty[building_type].unique()[i]
        avg_data = cnty[cnty[building_type]==bldgtype][statistic].mean(skipna=True)
        building_count.append(cnty[cnty[building_type]==bldgtype][statistic].count())
        avg_datas = np.append(avg_datas, avg_data)
        i += 1
        
    
    return avg_datas, building_count



