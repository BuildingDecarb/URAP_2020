
## Inputs

pv_size = 3.0  #kW

climatezone = '13'


# Utility rate structures of 
####......PGE Rate Structure ....

Fixed_PGE = 0.2  #Fixed rate all hours through the year

##------TOU - time of Use.......................

speak_PGE = 0.25354
soffpeak_PGE = 0.20657
wpeak_PGE = speak_PGE   #0.18022
woffpeak_PGE =soffpeak_PGE  # 0.17133
TOU = {
    'summer_weekday' :    [1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1],
    'summer_weekend' :    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    'nonsummer_weekday' : [3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3],
    'nonsummer_weekend' : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
}
speak_PGE = 0.25354
soffpeak_PGE = 0.20657
wpeak_PGE = 0.18022
woffpeak_PGE = 0.17133

##--------------Tiered_PGE----------------------------------
base_PGE = 15   #kWh
tier1_PGE = 0.22376   #$/kWh
tier2_PGE = 0,28159    #$/kWh
tier3_PGE = 0.49334     # $/KWh
##----------------------------------------------------------------



