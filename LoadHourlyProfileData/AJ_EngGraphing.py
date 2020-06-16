#AmyJiang's
#Annual energy use by source

from AJ_SummarizeDataFrames import *
from LoadCategories import *
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
    hrAvg = []
   # plt.figure(figsize = (20,20))
    plt.suptitle("Heating & Cooling Hourly Profiles: CZ13")
    for i in range(1, len(monthdays) + 1):
        
        plt.subplot(6, 2, i)
        plt.ylabel('kWh', fontsize = 10)
        if i == 12:
            hrAvg = monthAvg(categories, monthdays[i-1], 366)
            graphMonth(categories, hrAvg, i)
            
        else:
       #     print "graphYear non Leap",i, monthdays[i], monthdays[i-1]
            hrAvg = monthAvg(categories, monthdays[i-1], monthdays[i])
            graphMonth(categories, hrAvg,i)
        
        plt.grid(True)
        plt.title(monthnames[i - 1], fontsize = 10)
    plt.savefig('plots1/' + 'HourlyProfiles_CZ13_PV_'+str(pv_size) + '(kW)_june15.png')

    #plt.show()

def graphMonth(categories, categoryHrAvg, month):
    """
    Helper function to graph hourly energy use by category in a month. 
    """
    col = [ 'red','blue','green','cyan', 'orange']
    x = range(1, 25)
    runningSum = 0
    for i in range(0, len(categories)):
        #print "categories ", len(categories), categories[i].name
        plt.plot(x,  categoryHrAvg[i],  color = col[i],linewidth = 1.0 )
        if month ==12:
             plt.plot(x,  categoryHrAvg[i],  color = col[i], label = categories[i].name, linewidth = 0.75)
             legend([mpatches.Patch(color='red'), mpatches.Patch(color='blue'),mpatches.Patch(color= 'green'),mpatches.Patch(color= 'cyan'),mpatches.Patch(color= 'orange')],\
                   [categories[0].name,categories[1].name,categories[2].name, categories[3].name,categories[4].name ], loc =1, ncol = 1,fontsize = 15) 
     
        if(categories[i].name <> 'PV Profile'):    
           runningSum += categoryHrAvg[i]
    ylim(0,2.25)       
    plt.plot(x, runningSum,  'k-.', label= '', linewidth = 1.0)  # plots the total aggregate
    

 #   plt.legend()
   # plt.savefig('plots1/' + 'month_'+ str(month)+'CZ13_HC_PVSize_'+str(pv_size) + '(kW).png')
            
def monthAvg(categories, monthBeg, monthEnd):
    """i    Helper function to average energy use by hour. 
    """
    categoryHrAvg = []
   
    for cat in categories:
       
        month = cat.daylist[monthBeg:monthEnd]
        hourlyAvg = np.zeros(24)
        for i in range(0, len(month)):
            for j in range(0, 24):
                hourlyAvg[j] = hourlyAvg[j] + month[i].use[j]
        hourlyAvg = hourlyAvg/len(month)
        categoryHrAvg.append(hourlyAvg)
    return categoryHrAvg

def graphingMonth(categories, month, yeardays):
    
    plt.figure(figsize = (20,20))
    plt.suptitle("Heating & Cooling Hourly Profiles: CZ13 for month =%0.f " %month, fontsize =30)
    plt.ylabel('kWh', fontsize = 20)
    col = [ 'red','blue','green','cyan', 'yellow']
    
    if month == 12:
        hrAvg = monthAvg(categories, yeardays[month-1], 366)
    else: 
        hrAvg = monthAvg(categories, yeardays[month-1], yeardays[month])
       
 # print "testTEST", i, len(yeardays)
   
    x = range(1, 25)
    runningSum = 0
    for j in range(0, len(categories)):
        
        plt.plot(x,  hrAvg[j],  color = col[j-1], label = categories[j].name, linewidth = 1.5  )
      #  if j == 3:
      #      print j, categories[j].name, hrAvg[j]
        if(categories[j].name <> 'PV Profile'):    
            runningSum += hrAvg[j]

    ylim(0,2.25)       
    plt.plot(x, runningSum,  'k-.', label = 'Total demand', linewidth = 2.5)
    legend([mpatches.Patch(color='red'), mpatches.Patch(color='blue'),mpatches.Patch(color= 'green'),mpatches.Patch(color= 'orange'),mpatches.Patch(color= 'k')],\
            [categories[0].name,categories[1].name,categories[2].name, categories[3].name, 'Total demand'], loc =1, ncol = 1,fontsize = 15) 

    plt.savefig('plots1/' + "month_"+ str(month) + 'PVSize_'+ str(pv_size)+ 'kW_CZ13_HC_June10.png')



#categories, categories are all defined
# in LoadCategories.py


monthbase = EnergyYear(baseload, monthbeg)[1]
monthcool = EnergyYear(cooling, monthbeg)[1]
monthwh = EnergyYear(catwh, monthbeg)[1]
monthsh = EnergyYear(catsh, monthbeg)[1]
monthpv = EnergyYear(pvprofile,monthbeg)[1]

print "Annual total energy (kWh)", EnergyYear(baseload, monthbeg)[0],EnergyYear(cooling, monthbeg)[0], EnergyYear(pvprofile,monthbeg)[0]

#print "MONTHLY BASELOAD", monthbase


#Monthly Electricity demand Stacked graph
plt.figure(figsize = (20,11))
plt.title("Monthly Electricity Demand SCEN")
x = range(1,13)           
plt.stackplot(x,monthbase,monthcool,monthwh,monthsh, labels=['baseload', 'cooling','waterheating', 'spaceheating'])
plt.plot(x,monthpv, color = 'yellow', label = 'solarpv_output',linewidth = 2.5)
plt.legend(loc='upper left')
plt.xlabel("Month")
plt.ylabel("Average Monthly Demand(kW)" )
plt.savefig('plots1/' + 'PVSize_'+ str(pv_size)+ 'kW_CZ13_June15.png')
#plt.show()

#Average da1ly electricity demand for 12 months
newcateg = [ base_year, cool_year, sh_year,wh_year,pv_year]
graphYear(newcateg,monthbeg)


##
##anncool = 0
##for day in cooling.daylist:
##        anncool += sum(day.use)
##print "ann cooling energy", anncool
##
##annheat = 0
##for day in heating.daylist:
##        annheat += sum(day.use)
##print "ann heating energy", annheat        
##
##annbaseeng = 0
##for day in total.daylist:
##        anntotaleng += sum(day.use)
##print "\n Total ann total energy", anntotaleng
##
##annneteng = 0
##for day in total.daylist:
##        anntotaleng += sum(day.use)
##print "\n Total ann total energy", anntotaleng




