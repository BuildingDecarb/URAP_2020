from Inputs import *

def linearinterp(x1,x2,y1,y2,x):
    return ((y2-y1)/(x2-x1))*(x-x1) + y1  

def ElectrificationRate(yr, beginyr, EndYear,  Rate_beginyr, Rate_EndYear):  
          return  linearinterp(beginyr, EndYear,Rate_beginyr,Rate_EndYear, yr)

    
def ElectricRate(yr, ElecPercNG1,ElecPercNG2,ElecPercNG3,FinalPercNG_Elec ):   
     if (yr >=ThisYear):
            if (yr < Phase1 ):
                ElecRate = min(max(ElectrificationRate(yr, ThisYear,Phase1, 0.05, ElecPercNG1),0),ElecPercNG1)
       #         print yr, ElecRate
            elif (yr >= Phase1 and yr <= Phase2):
                ElecRate = min(max(ElectrificationRate(yr, Phase1,Phase2, ElecPercNG1, ElecPercNG2),0),ElecPercNG2)
     #           print yr, ElecRate
            elif (yr > Phase2 and yr <= Phase3):
                ElecRate = min(max(ElectrificationRate(yr, Phase2,Phase3, ElecPercNG2, ElecPercNG3),0),ElecPercNG3)
     #           print yr, ElecRate    
            elif (yr > Phase3 and yr <=EndYear):
                ElecRate = min(max(ElectrificationRate(yr, Phase3, EndYear,  ElecPercNG3, FinalPercNG_Elec),0),FinalPercNG_Elec)
     #           print yr, ElecRate
            else:
                ElecRate = 0
     else:
            ElecRate = 0
     return ElecRate       
    
def linearinterp(x1,x2,y1,y2,x):
    return ((y2-y1)/(x2-x1))*(x-x1) + y1 
    
def NPVSeq(arr, y1, y2, drate):
    result = 0
    for i in range (y1 , y2 +1):
        result = result + arr[i]/(1+drate)^(i-y1+1)
    return result    

S1_1 = 0.0   #phase1 2020  #NG to HP
S1_2= 0.5 # phase2 2030
S1_3 = 0.75  #phase3 2040
S1_4 = 1.0  #endyear 2050

S2_1 = 0.0   #phase1 2020   # ER TO HP
S2_2= 0.0  # phase2 2030
S2_3 = 0.0   #phase3 2040
S2_4 = 0.0    #endyear 2050

S3_1 = 0.0   #phase1 2020    # AC to HP
S3_2 = 0.75 # phase2 2030
S3_3 = 0.9  #phase3 2040
S3_4 = 1.0  #endyear 2050

# for yr in range( 2020, 2051):
#    print yr, ElectricRate(yr, S3_1,S3_2,S3_3,S3_4 ) 

def NG1_prob(yr):
         p = ElectricRate(yr, S1_1,S1_2,S1_3,S1_4 ) 
         N =1   #coin tossed N times..
         n=1
         s =sum(np.random.binomial(n, p,N)==1)/N  #   flipping a coin - with prob =p heads, device dies
      #   print "prob", yr, p,s
         return s

def ER1_prob(yr):
         p = ElectricRate(yr, S2_1,S2_2,S2_3,S2_4 ) 
         N =1   #coin tossed N times..
         n=1
         s =sum(np.random.binomial(n, p,N)==1)/N  #   flipping a coin - with prob =p heads, device dies
       #  print "prob", yr, p,s
         return s         

def AC1_prob(yr):
         p = ElectricRate(yr, S3_1,S3_2, S3_3, S3_4 ) 
         N =1   #coin tossed N times..
         n=1
         s =sum(np.random.binomial(n, p,N)==1)/N  #   flipping a coin - with prob =p heads, device dies
        # print "prob", yr, p,s
         return s         

# for yr in range(ThisYear,EndYear+1):
#     p = NG1_prob(yr)
#     q = ER1_prob(yr)
#     r = AC1_prob(yr)
#     print yr, p,q  ,r       