#AmyJiang's
#Annual energy use by source

from AJ_SumDataFrames import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches

## Graphing residential energy use by end-use

def EnergyYear(category, monthdays):
    """
    Compute Monthly average energy use by category by month for each month in the year. Categories are additive.
    Parameters:
        categories (Year[]): array of Years of different energy sources
        yeardays (int[]): the index number of first day of each month, out of the total days in the year 
    """
    totaluse = 0
    i= 1
    tot = 0
    monthlyuse = []
    for day in category.daylist:
        tot = tot + sum(day.use)
       # print "TESTTEST, totaluse", day.use, tot
        if i in monthend:
             #   print "\n  monthend test", i, tot
                monthlyuse.append(tot)
                totaluse += tot
                tot = 0
        i +=1
      #  print "i, totaluse", i, totaluse
    totaluse = sum(monthlyuse)
    return totaluse, monthlyuse    
    
def graphYear(categories, monthdays):
    """
    Graphs hourly energy use by category by month for each month in the year. Categories are additive.
    Parameters:
        categories (Year[]): array of Years of different energy sources
        yeardays (int[]): the index number of first day of each month, out of the total days in the year 
    """
   # plt.figure(figsize = (20,20))
   # plt.suptitle("Heating & Cooling Hourly Profiles: CZ16")
    for i in range(1, len(monthdays) + 1):
        plt.subplot(6, 2, i)
        plt.ylabel('kWh', fontsize = 10)
        if i == 12:
            hrAvg = monthAvg(categories, monthdays[i-1], 366)
            graphMonth(categories, hrAvg, i)
            
        else: 
            hrAvg = monthAvg(categories, monthdays[i-1], monthdays[i])
            graphMonth(categories, hrAvg,i)
        
        plt.grid(True)
        plt.title(monthnames[i - 1], fontsize = 10)
    plt.show()

def graphMonth(categories, categoryHrAvg, month):
    """
    Helper function to graph hourly energy use by category in a month. 
    """
    col = [ 'm','b','g','orange','black']
    x = range(1, 25)
    runningSum = 0
    for i in range(0, len(categories)):
        #print "categories ", len(categories), categories[i].name
        plt.plot(x,  categoryHrAvg[i],  color = col[i],linewidth = 1.0 )
        if month ==12:
             plt.plot(x,  categoryHrAvg[i],  color = col[i], label = categories[i].name, linewidth = 0.75)
        if(categories[i].name <> 'PV Profile'):    
           runningSum += categoryHrAvg[i]
    ylim(0,2.5)       
   # plt.plot(x, runningSum,  'k-.', label= 'Total H&C', linewidth = 1.0)
    plt.legend()
    plt.savefig('plots1/' + 'CZ16_HC_PVSize_'+str(pv_size) + '(kW).png')
            
def monthAvg(categories, monthBeg, monthEnd):
    """i    Helper function to average energy use by hour. 
    """
    categoryHrAvg = []
    for x in categories:
        month = x.daylist[monthBeg:monthEnd]
        hourlyAvg = np.zeros(24)
        for i in range(0, len(month)):
            for j in range(0, 24):
                hourlyAvg[j] = hourlyAvg[j] + month[i].use[j]
        hourlyAvg = hourlyAvg/len(month)
        categoryHrAvg.append(hourlyAvg)
    return categoryHrAvg

def graphingMonth(categories, month, yeardays):
    
    plt.figure(figsize = (20,20))
    plt.suptitle("Heating & Cooling Hourly Profiles: CZ16 for month =%0.f " %month, fontsize =30)
    plt.ylabel('kWh', fontsize = 20)
    col = [ 'red','blue','green','orange','black']
    
    if month == 12:
        hrAvg = monthAvg(categories, yeardays[month-1], 366)
    else: 
        hrAvg = monthAvg(categories, yeardays[month-1], yeardays[month])
       
 # print "testTEST", i, len(yeardays)
   
    x = range(1, 25)
    runningSum = 0
    for j in range(0, len(categories)):
        
        plt.plot(x,  hrAvg[j],  color = col[j], label = categories[j].name, linewidth = 2.5  )
      #  if j == 3:
      #      print j, categories[j].name, hrAvg[j]
        if(categories[j].name <> 'PV Profile'):    
            runningSum += hrAvg[j]

    ylim(0,2.5)       
    plt.plot(x, runningSum,  'k-.', label = 'Total demand', linewidth = 2.5)
    legend([mpatches.Patch(color='red'), mpatches.Patch(color='blue'),mpatches.Patch(color= 'green'),mpatches.Patch(color= 'orange'),mpatches.Patch(color= 'k')],\
            [categories[0].name,categories[1].name,categories[2].name, categories[3].name, 'Total demand'], loc =1, ncol = 1,fontsize = 15) 

    plt.savefig('plots1/' + "month_"+ str(month) + 'PVSize_'+ str(pv_size)+ 'kW_CZ16_HC_April16.png')






#graphYear(categories, monthbeg)
#plt.figure(figsize = (20,11))
#plt.title("Average hour demand")
#graphYear(categ1, monthbeg)
#graphYear(categ2, monthbeg)
#graphYear(categ3, monthbeg)
#plt.show()
#graphingMonth(categories,12, year)
#graphingMonth(categories,8, year)



