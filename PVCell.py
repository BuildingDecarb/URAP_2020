import pandas as pd
import numpy as np
from numpy import *
import PVCellDemandData as demandData

class PVCell:
    def __init__(self, C, s1, s2, vintage, lt, IC, OM, ef =0.1, customDemand =False):
        self.name = "PVCell"
        self.ef = ef
        self.C = C
        self.s1 = s1 #Size of walls
        self.s2 = s2 #Size of roof
        self.vintage = vintage
        self.lt = lt
        self.IC = IC 
        self.OM = OM 
        self.customDemand = customDemand

        self.peakDaily = demandData.dailyPeakDemand(C)
        self.peakMonthly = demandData.monthlyPeakDemand(C)
        self.peakYearly = demandData.peakYearlyDemand(C)
        self.averageYearlyDemand = demandData.yearlyDemand(C)

    #Get area needed for sufficient solar panels to meet demand.
    def getArea(self):
        demand = self.getDemand()

    #Get demand based on climate.
    def getDemand(self):
        demandData.climateDict.get(self.C)
        

        
        

    def getPeakDemand(self):



        


    def getKWH(self):
        
    
