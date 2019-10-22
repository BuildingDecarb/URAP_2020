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
        
        #kW
        self.peakDaily = demandData.dailyPeakDemand(C)
        self.peakMonthly = demandData.monthlyPeakDemand(C)
        self.peakYearly = demandData.peakYearlyDemand(C)
        self.averageYearlyDemand = demandData.averageYearlyDemand(C)

    #Get area needed for sufficient solar panels to meet a yearly demand.
    def getArea(self):
        demand = self.getDailyPeakDemand()
        solar_output_per_cell = self.getKWH()
        area_needed = (demand / solar_output_per_cell) * 10
        return area_needed
    
    #Unit: kW
    def getDailyPeakDemand(self):
        return self.peakDaily
    #Unit: kW
    def getYearlyPeakDemand(self):
        return self.peakYearly
    #Unit: kW
    def getMonthlyPeakDemand(self):
        return self.peakMonthly
    
    #Unit: kWh/sm/day
    def getKWH(self):
        efficiency = .1408
        sizing_factor = 1000 * efficiency
        percentSolarRadiation = 0.2
        return sizing_factor * percentSolarRadiation * 24 / 1000

        

    
        
    
