from AJ_RateCalculator import *
from AJ_RateGraphing import *

categories = [sh_year, wh_year, cool_year,df_year] #  [cool_year, pool_year, df_year, sh_year, wh_year]
total_year = grandSum(categories)

categ1 = [ cool_year,df_year ]
no_baseload = grandSum(categ1)

def graphByCat(categories):
    plt.figure(figsize = (20,11)) 
    plt.subplot(3, 2, 1)
    graphflat(categories)
    plt.title("Fixed Plan")

    plt.subplot(3, 2, 2)
    graphtier(categories)
    plt.title("Tiered Plan")
    
    plt.subplot(3, 2, 3)
    graphtou(categories)
    plt.title("Time of Use Plan")
    
    plt.subplot(3, 2, 5)
    graphflat([no_baseload])
    graphtier([no_baseload])
    graphtou([no_baseload])
    plt.title("Cost of Energy excl heating")
    
    plt.subplot(3, 2, 6)
    graphflat([total_year])
    graphtier([total_year])
    graphtou([total_year])
    plt.title("Total Energy Cost Including Heating")


    
    plt.show()


graphByCat(categories)
