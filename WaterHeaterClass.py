#Definition of Water Heater Class and Fuel Type
from scipy.stats import weibull_min
from Inputs_Energy import *
from RefrigerantCalc import Refrigerant


#a= 0.5  #shape
#b = 10 # scale

#Years of MeanLifeTIme, when all WHs are absolutely killed

#y = range(0,21)
#r= weibull_min.cdf(y,3,loc=0,scale = b)
#print (r)

UltimYr = 15

class WaterHeater:
    
    NPV = 0
    dailyVol = 50  #gallons
   # IncTemp = 75 #temp increase in Fahr
  #  DiscRate = 0.04
    CCDiscRate = 0.04  #carbon price discount rate
    Inflation = 0.0
   
    def __init__(self,name, fuel, ef, vintage, OrigNum,  lt, IC, OM, hasRefrigerant, refrigerant = Refrigerant(), IncTemp = 75):
        self.name = name
        self.fuel = fuel
        self.ef = ef    #Efficiency
        self.vintage = vintage  #year of installation..typically assumed happens beginning of a year
        self.OrigNum = OrigNum  #Original Num is the number of waterheaters created in the 'vintage'year
        self.lt = lt    #lifetime
        self.IC = IC   #Initial Cost could be just Capex or could be Capex+initial cost to build infrastructure
        self.OM = OM  #Operations and Maintenance
        self.hasRefrigerant = hasRefrigerant
        self.refrigerant = refrigerant
        self.IncTemp = IncTemp
       # self.calcNPV()   

#computes the total annual leakage from all the (self.Num appliances during their life

    def RefLeaks(self, yr ):
        result = {}
        if (self.hasRefrigerant == True):
            leakages = self.refrigerant.RefLeakage(yr, yr+self.lt)
            for i in range( yr, yr + self.lt+1):
                result[i]=leakages[i]                
        return result

    def AvgRefLeaks(self,yr):  #in tons of CO2 eq
        result = {}
        avgleak = 0
        if (self.hasRefrigerant == True):
            result = self.RefLeaks(yr)
            #for i in range(vint, vint+ self.lt):
             #   avgleak = avgleak + result[i]/(1+CCDiscRate)**(i-vint+1)
            avgleak = sum(result.values())/self.lt
        else:
            avgleak = 0
        return avgleak    
     
    def AnnEmissions(self,yr):  #in tons  with NO REFRIGERANT
            return self.AnnualEngUsage() * self.fuel.UnitEmissions[yr]/1000
      
      
    def AnnualEmissions(self,yr):  #in tons with REFRIGERANTS
        if self.hasRefrigerant == False:
            return self.AnnEmissions(yr)
        else:
            return ( self.AnnEmissions(yr)+ self.AvgRefLeaks(yr)  )
       
    def annualizedEmissions(self, vint):  #in tons (THIS IS THE AVERAGE EMISSIONS..NOT DISCOUNTED
    
        result = {}
      #  result1 = {}
        for i in range(vint, vint+self.lt):
            result[i] = self.AnnualEmissions(i)  #INCLUDING DIRECT AND INDIRECT
       #     result1[yr] = self.AnnEmissions(yr)
        annEmis = sum(result.values())/self.lt
        return (annEmis)
        
    def MarginalAnnualEmissions(self, WH2, yr):
        return (self.AnnualEmissions(yr) - WH2.AnnualEmissions(yr) )
       
    def annualCarbonCost(self, vint, UnitCarbonPrice=20):  #$20/ton is the default rate for Carbon...if not specified when calling the func
        result = {}
        for i in range(vint, vint+self.lt):
            if self.hasRefrigerant == True:
                result[i] = UnitCarbonPrice * (self.AnnualEmissions(i)  )
            else:
                result[i] = UnitCarbonPrice * (self.AnnEmissions(i) )
        return result
    
    def averageCarbonCost(self, vint, UnitCarbonPrice=20):  
        result = {}
        result = self.annualCarbonCost(vint,  UnitCarbonPrice)
        return sum(result.values())/self.lt
    
    
    def NPVEmissions_Refrigerant(self, yr):
         if self.hasRefrigerant == True:
             result = 0
             RefLeek = self.RefLeaks(yr)
             for i in range(yr, yr+self.lt+1):
                 result = result + RefLeek[i]/(1+DiscRate)**(i-yr+1)
         else:
             result = 0
         return result   
    
    def NPVEmissions_Indirect(self, yr):
        
         result = 0
         for i in range(yr, yr+self.lt+1):
             result = result + self.AnnEmissions(i)/(1+DiscRate)**(i-yr+1)
         
         return result        
        
    def NPVEmissions(self, yr):  #NPV OF EMISSIONS USED FOR COMPUTING NPV OF CARBONCOST
     
        NPVEm = self.NPVEmissions_Indirect(yr)+ self. NPVEmissions_Refrigerant(yr)
        return NPVEm
        
    def lcc(self, yr, UnitCarbonPrice =20 ):  #levelized 
        return (self.NPVEmissions(yr)*UnitCarbonPrice + self.calcNPV(yr) )

    def totalCapex(self):      #total cost of the stock of vintage yr
        return self.OrigNum * self.IC
    
    def NPVCost(self,yr):
        NPV = self.IC
        for I in range(yr, self.lt+yr):
             NPV = NPV + (self.OM[I-yr])/(1+DiscRate)**(I-yr+1)
        return NPV
         
    def NPVEngCost(self,yr):
        NPV = 0
        for I in range(yr, self.lt+yr):

             NPV = NPV + (self.AnnualEngCost(I))/(1+DiscRate)**(I-yr+1)
        return NPV     
        
    def NPVCC(self,vint, CarbonCost= 21):  #NPV of carbon cost
        return self.NPVEmissions(vint)*CarbonCost
         
        
    def calcNPV_Capex(self, yr, Capex):  #changing capex
         NPV = Capex
         
         for I in range(yr,self.lt +yr):
              
              NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I))/(1+DiscRate)**(I-yr+1)
         return NPV
   
    def calcNPV_LifeTime(self, yr, lifetime):  #changing can specify a difff lifetime other than self.lt
         NPV = self.IC
         for I in range(yr,lifetime +yr):
              NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I))/(1+DiscRate)**(I-yr+1)
         return NPV
         
    def calcNPV(self,yr):#initial fixed capex 
         
         NPV = self.IC
         
         for I in range(yr, self.lt+ yr):
            # print I, self.OM[I-ThisYear], self.AnnualEngCost(I)
             NPV = NPV + (self.OM[I-yr] + self.AnnualEngCost(I))/(1+DiscRate)**(I-yr+1)
         return NPV
         
  
    def annualizedNPV(self,yr):
        return self.calcNPV(yr)/self.lt
        
    def lcc(self, yr, UnitCarbonPrice =20 ):  #levelized 
        return (self.NPVEmissions(yr)*UnitCarbonPrice + self.calcNPV(yr) )
        
    def Annuallcc(self, yr, UnitCarbonPrice =20 ):  #levelized 
        return ( (self.NPVEmissions(yr)*UnitCarbonPrice + self.calcNPV(yr) ) /self.lt)   
            
    def payback(self, WHx,yr):
         X = WHx.IC - self.IC
         Y =  (self.OM[0] + self.AnnualEngCost(yr)) - (WHx.OM[0] + WHx.AnnualEngCost(yr))
         #print "#", X, Y, "#"
         if self == WHx:
             return 0
         elif (X>=0 and Y<=0):
             return max(self.lt, WHx.lt)
         elif (X<0 and Y>=0):
             return 0
         else:    
             return (min(self.lt, WHx.lt, X/(Y) ))
             
    def payback1(self, WHx,yr):
         N= 1
         maxN = max(self.lt, WHx.lt)
         X = WHx.IC - self.IC
         Y =  (self.OM[0] + self.AnnualEngCost(yr)) - (WHx.OM[0] + WHx.AnnualEngCost(yr))
      #   print '\n test', X, Y
        # if X  <= 0 and Y <=0:
        #    return 0
      
        # else: 
         while N < maxN and abs(X/Y) >1 : 
                Y = Y + (self.OM[N] + self.AnnualEngCost(yr+N)) - (WHx.OM[N] + WHx.AnnualEngCost(yr+N))
                N = N +1
         if N == maxN and X/Y > 1:
                return maxN
         else:    
                return N
          
          
    def AnnualEngUsage(self):
            return self.dailyVol* self.IncTemp*self.fuel.unitEng *  365/self.ef
        
    def AnnualEngCost(self, yr):
          # if self.fuel == NG:
           #     print yr, self.fuel.UnitEngCost[inf][yr]
            return self.AnnualEngUsage() * self.fuel.UnitEngCost[yr]

   
    def compareEngUsage(self, WH2):
        return (self.AnnualEngUsage() - WH2.AnnualEngUsage())

    def compareEmissions(self,WH2):
        return(self.AnnualEmissions() - WH2.AnnualEmissions())
    
    def CCBreakEven(self, WH2, yr):  #breakeven carbon cost
         breakeven = (self.calcNPV(yr)/self.lt- WH2.calcNPV(yr)/WH2.lt)/( WH2.NPVEmissions(yr)/WH2.lt - self.NPVEmissions(yr)/self.lt )
         return breakeven
     
    def weib(self):
       
        x = range(0, self.lt+UltimYr+1)
        w = weibull_min.cdf(x,3,loc=2.5,scale = self.lt) * self.OrigNum
        #print w
        return(w)
    
    def deadsofar(self, yr):
        if yr > self.vintage and yr < self.vintage+ self.lt + UltimYr:
         #   print yr, self.vintage
            return self.weib()[yr-self.vintage]
           
        elif yr >= self.vintage + self.lt + UltimYr:
            return self.OrigNum
        else:
            return 0

    def numAlive(self,yr): 
       return (self.OrigNum - self.deadsofar(yr))
   
    def age(self, yr):
        return (yr - self.vintage)
        
    def annualreplacement(self,yr):
      #  if yr> self.vintage + (self.lt + UltimYr) or yr < self.vintage:
       #     return 0
       # else:
            return (max(self.deadsofar(yr)- self.deadsofar(yr-1),0))       
    
class FuelType:
    def __init__(self, name,unitEng,UnitEngCost, UnitEmissions):
        self.name = name
        self.unitEng = unitEng
        self.UnitEngCost = UnitEngCost
        self.UnitEmissions= UnitEmissions
                        
NG = FuelType("NG", UnitNG , NGCostYrly, NGEmisYrly)
Elec = FuelType("Elec", UnitElec, ElecCostYrly, ElecEmisYrly)
Prop = FuelType("Prop", UnitProp, PropCostYrly, PropEmisYrly)

#for yr in range(ThisYear, EndYear+1):
#    print yr, "NGCOST", NGCostYrly['MED'][yr], ElecCostYrly['LOW'][yr], PropCostYrly['LOW'][yr]
#this class is to track the annual 'living' stock of WHs of a particular type, their annual energy and emissions for each
#WH in any year (sum over all vintages)

class WH_Aggregates:
    def __init__(self, name):
        self.name=name
        self.AnnAggStock = {}
        self.AnnAggEnergy = {}
        self.AnnAggEmissions = {}


Ref1 = Refrigerant(2000, 1, 0.005, 0.1, 0.3)  
Ref2 = Refrigerant(675, 1, 0.005, 0.1, 0.3)
Ref3 = Refrigerant(1, 1, 0.005, 0.1, 0.3)    

Stck = 100
Time = 2016    
NGGG = WaterHeater('NG_WH1', NG, NG0_EF, Time, Stck, NG_LT, NGIC, OM_NG, False)
INGGG = WaterHeater('ING_WH', NG, ING_EF, Time, Stck, ING_LT, INGIC, OM_ING, False)
EWH = WaterHeater('E_WH', Elec, E_EF, Time, Stck, EL_LT, EWHIC, OM_EL, False)
PWH = WaterHeater('Prop_WH', Prop, Prop_EF, Time, Stck, Prop_LT, PropIC, OM_Prop, False)
HPPP = WaterHeater('HP_WH1', Elec, HP1_EF, Time, Stck, HP_LT, HPIC, OM_HP, True, Ref1)
HPP2 = WaterHeater('HP_WH1', Elec, HP2_EF, Time, Stck, HP_LT, HPIC2, OM_HP, True, Ref2)
HPP3 = WaterHeater('HP_WH1', Elec, HP3_EF, Time, Stck, HP_LT, HPIC3, OM_HP, True, Ref3)
#STHER =  WaterHeater('ST_El', Elec, E_EF/(1-.6), Time ,Stck, ST_LT, SThCapex, OM_ST, False)
STH =  WaterHeater('ST_EL', Elec, E_EF/(1-.6), Time ,Stck, ST_LT, SThERIC, OM_ST, False)
STHHP =  WaterHeater('ST_HP1', Elec, HP1_EF/(1-.6), Time ,Stck, ST_LT, SThHPIC, OM_ST, True, Ref1)
#print ".............."
#print "EMissions solar, HP",  STHHP.AvgRefLeaks(Time),  HPPP.AvgRefLeaks(Time)
#print "EMissions solar, HP",  STHHP.AvgRefLeaks(2031),  HPPP.AvgRefLeaks(2031)
#print "EMissions solar, HP",  STHHP.AvgRefLeaks(2046),  HPPP.AvgRefLeaks(2046)
#print "Emis", NGGG.AnnualEmissions(Time), INGGG.AnnualEmissions(Time), HPPP.AnnualEmissions(yr), STH.AnnualEmissions(yr)


#print "Eng Usage NG, EWH, Prop", NGGG.AnnualEngUsage(),EWH.AnnualEngUsage(),PWH.AnnualEngUsage()
#print "Annual Emissions NG, EWH, Prop", NGGG.AnnualEmissions(Time),EWH.AnnualEmissions(Time), PWH.AnnualEmissions(Time)
#print "Ann Emissions NG, EWH, Prop", NGGG.AnnEmissions(Time),EWH.AnnEmissions(Time), PWH.AnnEmissions(Time)
#print "\n"

yr = Time
CarbonCost = 100

#print  "TT", HPP3.AnnEmissions(yr), HPP3.AvgRefLeaks(yr), EWH.AnnEmissions(yr)
#print  NGGG.AnnualEmissions(yr),HPPP.AnnualEmissions(yr), HPP2.AnnualEmissions(yr), HPP3.AnnualEmissions(yr)
#print "HELLO", EWH.annualizedEmissions(Time),HPPP.annualizedEmissions(Time),HPP2.annualizedEmissions(Time),STH.annualizedEmissions(Time),STHHP.annualizedEmissions(Time)
#print "HEllo Agian", EWH.AnnEmissions(2016),EWH.AvgRefLeaks(2016), HPPP.AnnEmissions(2022), HPPP.AvgRefLeaks(2022),STHHP.AnnEmissions(2016),STHHP.AvgRefLeaks(2016)
#print "++", EWH.AnnEmissions(2016)+ EWH.AvgRefLeaks(2016), HPPP.AnnEmissions(2016)+ HPPP.AvgRefLeaks(2016),HPP2.AnnEmissions(2016)+HPP2.AvgRefLeaks(2016), STHHP.AnnEmissions(2016)+STHHP.AvgRefLeaks(2016)

#print "AnnualizedEmissions", Time,HPPP.annualizedEmissions(Time), EWH.annualizedEmissions(Time), EWH.AnnEmissions(Time), 
#print "AnnualEng", Time, NGGG.AnnualEngUsage(),HPPP.AnnualEngUsage(), EWH.AnnualEngUsage()
#print "AnnualCarbonCost", Time, EWH.annualCarbonCost(Time,50), HPPP.annualCarbonCost(Time,50)
#print "Solar", STHHP.deadsofar(2025), STHHP.numAlive(2025)

#print "LCC", Time, NGGG.lcc(Time,0),INGGG.lcc(Time, 0), EWH.lcc(Time,0),HPPP.lcc(Time,0),  STHHP.lcc(Time,0)
#print "I payback w.r.t NG", yr, NGGG.payback(INGGG,yr), NGGG.payback(EWH,yr), NGGG.payback(HPPP,yr),  NGGG.payback(STH,yr)
#print "II payback w.r.t NG", yr, NGGG.payback1(INGGG,yr), NGGG.payback1(EWH,yr), NGGG.payback1(HPPP,yr),  NGGG.payback1(STH,yr)
#print "II payback w.r.t EWH", yr, EWH.payback(NGGG,yr), EWH.payback(INGGG,yr), EWH.payback(HPPP,yr),  EWH.payback(STHHP,yr)
#print "III payback w.r.t EWH", yr, HPPP.payback(STHHP,yr), HPPP.payback(EWH,yr)

#print "annualized LCC", Time, NGGG.lcc(Time,0)/NGGG.lt, INGGG.lcc(Time, 0)/ INGGG.lt , EWH.lcc(Time,0)/EWH.lt, HPPP.lcc(Time,0)/HPPP.lt, STH.lcc(Time,0)/STH.lt

#print 'payback', Time, NGGG.payback1(INGGG,Time),INGGG.payback1(NGGG,Time), EWH.payback1(NGGG,Time), NGGG.payback1(EWH, Time), INGGG.payback1(HPPP,Time), EWH.payback1(HPPP,Time), INGGG.payback1(STH,Time),STH.payback1(INGGG,Time) 
#print 'payback orig', Time, NGGG.payback(INGGG,Time),INGGG.payback(NGGG,Time), EWH.payback(NGGG,Time), NGGG.payback(EWH,Time), INGGG.payback(HPPP,Time), EWH.payback(HPPP,Time), INGGG.payback(STH,Time), STH.payback(INGGG,Time)

#import matplotlib.pyplot as plt
#from matplotlib.pyplot import *
#import matplotlib.patches as mpatches
#fig = plt.figure(figsize=(10.0, 8.0))
#axes1 = fig.add_subplot(1,1, 1)

#p1 =[]
#p2 = []
#for yr in range (2016,2060):
#      print yr, round( NGGG.numAlive(yr),2), round(INGGG.numAlive(yr),2), round(PWH.numAlive(yr),2), round(HPPP.numAlive(yr),2)
#      plt.hold(True)
  
#      s1 = axes1.scatter(yr-2016, INGGG.numAlive(yr), color = 'r') 
 
#      s1 = axes1.scatter(yr-2016, HPPP.numAlive(yr), color = 'g')
#      s1 = axes1.scatter(yr-2016, STH.numAlive(yr), color = 'b')
#      p1.append([s1])
#axes1.legend([mpatches.Patch(color='r'), mpatches.Patch(color='g'), mpatches.Patch(color = 'b')], ['Instantaneous NG','HeatPump/NG Storage', 'SolarThermal'], loc = 1, fontsize = 10 )
#axes1.axis([0,40, 0, 110])
    

#fig.tight_layout()    
#plt.show() 

