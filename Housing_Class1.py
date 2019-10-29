# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 05:36:53 2017
@author: shubaraghavan
"""
from Appliances_Class import *
import copy
# from AnnualHeatDemand import AnnualEngDemand

# import xlrd
# import xlsxwriter
import numpy as np
# import seaborn as sns
# from matplotlib.pyplot import cm

# import matplotlib.pyplot as plt
from matplotlib.pyplot import *
# import matplotlib.patches as mpatch
import csv
import pandas as pd
import datetime


def binomial_draw(p, n=1, N=1):
    s = sum(np.random.binomial(n, p, N) == 1) / N
    return s
    # print binomial_draw(0.9)


def remove_device(devlist, thisdevice, devicename):
    for dd in devlist:
        if dd != thisdevice and devicename in dd.name:
            devlist.remove(dd)


"""List of 16 dictionaries, each corresponding to a dictionary. Each dictionary maps
a tuple of year and end-use to a list of total energy usage for all hours"""

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
months = {"Jan": 0,
          "Feb": 1,
          "Mar": 2,
          "Apr": 3,
          "May": 4,
          "Jun": 5,
          "Jul": 6,
          "Aug": 7,
          "Sep": 8,
          "Oct": 9,
          "Nov": 10,
          "Dec": 11}
seasons = {"Winter": ("Jan", "Feb"),
           "Spring": ("Mar", "May"),
           "Summer": ("Jun", "Aug"),
           "Fall": ("Sep", "Nov")}

class HouseType:

    hourly_energy = [{} for x in range(16)]

    def __init__(self, type, HouseNum, cznum, size1, size2, vintage, devices, is_new=False):
        self.type = type  # SingleFam, Multi_Fam, apt, mobile
        self.HouseNum = HouseNum
        self.cznum = cznum
        self.size1 = size1  # surface area of the walls
        self.size2 = size2  # surface area of the roof
        self.vintage = vintage
        self.devices = devices  # device class
        self.end_uses = [device.name for device in self.devices]
        self.year_dict = {}
        self.is_new = is_new  # boolean

        #if self.devices[0].vintage <= 2007:
        #    pp = binomial_draw(0.1)

        #  if pp ==0:
        #          self.versionId = 1
        #         self.vintage = 2005
        # elif pp == 1:
        #         self.versionId =2
        #         self.vintage = 1990
        # elif self.vintage > 2007:
        #   self.versionId = 3
    # self.deviceCnt = deviceCnt

    # def HHCountWithdevice(self, devicetype):

    class Day:
        def __init__(self, datetime, season, use):
            self.season = season
            # self.weekday = "weekday"
            self.datetime = datetime
            self.use = use
            self.dayuse = sum(self.use)

        """
        def set_season(self, season):
            self.season = season

        def set_day(self, weekday):
            self.weekday = weekday
        """

    def create_year_dict(self, year):
        for end_use in self.end_uses:
            self.year_dict[end_use] = self.create_year(self.cznum, year, end_use)

    def create_year(self, cznum, year, end_use):
        daylist = []
        use = []
        curr_datetime = datetime.datetime(year, 1, 1)
        usage = HouseType.hourly_energy[cznum - 1][year, end_use]
        for i in range(len(usage)):
            use.append(usage[i])
            if (i + 1) % 24 == 0:
                if 6 <= curr_datetime.month <= 9:
                    season = "summer"
                else:
                    season = "winter"
                daylist.append(HouseType.Day(curr_datetime, season, use))
                use = []
                curr_datetime = curr_datetime + datetime.timedelta(days=1)
        return daylist

    def flat(self, price=0.19):
        flat_use = {}
        for end_use, daylist in self.year_dict.items():
            parttotaluse = 0
            for day in daylist:
                parttotaluse = parttotaluse + day.dayuse
            flat_use[end_use] = parttotaluse * price
        flat_use["Total"] = sum(list(flat_use.values()))
        return flat_use


    def tier(self, daylist, baseline=15, tier1=0.22376, tier2=0.28159, tier3=0.49334):
        # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-1.pdf
        monthlyuse = []
        i = 1
        totaluse = 0
        for day in daylist:
            totaluse = totaluse + day.dayuse
            if i in year:
                monthlyuse.append(totaluse)
                totaluse = 0
        totalcost = 0
        for month in monthlyuse:
            totalcost = totalcost + min(baseline, month) * tier1 + max(0, month - baseline) * tier2 + max(0, month - 4*baseline) * tier3
        return totalcost


    def tou(self, daylist, speak=0.25354, soffpeak=0.20657, wpeak=0.18022, woffpeak=0.17133):
        # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_EL-TOU.pdf
        speaksum = 0
        soffpeaksum = 0
        wpeaksum = 0
        woffpeaksum = 0
        for day in daylist:
            if day.season == "summer":
                if day.weekday == "weekday":
                    speaksum = speaksum + sum(day.use[14:19])
                    soffpeaksum = soffpeaksum + sum(day.use[:14]) + sum(day.use[19:])
                else:
                    soffpeaksum = soffpeaksum + day.dayuse
            else:
                if day.weekday == "weekday":
                    wpeaksum = wpeaksum + sum(day.use[14:19])
                    woffpeaksum = woffpeaksum + sum(day.use[:14]) + sum(day.use[19:])
                else:
                    woffpeaksum = woffpeaksum + day.dayuse
        return speaksum * speak + soffpeaksum * soffpeak + wpeaksum * wpeak + woffpeaksum * woffpeak

    def update_dictionary(filename, year, end_use):
        with open(filename, 'r') as csvfile:
            read_csv = csv.reader(csvfile)
            for cznum in range(16):
                csvfile.seek(0)
                first = True
                HouseType.hourly_energy[cznum][(year, end_use)] = []
                for row in read_csv:
                    if first:
                        first = False
                        continue
                    HouseType.hourly_energy[cznum][(year, end_use)].append(float(row[cznum + 1]))

    def get_hourly_usage_for_year(self, cznum, year, end_use):
        """
        Helper function to access the appropriate hourly usage for a particular cznum, year, and end use.
        Returns a list of size 8760 with all the hourly energy usage.
        """
        return HouseType.hourly_energy[cznum - 1][(year, end_use)]

    def get_annual_cost_base_price(self, cznum, year, end_uses, rate):
        annual_usage = self.get_total_annual_usage(cznum, year, end_uses)
        return annual_usage * rate

    def get_total_annual_usage(self, cznum, year, end_uses):
        usages = self.get_annual_usage(cznum, year, end_uses)
        total = 0
        for usage in usages.values():
            total += usage
        return total

    def get_annual_usage(self, cznum, year, end_uses):
        result = {}
        for end_use in end_uses:
            result[end_use] = sum(self.get_hourly_usage_for_year(cznum, year, end_use))
        return result

    def get_hourly_usage_for_seasons(self, season, cznum, year, end_uses):
        """
        Calculates the energy used for a particular season.
        """
        st_month = seasons[season][0]
        end_month = seasons[season][1]
        return self.get_hourly_usage_for_months(st_month, end_month, cznum, year, end_uses)

    def get_hourly_usage_for_months(self, st_month, end_month, cznum, year, end_uses, st_hour=0, end_hour=23):
        """
        Calculates the energy used for a particular month range.
        st_month and end_month are strings containing the first 3 letters of the month.
        st_hour and end_hour can be specified, but function defaults to calculating usage for the entire day.
        """
        st_month_num = months[st_month]
        end_month_num = months[end_month]
        st_day = 0
        for i in range(st_month_num):
            st_day += days_in_months[i]
        end_day = 0
        for i in range(end_month_num + 1):
            end_day += days_in_months[i]
        end_day -= 1
        # print(str(st_day) + " " + str(end_day))
        return self.hour_range(st_hour, end_hour, st_day, end_day, cznum, year, end_uses)

    def get_peak_energy_usage_per_month(self, cznum, year, end_uses):
        """
        Gets the maximum energy usage and corresponding hour for each month
        """
        result = {}
        for end_use in end_uses:
            current = self.get_hourly_usage_for_year(cznum, year, end_use)
            month_usages = {}
            curr_hour = 0
            for i in range(12):
                max_hour = curr_hour
                max_energy = 0
                for j in range(curr_hour, curr_hour + 24 * days_in_months[i]):
                    if current[j] > max_energy:
                        max_hour = j + 1
                        max_energy = current[j]
                curr_hour = curr_hour + 24 * days_in_months[i]
                month_usages[i + 1] = [max_hour, max_energy]
            result[end_use] = month_usages
        return result

    def hour_range(self, st_hour, end_hour, st_day, end_day, cznum, year, end_uses):
        """
        Calculates the energy used for a particular time range across a day range.
        Ex: st_hour = 10, end_hour = 18, st_day = 0, end_day = 30
        Returns the total hourly energy used from 10 a.m. to 6 p.m. each day
        from January 1st to January 31st.
        """
        result = {}
        for end_use in end_uses:
            total = 0
            hourly_usage_for_year = self.get_hourly_usage_for_year(cznum, year, end_use)
            for i in range(st_day, end_day + 1):
                for j in range(st_hour, end_hour + 1):
                    day_in_hours = i * 24
                    total += hourly_usage_for_year[day_in_hours + j]
            # print(end_day * 24 + end_hour)
            result[end_use] = total
        return result

    """Function which returns hourly energy usage """
    def hourly_usage(self, year, end_use, hour):
        temp = (year, end_use)  # Tuple of variables
        return HouseType.hourly_energy[self.cznum][temp][hour - 1]


    def HHenergyUsage_BTU(self):  # outputs heating and cooling energy in BTUs
        # num = self.deviceCnt
        esumheat = 0
        esumcool = 0
        i = 0
        num = len(self.devices)
        NGswitch = 0
        # print "TEST", num
        for k in range(0, num):
            if self.devices[k].name != "Cooler" and self.devices[k].name != "Cond":
                i += 1
                esumheat += self.devices[k].AnnualHeatEngUsage_BTU()  # this does not contain Blower usage
                #  print "before", i, esumheat
                if self.devices[k].fuel.name == "NG" and NGswitch == 0:
                    NGswitch = 1
                    if "WH" not in self.devices[k].name:
                        esumheat += NG_AnnualElecUsage * kWh_BTU  # Adding blower usage
            # print "I", i, self.devices[k].name, NG_AnnualElecUsage,esumheat, "\n"
            if self.devices[k].name == "Cooler":
                i += 1
                esumcool += self.devices[k].AnnualCoolEngUsage_BTU()
            # print "II", i, self.devices[k].name, esumcool , "\n"
            if self.devices[k].name == "Cond":
                i += 1
                esumcool += self.devices[k].AnnualCoolEngUsage_BTU()
                esumheat += self.devices[k].AnnualHeatEngUsage_BTU()
        #       print "III",i, self.devices[k].name, esumcool, esumheat , "\n"
        return esumheat, esumcool  # esumheat contains NG blower electric usage


    def HHenergyUsage_BTU_withoutNGBlower(self):  # outputs heating and cooling energy in BTUs
        # num = self.deviceCnt
        esumheat = 0
        esumcool = 0
        i = 0
        num = len(self.devices)
        #  NGswitch = 0
        # print "TEST", num
        for k in range(0, num):
            if self.devices[k].name != "Cooler" and self.devices[k].name != "Cond":
                i += 1
                esumheat += self.devices[k].AnnualHeatEngUsage_BTU()  # this does not contain Blower usage
            #  print "before", i, esumheat
            # if self.devices[k].fuel.name == "NG" and NGswitch == 0:
            #     NGswitch = 1
            #     if "WH" not in self.devices[k].name:
            #         esumheat += NG_AnnualElecUsage * kWh_BTU     #Adding blower usage
            # print "I", i, self.devices[k].name, NG_AnnualElecUsage,esumheat, "\n"
            if self.devices[k].name == "Cooler":
                i += 1
                esumcool += self.devices[k].AnnualCoolEngUsage_BTU()
            # print "II", i, self.devices[k].name, esumcool , "\n"
            if self.devices[k].name == "Cond":
                i += 1
                esumcool += self.devices[k].AnnualCoolEngUsage_BTU()
                esumheat += self.devices[k].AnnualHeatEngUsage_BTU()
        #       print "III",i, self.devices[k].name, esumcool, esumheat , "\n"
        return esumheat, esumcool  # esumheat contains NG blower electric usage


    def HHenergyUsage_kWh(self):  # total energy usage in a house in KWh
        eng = self.HHenergyUsage_BTU()
        X = eng[0] / kWh_BTU + eng[1] / kWh_BTU
        #  if (self.versionID == 1) return X*1.1:
        return X


    def HHenergyUsage_units(self):  # actually this should HHenergyUsage_fueltype,
        # outputs NG usage and Elec usage - the latter includes the electricity demand of NG Fan blower
        num = len(self.devices)  # BUT NOW   output in kWh ..don't change it though...
        esumNG = 0  # NG usage in kWh
        esumElec = 0  # Elec usage in kWh
        NGswitch = 0
        #  print "cnt", num, devices[0].fuel.name, devices[1].fuel.name,devices[2].fuel.name
        for k in range(0, num):
            #  print "\n Name", self.devices[0].name
            if self.devices[k].fuel.name == "NG" and NGswitch == 0:  # to avoid double counting NG appliances
                NGswitch = 1
                NGEng = self.HHenergyUsage_BTU()[0] / kWh_BTU
                NGEng = NGEng - NG_AnnualElecUsage
                esumNG += NGEng  # in kWh
                if "WH" not in self.devices[k].name:  # only for NG space heaters
                    esumElec += NG_AnnualElecUsage
            #  print "\n NG Eng",k, self.devices[k].name ,esumNG
            elif self.devices[k].fuel.name == "Elec":

                if self.devices[k].name != "Cooler" and self.devices[k].name != "Cond":
                    eheat = self.devices[k].AnnualHeatEngUsage_BTU() / kWh_BTU
                    esumElec += eheat
                #   print "\n heating Energy",k,  self.devices[k].name, eheat
                if self.devices[k].name == "Cooler":
                    ecool = self.devices[k].AnnualCoolEngUsage_BTU() / kWh_BTU
                    esumElec += ecool
                #    print "\n Cooling Energy", k, self.devices[k].name,ecool
                if self.devices[k].name == "Cond":
                    ecool = self.devices[k].AnnualCoolEngUsage_BTU() / kWh_BTU
                    eheat = self.devices[k].AnnualHeatEngUsage_BTU() / kWh_BTU
                    esumElec += ecool + eheat
            #      print "\n Cond Energy", k,devices[k].name, ecool, eheat
        return esumNG, esumElec


    def HHemissions(self, year):
        num = len(self.devices)
        # print "num of devices", num
        emisng = 0
        emiselec = 0
        refemis = 0
        for k in range(0, num):
            if self.devices[k].fuel.name == "Elec":
                if self.devices[k].hasRefrigerant == True:
                    refemis += self.devices[k].AvgRefLeaks(year)
                # print "\Iterate through device", self.type, self.devices[k].name, refemis
        #   print "\n ref yes/no", self.type,self.devices[k].fuel.name, self.devices[k].hasRefrigerant
        NGeng = self.HHenergyUsage_units()[0]  # this is in kWh
        Eleceng = self.HHenergyUsage_units()[1]
        #  print "\n heat & cool eng", self.type,year, NGeng, Eleceng
        emisng = (NGeng / Therm_kWh) * NGEmisYrly[year] / 1000
        emiselec = Eleceng * ElecEmisYrly[year] / 1000
        #     print "\n HH EMissions", year, self.type, NGeng,Eleceng, emisng, emiselec, refemis
        return emisng, emiselec + refemis  # in metric tons


    def HHemissions_refrig(self, year):
        num = len(self.devices)
        # print "num of devices", num
        emisng = 0
        emiselec = 0
        refemis = 0
        for k in range(0, num):
            hdd = self.devices[k].HDD
            cdd = self.devices[k].CDD
            if self.devices[k].fuel.name == "Elec":
                if self.devices[k].hasRefrigerant == True:
                    if self.devices[k].name == "Cooler":
                        refemis += self.devices[k].AvgRefLeaks(year)  # * cdd/(hdd+cdd)
                    if self.devices[k].name == "Cond":
                        refemis += self.devices[k].AvgRefLeaks(year)
                # print "\Iterate through device", self.type, self.devices[k].name, refemis
        #   print "\n ref yes/no", self.type,self.devices[k].fuel.name, self.devices[k].hasRefrigerant
        NGeng = self.HHenergyUsage_units()[0]  # this is in kWh
        Eleceng = self.HHenergyUsage_units()[1]
        #  print "\n heat & cool eng", self.type,year, NGeng, Eleceng
        emisng = (NGeng / Therm_kWh) * NGEmisYrly[year] / 1000
        emiselec = Eleceng * ElecEmisYrly[year] / 1000
        # print "\n HH EMissions", year, self.type, NGeng,Eleceng, emisng, emiselec, refemis, "..", ElecEmisYrly[year], NGEmisYrly[year]
        return emisng, emiselec, refemis


    def HHemissions_heatcool(self, year):
        num = len(self.devices)
        emisheat = 0
        emiscool = 0

        for k in range(0, num):
            hdd = self.devices[k].HDD
            cdd = self.devices[k].CDD
            if self.devices[k].name != "Cooler" and self.devices[k].name != "Cond":
                heateng = self.devices[k].AnnualHeatEngUsage_BTU()  # NO NG BLOWER Usage
                if self.devices[k].fuel.name == "Elec":
                    emisheat += (heateng / kWh_BTU) * ElecEmisYrly[year] / 1000
                    if self.devices[k].hasRefrigerant == True:
                        emisheat += self.devices[k].AvgRefLeaks(year)
                # print "before",self.type, i, emisheat
                if self.devices[k].fuel.name == "NG":
                    emisheat += (heateng / Therm_BTU) * NGEmisYrly[year] / 1000
                    if "WH" not in self.devices[k].name:
                        emisheat += (NG_AnnualElecUsage) * ElecEmisYrly[year] / 1000  # ADDING BLOWER USAGE
            #     print "I",self.type, i, emisheat, "\n"
            if self.devices[k].name == "Cooler":
                cooleng = self.devices[k].AnnualCoolEngUsage_BTU() / kWh_BTU
                emiscool += cooleng * ElecEmisYrly[year] / 1000
                if self.devices[k].hasRefrigerant == True:
                    emiscool += self.devices[k].AvgRefLeaks(year) * cdd / (hdd + cdd)
            #     print "II",self.type, i, emiscool , self.devices[k].AvgRefLeaks(year) ,"\n"
            if self.devices[k].name == "Cond":
                heateng = self.devices[k].AnnualHeatEngUsage_BTU() / kWh_BTU
                cooleng = self.devices[k].AnnualCoolEngUsage_BTU() / kWh_BTU
                hdd = self.devices[k].HDD
                cdd = self.devices[k].CDD
                emisheat += heateng * ElecEmisYrly[year] / 1000 + self.devices[k].AvgRefLeaks(year) * (hdd / (hdd + cdd))
                emiscool += cooleng * ElecEmisYrly[year] / 1000 + self.devices[k].AvgRefLeaks(year) * (cdd / (hdd + cdd))
                print
                "III", self.type, i, self.devices[k].HDD, self.devices[k].CDD, emisheat, emiscool, self.devices[
                    k].AvgRefLeaks(year)
        return emisheat, emiscool


    def HHEnergyCost(self, year):
        eng_units = self.HHenergyUsage_units()
        ngdemand = eng_units[0] / Therm_kWh
        elecdemand = eng_units[1]
        #  print "HH Energy units", self.type, year, ngdemand, elecdemand
        ngCost = ngdemand * NGCostYrly[year]
        elecCost = elecdemand * ElecCostYrly[year]
        # print "Unit Cost", self.type, year, ngdemand, elecdemand,NGCostYrly[year], ElecCostYrly[year],ngCost, elecCost
        return ngCost, elecCost


    def HHTotalEnergyCost(self, year):
        #      print "Total Eng Cost", year, self.type, self.HHEnergyCost(year)[0],  self.HHEnergyCost(year)[1]
        return self.HHEnergyCost(year)[0] + self.HHEnergyCost(year)[1]


    def HHTotalEmissions(self, year):
        #    print "Total Emis", year,self.type, self.HHemissions(year)[0] + self.HHemissions(year)[1]
        return (self.HHemissions(year)[0] + self.HHemissions(year)[1])


    def HHDevicesCapCost(self, year):
        dev = self.devices
        num = len(dev)
        cost = 0
        for k in range(0, num):
            cost += self.devices[k].IC
        #  print "dev cost",num, self.devices[k].name, self.devices[k].IC
        return cost


    def HHNPVDevicesCost(self, year):  # NPV of Capital Cost and OM Cost through the life of Devices
        dev = self.devices
        num = len(dev)
        hhnpv = 0
        for k in range(0, num):
            #  print "\n test devices Cost", year, self.type, self.devices[k].name, self.devices[k].lt
            cost = self.devices[k].NPVCost(year)
            # print "NPV Cost", cost
            hhnpv += cost
        # print year, self.type, hhnpv
        return hhnpv


    def HHNPVEnergyCost(self, year):
        dev = self.devices
        num = len(dev)
        minLT = 0
        engcost = 0
        minLT = 0
        for k in range(0, num):
            minLT = min(self.devices[0].lt, self.devices[k].lt)
        # print "MIN LT", self.type, self.devices[k].name,minLT, self.devices[k].lt
        for k in range(year, year + minLT + 1):
            cost = self.HHTotalEnergyCost(k)
            engcost += cost / (1 + DiscRate) ** (k - year + 1)
        #   print year, self.type, cost
        return engcost


    def HHNPVEmissionsCost(self, year, UnitCarbonCost=0):  # at CCost = $1, this is just a NPV of emissions
        CCost = UnitCarbonCost
        dev = self.devices
        num = len(dev)
        minLT = self.devices[0].lt
        hhemisCost = 0
        for k in range(0, num):
            minLT = min(self.devices[k].lt, self.devices[k].lt)
        # print "min LT", self.type, self.devices[k].name, minLT
        for time in range(1, minLT + 1):
            years = year + time
            hhemis = self.HHTotalEmissions(years)
            hhemisCost += CCost * hhemis / (1 + DiscRate) ** (time + 1)
        #     print "HH Emissions", year, self.type, hhemis, hhemisCost
        return hhemisCost


    def HHNPVDevicesCost(self, year):  # NPV of Capital Cost and OM Cost through the life of Devices
        dev = self.devices
        num = len(dev)
        hhnpv = 0
        for k in range(0, num):
            # print "\n test devices Cost", year, self.type, self.devices[k].name, self.devices[k].lt
            cost = self.devices[k].NPVCost(year)
            #   print "NPV Cost", cost
            hhnpv += cost
        # print year, self.type, hhnpv
        return hhnpv


    # =================================================================================================================
    def HHNPVEnergyCost_LT(self, year, horizon):
        dev = self.devices
        num = len(dev)
        minLT = 0
        engcost = 0
        minLT = horizon

        # print "MIN LT", self.type, self.devices[k].name,minLT, self.devices[k].lt
        for k in range(year, year + minLT):
            cost = self.HHTotalEnergyCost(k)
            engcost += cost / (1 + DiscRate) ** (k - year)
        # print year, self.type, cost
        #  print year, self.devices[0].name, engcost
        return engcost


    def HHNPVEmissionsCost_LT(self, year, horizon, UnitCarbonCost=0):  # at CCost = $1, this is just a NPV of emissions
        CCost = UnitCarbonCost
        dev = self.devices
        num = len(dev)
        minLT = horizon
        hhemisCost = 0

        # print "min LT", self.type, self.devices[k].name, minLT
        for time in range(1, minLT + 1):
            years = year + time
            hhemis = self.HHTotalEmissions(years)
            hhemisCost += CCost * hhemis / (1 + DiscRate) ** (time)
        #     print "HH Emissions", year, self.type, hhemis, hhemisCost
        return hhemisCost


    # ============================================================================

    def HHpayback(self, Hx, yr, CC):  # SF3 = Hx and SF1= self two appliances vs Conditioner...specifically
        N = 1
        maxN = 22  #
        dev1 = self.devices
        dev2 = Hx.devices
        num1 = len(dev1)  # self
        num2 = len(dev2)  # SF3
        Capcost1 = self.HHDevicesCapCost(yr)
        Capcost2 = Hx.HHDevicesCapCost(yr)
        delta_cost = Capcost2 - Capcost1
        eng1 = self.HHTotalEnergyCost(yr)  # Assuming O&M are the same for both...not true..but
        eng2 = Hx.HHTotalEnergyCost(yr)
        emis1 = self.HHTotalEmissions(yr)
        emis2 = Hx.HHTotalEmissions(yr)
        deng = eng2 - eng1
        demis = CC * (emis2 - emis1)
        delta = (deng + demis) / (1 + DiscRate) ** N
        cnt = 0
        #    print "cnt 0...",cnt, N, yr, CC,  delta_cost, deng, demis,delta
        if round(delta_cost + delta, 0) <= 0:
            return 0
        elif round(delta_cost + delta, 0) > 0:  # App2 is more expensive but app2 energy cheaper
            while N <= maxN and round(delta_cost + delta, 0) > 0:
                cnt += 1
                N = N + 1
                deng = Hx.HHTotalEnergyCost(yr + N) - self.HHTotalEnergyCost(yr + N)
                demis = CC * (Hx.HHTotalEmissions(yr + N) - self.HHTotalEmissions(yr + N))
                diff = (deng + demis)
                delta += diff / (1 + DiscRate) ** (N)
            return N


    def HHCCBreakEven(self, Hx, yr, TimeHorizon=15):  # breakeven carbon cost of Hx with self.
        #  print "\n Calling X1"
        CC = 0
        delta_cost = Hx.HHDevicesCapCost(yr) - self.HHDevicesCapCost(yr)
        engcost1 = 0
        engcost2 = 0
        emis1 = 0
        emis2 = 0
        for k in range(yr, yr + TimeHorizon + 1):
            cost1 = self.HHTotalEnergyCost(k)
            engcost1 += cost1 / (1 + DiscRate) ** (k - yr)
            hhemis1 = self.HHTotalEmissions(k)
            emis1 += hhemis1 / (1 + DiscRate) ** (k - yr)

            cost2 = Hx.HHTotalEnergyCost(k)
            engcost2 += cost2 / (1 + DiscRate) ** (k - yr)
            hhemis2 = Hx.HHTotalEmissions(k)
            emis2 += hhemis2 / (1 + DiscRate) ** (k - yr)

            delta_eng = engcost2 - engcost1
        diff_emis = emis2 - emis1
        delta_emis = CC * diff_emis

        #  print "breakeven CC..", CC, delta_cost , engcost1, engcost2, emis1, emis2
        if round(delta_cost + delta_eng + delta_emis, 0) <= 0:
            return CC
        elif round(delta_cost + delta_eng + delta_emis, 0) > 0:

            while round(delta_cost + delta_eng + delta_emis, 0) > 0 and CC <= 2000:
                CC += 25
                delta_emis = CC * diff_emis
            #  print "breakeven CC: ", yr,k, self.type, Hx.type, CC, delta_cost, delta_eng, emis2- emis1
        return CC


    def HHLCC(self, year, CarbonCost=0):  # assuming time horizon is MinLifeTime of all appliances
        lcc = self.HHNPVDevicesCost(year) + self.HHNPVEnergyCost(year) + self.HHNPVEmissionsCost(year, CarbonCost)
        return lcc


class SFHomes(HouseType, object):
    def __init__(self, type, HouseNum, cznum, size1, size2, vintage, devices, is_new=False):
        super(SFHomes, self).__init__(type, HouseNum, cznum, size1, size2, vintage, devices, is_new)
    #  def HHenergy(self):
    #  return super(SFHomes, self).HHenergyUsage_BTU()


class MFHomes(HouseType, object):
    def __init__(self, type, HouseNum, cznum, size11, size21, vintage, devices, is_new=False):
        super(MFHomes, self).__init__(type, HouseNum, cznum, size11, size21, vintage, devices, is_new)


#  def HHenergyUsage_BTU(self):
#     return super(MFHomes, self).HHenergyUsage_BTU()

def getDead(p1_homes, devices, homeType, fuelName, k, yr):
    # print "dead test", device.name, device.fuel.name
    for dev in devices:
        print
        "testtest", yr, dev.C, k, len(devices), dev.name, fuelName, dev.annualreplacement(yr)
    num = sum([dev.annualreplacement(yr) for dev in devices if (dev.C == k and dev.fuel.name == fuelName)])
    #  print "dead", num
    return num


def getAppDead(p1_homes, devices, homeType, fuelName, AppName, k, yr):
    if "HP" in AppName:
        return sum([dev.annualreplacement(yr) for dev in devices if
                    (dev.C == k and dev.fuel.name == fuelName and "HP" in dev.name)])
    elif "Cooler" in AppName:
        return sum([dev.annualreplacement(yr) for dev in devices if
                    (dev.C == k and dev.fuel.name == fuelName and "Cooler" in dev.name)])
    elif "Cond" in AppName:
        return sum([dev.annualreplacement(yr) for dev in devices if
                    (dev.C == k and dev.fuel.name == fuelName and "Cond" in dev.name)])


def homesWithApp(homes, deviceName):
    num = 0
    for home in homes:
        dev = home.devices
        for d in dev:
            if d.name == deviceName:
                num += 1
    return num


class HomesStats:

    def __init__(self, year, cznum, homes):
        self.year = year
        self.cznum = cznum
        self.homes = homes  # hometype
        self.aggregateHomeStats = {}  # mapping of hometype to AggregateStats
    #  self.aggregatedevicesByType = {}   # stats on different kinds of devices


class AggregateStats:
    def __init__(self):
        self.num = 0  # total homes of a hometype in a #cz in a year
        self.num1 = 0  # total homes iwth heating
        self.num2 = 0  # total homes with cooling
        self.numdev = 0  # number of total devices in a home
        self.aggDevices = {}  # list of devices for each hometype
        self.eng1 = 0  # NG energy
        self.eng2 = 0  # electricity
        self.heateng = 0
        self.cooleng = 0
        self.emis1 = 0  # NG emis
        self.emis2 = 0  # Elec Emis
        self.emis_refrig = 0
        self.heatemis = 0
        self.coolemis = 0
        self.engCost1 = 0  # NG Cost
        self.engCost2 = 0  # Elec Cost
        self.heatCost = 0
        self.coolCost = 0
        self.replaceCost = 0
        self.hpcond_heat = 0  # heat energy of HP Cond
        self.hpcond_cool = 0
        #   self.devices = devices   #specifics of device list in that home in that year in that cZ
        self.aggDevices = aggDevices


# combine two lists of home classes into one struct
aggDevices = {}


def updateHomeStats(A, B):
    # print A.year, B.year, A.cznum, B.cznum
    z = copy.deepcopy(A)
    z.year = A.year
    z.cznum = A.cznum
    #  homesL1 = [A.homes]
    # z.homes = homesL1.extend([B.homes] )
    z.homes = copy.deepcopy(A.homes) + copy.deepcopy(B.homes)
    #        for homeType in B.aggregateHomeStats:
    #            if homeType in A.aggregateHomeStats:
    #                z.aggregateHomeStats[homeType] = combine(A.aggregateHomeStats[homeType], B.aggregateHomeStats[homeType])
    #            else:
    #                z.aggregateHomeStats[homeType] = B.aggregateHomeStats[homeType]
    return z


# go field by field, creating homeStats with each field as combo self.field and otherHomeStats.field
# combine two aggregate stats
def combine(A, B):
    newaggregate = copy.copy(A)
    newaggregate.num += B.num
    newaggregate.num1 += B.num1  # NUm HHs with heating
    newaggregate.num2 += B.num2  # Num HHs iwth cooling
    newaggregate.eng1 += B.eng1  # NG eng in kWh
    newaggregate.eng2 += B.eng2  # Elec eng in kWH
    newaggregate.heaeng += B.heateng
    newaggregate.cooeng += B.cooleng
    newaggregate.emis1 += B.emis1
    newaggregate.emis2 += B.emis2
    newaggregate.emis_refrig += B.emis_refrig
    newaggregate.heatemis += B.heatemis
    newaggregate.coolemis += B.coolemis
    newaggregate.engCost1 += B.engCost1
    newaggregate.engCost2 += B.engCost2
    newaggregate.heatCost += B.heatCost
    newaggregate.coolCost += B.coolCost
    newaggregate.replaceCost += B.replaceCost
    newaggregate.hpcond_heat += B.hpcond_heat
    newaggregate.hpcond_cool += B.hpcond_cool
    #   newaggregate.aggDevices = A.aggDevices
    # for dev in B.aggDevices:
    #    newaggregate.aggDevices += B.aggDevices
    return newaggregate


# get a list of devices  -
def getDevices(stats, homeType):
    devs = []
    for home in stats.homes:
        if home.type == homeType:
            for d in home.devices:
                #  if d.lt ==  15:
                devs += [copy.copy(d)]
    return devs


def isDeviceinHome(home, devname):
    for d in home.devices:
        if d.name == devname:
            return 1
    return 0

"""
def addDevice(home, newdevname):
    for d in home.devices:
        dev = home.devices
        if d.name != newdev.name:  # if device already in the house..return the existing dev list
            dev += newdev
        return dev
"""


# get a list of devices of deviceType in a particular year from all hometypes
def getDevicesYear(stats, deviceType, year):
    devs = []
    for home in stats.homes:
        # homeType = home.type
        for d in home.devices:
            if d.name == deviceType:
                devs += [copy.copy(d)]
    return devs


#
def getDeviceCountYear(stats, deviceType, year):  # Num of devices of this type in a year in all homes
    cnt = 0
    for home in stats.homes:
        # homeType = home.type
        for d in home.devices:
            if d.name == deviceType:
                cnt += 1
    return cnt


def getDeviceCountinHome(stats, deviceType, homeType, year):  # THIS works
    cnt = 0
    for home in stats.homes:
        if home.type == homeType:
            for d in home.devices:
                if d.name == deviceType:
                    cnt += 1
                #    print "func call:", home.type,   d.name, cnt
    return cnt


def getDeviceEnginHome(stats, deviceType, homeType):
    heng = 0
    ceng = 0
    for home in stats.homes:
        if home.type != homeType:
            #    print "not home", home.type, homeType
            break
        for d in home.devices:
            if d.name != deviceType:
                break
            heateng = d.AnnualHeatEngUsage_BTU() / kWh_BTU  # This does not include NG blower energy
            cooleng = d.AnnualCoolEngUsage_BTU() / kWh_BTU
            heng = home.HHenergyUsage_BTU_withoutNGBlower()[0] / kWh_BTU
            ceng = home.HHenergyUsage_BTU_withoutNGBlower()[1] / kWh_BTU
    #         print "cond elec", homeType, deviceType,heateng,cooleng, ".....", heng, ceng

    #  print "cond heat", homeType, deviceType, heng, ceng
    return heng, ceng


# def getDeviceCumulativeCount(stats, deviceType,  year): #Sum of all devices installed till this year
#     cnt = 0
#  for yr in range(PastPastYear, year+1):
#      cnt += getDeviceCountYear(stats, deviceType, yr)
#  return cnt

def getDeviceCapCost(stats, deviceType, year):  # weighted average cap cost of that year's stock
    dcost = 0
    for home in stats.homes:
        devcnt = getDeviceCountinHome(stats, deviceType, home.type, year)
        for d in home.devices:
            if d.name == deviceType:
                dcost += d.IC
            #    print year, home.type, devcnt, d.name, d.IC
    if devcnt == 0:
        return 0
    else:
        return dcost / devcnt


# def getDeviceIC(stats, deviceType, year):  # cap cost of that vintage

#     for home in stats.homes:

#         for d in home.devices:

#             if d.name == deviceType and:
#                 dcost = d.IC
#                 return dcost
#             else:
#               return 0

def LearningRateCost(stats, deviceType, Cum, year, LR=LR_HP):  # Assuming this is used only for HPConditioners..
    devcost = 0  # LR_HP given in the 1st few line of Inputs_Appliances_Retrofit
    if deviceType == "Cond":
        cum = Cum
        ctr = 1
        devcost = HPCapex1
        while (
                cum > 2 * HPCumulativeFloor * ctr and devcost >= HPCapexFloor):  # HPCumulativeFloor is defined in Inputs_Appliances_Retrofit
            devcost = devcost * (1 - LR)
            ctr += 1
        #  print "LR MODULE", year, ctr, cum, devcost
        #  print "LR Cost Cond", year, cum
        return devcost
    else:
        return 0


def gethomeTypecount(stats, homeType):
    cnt = 0
    for home in stats.homes:
        if home.type == homeType:
            cnt += 1
    return cnt


def getwtAvgLT(stats, deviceType, homeType, year):  # weighted average age is life/cnt
    wtavg = 0
    life = 0
    cnt = getDeviceCountinHome(stats, deviceType, homeType, year)
    if cnt == 0:
        return 0
    else:
        #  print "getwtAvgLT", cnt, homeType, deviceType
        for home in stats.homes:
            d_lt = 0
            if home.type == homeType:
                for d in home.devices:
                    if d.name == deviceType:
                        d_lt += d.lt
                        wtavg += d_lt
                        life += year - d.vintage
                    # print d_lt
                    # print "home type wtavg",year, year-d.vintage, home.type, deviceType, life ,cnt
    return life / cnt  # wtavg /cnt


def getwtAvgEF(stats, deviceType, homeType, year):  # weighted average age is life/cnt
    wtavgEF = 0
    d_ef = 0
    cnt = getDeviceCountinHome(stats, deviceType, homeType, year)
    if cnt == 0:
        return 0
    else:
        #  print "getwtAvgLT", cnt, homeType, deviceType
        for home in stats.homes:
            if home.type == homeType:
                for d in home.devices:
                    if d.name == deviceType:
                        if "Cooler" in d.name or "Cond" in d.name:
                            d_ef += d.ef_cooler
                            wtavgEF = d_ef
                        #   print year, homeType, d.name, d_ef, cnt
                        else:
                            d_ef += d.ef
                            wtavgEF = d_ef
                        # print year, homeType, d.name, d_ef, cnt
                    # print "home type wtavg",year, year-d.vintage, home.type, deviceType, life ,cnt
    return wtavgEF / cnt  # wtavg /cnt

"""
# horizon = 5   #breakeven carbon
# CC =  0
Stck1 = 1
k = 3
year = 2018
is_new = False
# print "\nSF1 \n"
R0val[i, year] = 1.0 / UVals.cell(45, 13).value  # 1.0/HDD_CDD.cell(23+1,11).value   # window
R1val[i, year] = 1.0 / UVals.cell(44, 13).value  # 1.0/HDD_CDD.cell(23+1,6).value
R2val[i, year] = 1.0 / UVals.cell(43, 13).value
devices1 = []
devices1 += [NGHeater(k, size11, size22, year, False, is_new)]  # 2nd True for new home
devices1 += [Cooler(k, size11, size22, year, is_new)]
# devices1 += [NGWH(k,year)]
SF1 = SFHomes("SF1", Stck1, k, size11, size22, year, devices1, is_new)

SHeng = devices1[0].AnnualHeatEngUsage_BTU()
Cooleng = devices1[1].AnnualCoolEngUsage_BTU()

# WHemis = devices1[2].AnnEmissions(year,WHeng)
SHemis = devices1[0].AnnEmissions(year, SHeng)  # NG, Elec and total emis 3 tuple result
Coolemis = devices1[1].AnnEmissions(year, Cooleng)  # ditto
R0val[i, year] = 1.0 / UVals.cell(45, 13).value  # 1.0/HDD_CDD.cell(23+1,11).value   # window
R1val[i, year] = 1.0 / UVals.cell(44, 13).value  # 1.0/HDD_CDD.cell(23+1,6).value
R2val[i, year] = 1.0 / UVals.cell(43, 13).value
heng1 = SF1.HHenergyUsage_BTU()[0] / kWh_BTU
ceng1 = SF1.HHenergyUsage_BTU()[1] / kWh_BTU

heng11 = SF1.HHenergyUsage_units()[0]  # NG Usage in kWh
ceng12 = SF1.HHenergyUsage_units()[1]  # Elec usage in KWh
hhemis1 = SF1.HHemissions_refrig(year)[0]
hhemis2 = SF1.HHemissions_refrig(year)[1]
hhemis_refrig = SF1.HHemissions_refrig(year)[2]
hhheatemis = SF1.HHemissions_heatcool(year)[0]
hhcoolemis = SF1.HHemissions_heatcool(year)[1]
hhcost = SF1.HHDevicesCapCost(year)
# print "\n test", 1/SF1.devices[0].Rval0, 1/SF1.devices[0].Rval1,1/SF1.devices[0].Rval2
print
"SF1", k, year, round(heng1, 2), round(ceng1, 2), round(heng11, 2), round(ceng12,
                                                                          2)  # , "..", round(hhemis1,3), round(hhemis2,3),round(hhemis_refrig,3) ,round(hhheatemis,3), round(hhcoolemis,3)
# print "\n"
# print "SF1 Cost", SF1.HHEnergyCost(year)[0], SF1.HHEnergyCost(year)[1], SF1.HHLCC(year,CC)

# devices2 = []
# devices2 +=[ Cond(k,size1,size2,year, HPCapex1, False, False, is_new)]
# #devices2 +=[HPWH(k,year)]
# SF2 =  SFHomes("SF2",Stck1 , k,size1, size2,year,devices2, is_new)

# #WHeng2 = devices2[1].AnnualHeatEngUsage_BTU()
# SHeng2 = devices2[0].AnnualHeatEngUsage_BTU()
# Cooleng2 = devices2[0].AnnualCoolEngUsage_BTU()
# #WHemis2 = devices2[1].AnnEmissions(year,WHeng2)
# SHemis2 = devices2[0].AnnEmissions(year,SHeng2)
# Coolemis2 = devices2[0].AnnEmissions(year,Cooleng2)
# #print "Eng WH, SH, Cool" , WHeng2/kWh_BTU, SHeng2/kWh_BTU, Cooleng2/kWh_BTU
# #print "Emis WH SH Cool", WHemis2[0]+ SHemis2[0],WHemis2[1],SHemis2[1], Coolemis2[1]

# heng2 = SF2.HHenergyUsage_BTU()[0]/kWh_BTU
# ceng2 = SF2.HHenergyUsage_BTU()[1]/kWh_BTU
# hhemis21 = SF2.HHemissions(year)[0]
# hhemis22 = SF2.HHemissions(year)[1]
# hhheatemis2 = SF2.HHemissions_heatcool(year)[0]
# hhcoolemis2 = SF2.HHemissions_heatcool(year)[1]
# hhcost = SF2.HHDevicesCapCost(year)
# print "SF2 Eng", k, year,round(heng2,3), round(ceng2,3)   #,  round(hhemis22,3),round(hhheatemis2,3), round(hhcoolemis2,3)
# print "\n"  #, 1/SF2.devices[0].Rval0, 1/SF2.devices[0].Rval1,1/SF2.devices[0].Rval2
# print "SF2 Cost", SF2.HHEnergyCost(year)[0], SF2.HHEnergyCost(year)[1], SF2.HHLCC(year,CC)


#

# #print np1
# #print "test",SF1.devices[0].name,len(dev)
# devices2 = []
# devices2 += [HP(k,size1,size2,year)]
# devices2 += [Cooler(k,size1,size2 , year)]
# SF2 =  SFHomes("SF2",Stck1 , k,size1, size2,year,devices2)

# devices3 = []
# devices3 += [Cond(k,size1,size2,year)]
# SF3 =  SFHomes("SF3",Stck1 , k,size1, size2,year,devices3)
# #
# #
# #ecost1 = SF1.HHEnergyCost(year)[0]
# #ecost11 = SF1.HHEnergyCost(year)[1]
# #ecost2 = SF2.HHEnergyCost(year)[0]
# #ecost22 = SF2.HHEnergyCost(year)[1]

# emis1 = SF1.HHemissions(year)[0]
# emis11 = SF1.HHemissions(year)[1]
# print "...."
# emis2 = SF1.HHemissions_heatcool(year)[0]
# emis22 = SF1.HHemissions_heatcool(year)[1]

# print year,k,  "SF1", emis1, emis11, emis2, emis22
# print ">>>>"

# emis3 = SF3.HHemissions(year)[0]
# emis33 = SF3.HHemissions(year)[1]
# emis34 = SF3.HHemissions_heatcool(year)[0]
# emis334 = SF3.HHemissions_heatcool(year)[1]


# print year, k, "SF3", emis3, emis33, emis34, emis334


# #
# #SF1HeatEng = SF1.devices[0].AnnualHeatEngUsage_BTU()
# #SF1CoolEng = SF1.devices[1].AnnualCoolEngUsage_BTU()
# #SF2HeatEng = SF2.devices[0].AnnualHeatEngUsage_BTU()
# SF2CoolEng = SF2.devices[1].AnnualCoolEngUsage_BTU()
# SF3HeatEng = SF3.devices[0].AnnualHeatEngUsage_BTU()
# SF3CoolEng = SF3.devices[0].AnnualCoolEngUsage_BTU()
# cost1 = SF1.devices[0].AnnualEngCost(year, SF1HeatEng)
# cost11 = SF1.devices[1].AnnualEngCost(year, SF1CoolEng)
# cost2 = SF2.devices[0].AnnualEngCost(year, SF2HeatEng)
# cost22 = SF2.devices[1].AnnualEngCost(year, SF2CoolEng)
# cost3 = SF3.devices[0].AnnualEngCost(year, SF3HeatEng)
# cost33 = SF3.devices[0].AnnualEngCost(year, SF3CoolEng)
#
##print "Annual devices energy Usage", SF1HeatEng/(Therm_BTU), SF1CoolEng/(kWh_BTU), SF2HeatEng/(kWh_BTU), SF2CoolEng/(kWh_BTU),SF3HeatEng/(kWh_BTU), SF3CoolEng/(kWh_BTU)
##
##print " \n energy Usage", SF1.HHenergyUsage_units(),SF2.HHenergyUsage_units(),SF3.HHenergyUsage_units()
##print "Annual Devices energy cost", cost1, cost11, cost2, cost22, cost3, cost33
##print "Eng Costs", ecost1, ecost11, ecost2, ecost22, ecost3, ecost33
##
##print "HH ENg Costs", SF1.HHNPVEnergyCost(year), SF2.HHNPVEnergyCost(year), SF3.HHNPVEnergyCost(year)
##print "HH devices COsts", SF1.HHNPVDevicesCost(year), SF2.HHNPVDevicesCost(year), SF3.HHNPVDevicesCost(year)
##print "HH emissions COsts", SF1.HHNPVEmissionsCost(year,55), SF2.HHNPVEmissionsCost(year,55), SF3.HHNPVEmissionsCost(year,55)
##print "HHLCC", SF1.HHLCC(year,CC), SF2.HHLCC(year,CC), SF3.HHLCC(year,CC)
##print "\n\n.........."
##np1 = SF1.HHCCBreakEven( SF2,year)
##np2 = SF1.HHCCBreakEven( SF3,year)
##print "HOUSES", np1, np2
"""