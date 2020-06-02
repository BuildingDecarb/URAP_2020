from AJ_RateCalculator import *

#def graphByCat(categories):
 #   plt.figure(figsize = (20,11)) 

##    plt.subplot(2, 2, 1)
##    graphflat(categories)
##    plt.title("Flat Plan")
##
##    plt.subplot(2, 2, 2)
##    graphtier(categories)
##    plt.title("Tiered Plan")
    
  #  plt.subplot(1, 1,1)
  #  graphtou(categories)
  #  plt.title("Time of Use Plan")
    
    

##    plt.subplot(2, 2, 4)
##    graphflat(categories)
##    graphtier(categories)
##    graphtou(categories)
  #  plt.title("All")
    
 #   plt.show()

def graphflat(categories):
    x = range(1, 13)
    runningMonthSum = np.zeros(12)
    for cat in categories:
        flatcost = flat(cat)[1]  
        for i in range(0, 12):
            runningMonthSum[i] = runningMonthSum[i] + flatcost[i]
    plt.plot(x, runningMonthSum, label = cat.name + ", flat")
   #     print "test1 \n", cat.name, runningMonthSum    
    plt.legend()
    plt.grid(True)
   # plt.xlabel("Month")
    plt.ylabel("$")

def graphtier(categories):
    x = range(1, 13)
    runningMonthSum = np.zeros(12)
    for cat in categories:
        tiercost = tier(cat)[1]
        for i in range(0, 12):
            runningMonthSum[i] = runningMonthSum[i] + tiercost[i]
    plt.plot(x, runningMonthSum, label = cat.name + ", tiered")
      #  print "test2 \n", cat.name, runningMonthSum
    plt.legend()
    plt.grid(True)
   # plt.xlabel("Month")
    plt.ylabel("$")


def graphtou(categories, legend = ""):
    x = range(1, 13)
    runningMonthSum = np.zeros(12)
    for cat in categories:
        toucost = tou(cat)[1]
        for i in range(0, 12):
            runningMonthSum[i] = runningMonthSum[i] + toucost[i]
     #   print "test", cat.name, runningMonthSum         
    plt.plot(x, runningMonthSum, label = legend + ": TOU Rate")
   
    plt.legend()
    plt.grid(True)
#    plt.xlabel("Month")
    plt.ylabel("$")   

categwh = [wh_year]
catwh = grandSum(categwh)
categWH = [catwh]

categsh = [sh_year]
catsh = grandSum(categsh)
categSH = [catsh]

categ = [sh_year, wh_year] 
heating = grandSum(categ)
categheat = [heating]

categcool = [cool_year]
cooling = grandSum(categcool)
categcool = [cooling]

categ1 = [ df_year ]
baseload = grandSum(categ1)
categbase = [baseload]

allcateg = [ sh_year, wh_year,cool_year,df_year ]
total = grandSum(allcateg)
categtotal = [total]

toubase = tou(baseload)[1]
toucool = tou(cooling)[1]
touwh= tou(catwh)[1]
toush = tou(catsh)[1]

tierbase = tier(baseload)[1]
tiercool = tier(cooling)[1]
tierwh= tier(catwh)[1]
tiersh = tier(catsh)[1]

print "Tiered Cost", tier(baseload)[0],tier(cooling)[0],tier(catwh)[0],tier(catsh)[0]
print "Tou Cost", tou(baseload)[0],tou(cooling)[0],tou(catwh)[0],tou(catsh)[0]
print "\n %", (tier(baseload)[0]-tou(baseload)[0])/tier(baseload)[0],  (tier(cooling)[0] - tou(cooling)[0])/tier(cooling)[0]
print "% ", (tier(catwh)[0]- tou(catwh)[0])/tier(catwh)[0], (tier(catsh)[0]-tou(catsh)[0])/tier(catsh)[0]
##
#print "WH & SH", toubase,touwh, toush

##STacked graph of TOU
plt.figure(figsize = (20,11))
plt.title("Monthly cost of Electricity for SCEN")
x = range(1,13)
plt.stackplot(x,toubase,toucool, touwh,toush, labels=['baseload','cooling','waterheating','spaceheating'])
plt.legend(loc='upper left')
plt.xlabel("Month")
plt.ylabel("Average Cost of Electricity by TOU($)")
plt.show()


##STacked graph of TIER
plt.figure(figsize = (20,11))
plt.title("Monthly cost of Electricity for SCEN")
x = range(1,13)
plt.stackplot(x,tierbase,tiercool, tierwh,tiersh, labels=['baseload','cooling','waterheating','spaceheating'])
plt.legend(loc='upper left')
plt.xlabel("Month")
plt.ylabel("Average Cost of Electricity Tiered ($)")
plt.show()

#Electricity demand Stacked graph

plt.figure(figsize = (20,11))
plt.title("Monthly Electricity Demand SCEN")
x = range(1,13)

monthbase = EnergyYear(baseload, monthbeg)[1]
monthcool = EnergyYear(cooling, monthbeg)[1]
monthwh = EnergyYear(catwh, monthbeg)[1]
monthsh = EnergyYear(catsh, monthbeg)[1]


print "MONTHLY BASELOAD", monthbase
#monthwh = EnergyYear(catwh, monthbeg)
           
plt.stackplot(x,monthbase,monthcool,monthwh,monthsh, labels=['baseload', 'cooling','waterheating', 'spaceheating'])
plt.legend(loc='upper left')
plt.xlabel("Month")
plt.ylabel("Average Monthly Demand(kW)" )
plt.show()

##
### TOU Cost by category Graph
##plt.figure(figsize = (20,11))
##plt.title("Monthly cost of Electricity for SCEN_May12")
##graphtou(categheat, "heating")
##graphtou(categcool, "cooling")
##graphtou(categbase, "baseload")
##graphtou(categtotal, "aggregate")
##plt.show()
##


annbase = 0
for day in baseload.daylist:
        annbase += sum(day.use)
print "\n ann base energy", annbase 
#print "\n cost", anneng, flat(total)[0], tier(total)[0], tou(total)[0]

anncool = 0
for day in cooling.daylist:
        anncool += sum(day.use)
print "ann cooling energy", anncool

annheat = 0
for day in heating.daylist:
        annheat += sum(day.use)
print "ann heating energy", annheat        

anneng = 0
for day in total.daylist:
        anneng += sum(day.use)
print "\n Total ann energy", anneng

#graphByCat(categ_total)
#graphByCat(allcateg)

##plt.figure(figsize = (20,11)) 
##
##plt.subplot(3, 1, 1)
##graphtou(categheat,"heating")
##graphtou(categcool, "cooling")
###plt.title("Heating TOU Rates")
##
##plt.subplot(3, 1, 2)
##graphtou(categbase, "baseload")
###plt.title("Base Load TOU Rates")
##
##plt.subplot(3 ,1,3)
##graphtou(categtotal, "total Load")
###plt.title("Combined Load TOU Rates")
##plt.show()
