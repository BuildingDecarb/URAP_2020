
#Inputs
#----------

from Inputs import *

UnitNGCost =    1.387 #https://www.eia.gov/dnav/ng/ng_pri_sum_dcu_SCA_m.htm               #1.3 #($/Therm)
UnitElecCost =  0.1832        #https://www.eia.gov/electricity/monthly/epm_table_grapher.cfm?t=epmt_5_6_a    
    # 0.135  #($/kWh)
#UnitPropCost =  2.05 # $/gallon

NGInflation =  0.02 # {'LOW' : 0.01, 'MED': 0.03, 'HIGH': 0.05}
ElecInflation = 0.02  #{'LOW' : 0.01, 'MED': 0.03, 'HIGH': 0.05}
# PropInflation = 0.0  #  {'LOW' : 0.01, 'MED': 0.03, 'HIGH': 0.05}

UnitNGEmission = 6.1 #kg/Therm
UnitPropEmission = 5.67 #kg/gal

ElecEmis_ThisYear = 0.25  #kg/kWh   2016 ARB https://www.arb.ca.gov/cc/inventory/pubs/reports/2000_2016/ghg_inventory_trends_00-16.pdf
ElecEmis_MidYear = 0.203  #place holder
ElecEmis_EndYear = 0.0   #  Elec Emissions for years> Phase33  = 2045  is 0

ThisYear = 2016
MidYear = 2030  # ESTIMATED
EndYear = 2045

UnitBTU = 8.34   #BTU to raise temp of 1 gallon of water by 1 deg F 
Therm_BTU = 100000.0  # 1 therm in BTU
Therm_Ccf = 100.0/1.032  #therms per Ccf (100 cubic feet)
BTU_Ccf = 1032.0  # BTU per scf
kWh_BTU = 3412.14  #1 kWh in BTU
Gal_BTU = 91500.0 #BTU/gallon

Therm_Ccf = 100/1.032  #therms per Ccf (100 cubic feet)
Ccf_Therm = 1.0/Therm_Ccf  #cf by therm
    #1 kWh in BTU

UnitNG = UnitBTU/Therm_BTU   #(THerms)   # energy required to raise the temp of 1 gallon of water by 1 degree
UnitElec = UnitBTU/kWh_BTU    #kWh 
Therm_kWh = Therm_BTU/kWh_BTU
#print UnitNG, UnitElec, Therm_BTU, kWh_BTU
#print  Therm_kWh, Therm_BTU

Gal_kWh = Gal_BTU/kWh_BTU
UnitProp = UnitBTU/Gal_BTU

"""
ElecEmisYrly = {}
ElecEmisYrly[ThisYear] = ElecEmis_ThisYear 
for yr in range(ThisYear+1, EndYear + EL_LT + 10):  #
        if yr <= MidYear:
            ElecEmisYrly[yr] = ElecEmis_ThisYear + ((ElecEmis_MidYear- ElecEmis_ThisYear)/(MidYear - ThisYear))*(yr - ThisYear)
        elif (yr>MidYear and yr <=Phase33):
            ElecEmisYrly[yr] = ElecEmis_MidYear + ((ElecEmis_EndYear- ElecEmis_MidYear)/(EndYear - MidYear))*(yr - MidYear)
        else:
            ElecEmisYrly[yr] = ElecEmis_EndYear   #After Phase33 or 2045 ElecEmis = 0
      #  print yr, ElecEmisYrly[yr]
"""

ElecEmisYrly = {ThisYear: ElecEmis_ThisYear}
for yr in range(ThisYear + 1, EndYear):
    if yr <= MidYear:
        ElecEmisYrly[yr] = ElecEmis_ThisYear + ((ElecEmis_MidYear - ElecEmis_ThisYear)/(MidYear - ThisYear))*(yr - ThisYear)
    else:
        ElecEmisYrly[yr] = ElecEmis_MidYear + ((ElecEmis_EndYear - ElecEmis_MidYear)/(EndYear - MidYear))*(yr - MidYear)

        
#Annual Emissions from Natural gas for now is constant
#Need to Look at this -for ex. switch to RE NG? 
NGEmisYrly = {}
NGEmisYrly[ThisYear] = UnitNGEmission
for yr in range(ThisYear+1, EndYear + NG_LT + 30):
        NGEmisYrly[yr] = UnitNGEmission
        #print yr, NGEmisYrly[yr]

PropEmisYrly = {}
PropEmisYrly[ThisYear] = UnitPropEmission
for yr in range(ThisYear+1, EndYear + NG_LT + 30):
        PropEmisYrly[yr] = UnitPropEmission

#ElecCost with Inflation
     
#for inf in ElecInflation:
      
ElecCostYrly = {}
ElecCostYrly[ThisYear] = UnitElecCost
for yr in range(ThisYear+1, EndYear + EL_LT +25):
                 ElecCostYrly[yr] = ElecCostYrly[yr-1]*(1+ElecInflation)
             #    print  yr, ElecInflation, ElecCostYrly[yr]
       
#NG Cost with inflation
NGCostYrly = {}
NGCostYrly[ThisYear] = UnitNGCost
for yr in range(ThisYear+1, EndYear + NG_LT +25):
                NGCostYrly[yr] = NGCostYrly[yr-1]*(1+NGInflation)
           #     print yr, NGInflation, NGCostYrly[yr]       

#PropCostYrly = {}
#PropCostYrly[ThisYear] = UnitPropCost
#for yr in range(ThisYear+1, EndYear + Prop_LT +25):
#                PropCostYrly[yr] = PropCostYrly[yr-1]*(1+PropInflation)

#Efficienciesof WH (current and future)

for yr in range(ThisYear - 30, ThisYear+1):
        NGEmisYrly[yr]= UnitNGEmission
        PropEmisYrly[yr] = UnitPropEmission
        ElecEmisYrly[yr] = ElecEmis_ThisYear
        NGCostYrly[yr]   = UnitNGCost
      #  PropCostYrly[yr] = UnitPropCost
        ElecCostYrly[yr] = UnitElecCost
     #   print yr, NGCostYrly[yr],NGEmisYrly[yr]
        
