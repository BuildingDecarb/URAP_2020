from calendar import monthrange
import pandas as pd

# PV System Specifications for Data Below
# DC System Size: 4 kW //TODO: Update files to change to 1 kW
# Module: Standard
# Array Type: Fixed (open rack)
# Array Tilt: 20°
# Array Azimuth: 180°
# Efficiency: 14.08% 
# Inverter Efficiency: 96%
# DC to AC Size Ratio: 1.2
# Capacity Factor: 15.3%

C1_arcata = pd.read_csv("PVCellData/1_Arcata.csv", skiprows = 17)
C1_eureka = pd.read_csv("PVCellData/1_Eureka.csv", skiprows = 17)

C2_napa = pd.read_csv("PVCellData/2_Napa.csv", skiprows = 17)
C2_sanrafael = pd.read_csv("PVCellData/2_SanRafael.csv", skiprows = 17)

C3_oakland = pd.read_csv("PVCellData/3_Oakland.csv", skiprows = 17)
C3_redwoodcity = pd.read_csv("PVCellData/3_RedwoodCity.csv", skiprows = 17)
C3_sf = pd.read_csv("PVCellData/3_SF.csv", skiprows = 17)

C4_gilroy = pd.read_csv("PVCellData/4_Gilroy.csv", skiprows = 17)
C4_sanjose = pd.read_csv("PVCellData/4_SanJose.csv", skiprows = 17)
C4_sunnyvale = pd.read_csv("PVCellData/4_Sunnyvale.csv", skiprows = 17)

C5_santamaria = pd.read_csv("PVCellData/5_SantaMaria.csv", skiprows = 17)
C5_slo = pd.read_csv("PVCellData/5_SLO.csv", skiprows = 17)

C6_longbeach = pd.read_csv("PVCellData/6_LongBeach.csv", skiprows = 17)
C6_santabarbara = pd.read_csv("PVCellData/6_SantaBarbara.csv", skiprows = 17)

C7_oceanside = pd.read_csv("PVCellData/7_Oceanside.csv", skiprows = 17)
C7_sandiego = pd.read_csv("PVCellData/7_SanDiego.csv", skiprows = 17)

C8_anaheim = pd.read_csv("PVCellData/8_Anaheim.csv", skiprows = 17)
C8_tustin = pd.read_csv("PVCellData/8_Tustin.csv", skiprows = 17)

C9_la = pd.read_csv("PVCellData/9_LA.csv", skiprows = 17)
C9_pasadena = pd.read_csv("PVCellData/9_Pasadena.csv", skiprows = 17)

C10_riverside = pd.read_csv("PVCellData/10_Riverside.csv", skiprows = 17)
C10_sanbernardino = pd.read_csv("PVCellData/10_SanBernardino.csv", skiprows = 17)

C11_marysville = pd.read_csv("PVCellData/11_Marysville.csv", skiprows = 17)
C11_redbluff = pd.read_csv("PVCellData/11_RedBluff.csv", skiprows = 17)

C12_merced = pd.read_csv("PVCellData/12_Merced.csv", skiprows = 17)
C12_stockton = pd.read_csv("PVCellData/12_Stockton.csv", skiprows = 17)

C13_bakersfield = pd.read_csv("PVCellData/13_Bakersfield.csv", skiprows = 17)
C13_fresno = pd.read_csv("PVCellData/13_Fresno.csv", skiprows = 17)

C14_29palms = pd.read_csv("PVCellData/14_29Palms.csv", skiprows = 17)
C14_barstow = pd.read_csv("PVCellData/14_Barstow.csv", skiprows = 17)

C15_blythe = pd.read_csv("PVCellData/15_Blythe.csv", skiprows = 17)
C15_needles = pd.read_csv("PVCellData/15_Needles.csv", skiprows = 17)

C16_bishop = pd.read_csv("PVCellData/16_Bishop.csv", skiprows = 17)
C16_mtshasta = pd.read_csv("PVCellData/16_Mtshasta.csv", skiprows = 17)

# Key: Climate number
# Value: List of tables for 2-3 cities from the climate.
# Table cols: 
# Month, Day, Hour, Beam Irradiance (W/m^2), Diffuse Irradiance (W/m^2), Ambient Temperature (C), Wind Speed (m/s),
# Plane of Array Irradiance (W/m^2), Cell Temperature (C), DC Array Output (W), AC System Output (W)
climateDict = {
    1 : [C1_arcata, C1_eureka],
    2 : [C2_napa, C2_sanrafael],
    3 : [C3_oakland, C3_redwoodcity, C3_sf],
    4 : [C4_gilroy, C4_sanjose, C4_sunnyvale],
    5 : [C5_santamaria, C5_slo],
    6 : [C6_longbeach, C6_santabarbara],
    7 : [C7_oceanside, C7_sandiego],
    8 : [C8_anaheim, C8_tustin],
    9 : [C9_la, C9_pasadena],
    10 : [C10_riverside, C10_sanbernardino],
    11 : [C11_marysville, C11_redbluff],
    12 : [C12_merced, C12_stockton],
    13 : [C13_bakersfield, C13_fresno],
    14 : [C14_29palms, C14_barstow],
    15 : [C15_blythe, C15_needles],
    16 : [C16_bishop, C16_mtshasta]
}

# Input: 1 <= climate <= 16, 1 <= month <= 12
# Returns a dictionary with hour (0 -> 23) as keys and kW as values.
def averageHourlyKWInMonth(climate, month):
    assert climate >= 1 and climate <= 16
    assert month >= 1 and month <= 12
    hourlyDict = {}
    cities = climateDict.get(climate)
    days = days_in_month(month)
    for city in cities:
        monthTable = city[city['Month'] == str(month)]
        for hour in range(24):
            sumKWH = monthTable[monthTable['Hour'] == str(hour)]['AC System Output (W)'].sum()
            averageKWH = sumKWH / days
            hourlyDict[hour] = averageKWH
    return hourlyDict
            
# Input: 1 <= climate <= 16
# Returns a tuple (Month, Day, Demand) that represents the highest peak demand day of the year for the given climate.
def dailyPeakDemand(climate):
    assert climate >= 1 and climate <= 16
    cities = climateDict.get(climate)
    peakMonth = 0
    peakDay = 0
    peakDailyDemand = 0
    for city in cities:
        for month in range(1, 13):
            days = days_in_month(month)
            monthTable = city[city['Month'] == str(month)]
            for day in range(days):
                dailyDemand = monthTable[monthTable['Day'] == str(day)]['AC System Output (W)'].sum()
                if (dailyDemand > peakDailyDemand):
                    peakDailyDemand = dailyDemand
                    peakMonth = month
                    peakDay = day
    return (peakMonth, peakDay, peakDailyDemand / 1000)

# Input: 1 <= climate <= 16
# Returns a tuple (Month, Demand) that represents the highest peak demand month of the year for the given climate.
def monthlyPeakDemand(climate):
    assert climate >= 1 and climate <= 16
    cities = climateDict.get(climate)
    peakMonth = 0
    peakMonthlyDemand = 0
    for city in cities:
        for month in range(1, 13):
            monthlyDemand = city[city['Month'] == str(month)]['AC System Output (W)'].sum()
            if (monthlyDemand > peakMonthlyDemand):
                peakMonth = month
                peakMonthlyDemand = monthlyDemand
    return (peakMonth, peakMonthlyDemand / 1000)

# Input: 1 <= climate <= 16
# Returns the demand in KW of the most demanding city between 2-3 cities in the given climate.
def peakYearlyDemand(climate):
    assert climate >= 1 and climate <= 16
    cities = climateDict.get(climate)
    demand = 0
    for city in cities:
        cityDemand = city[city['Month'] == 'Totals']['AC System Output (W)'][8760]
        if (demand < cityDemand):
            demand = cityDemand
    return demand / 1000

# Input: 1 <= climate <= 16
# Returns the average demand in KW of 2-3 cities in the given climate.
def averageYearlyDemand(climate):
    assert climate >= 1 and climate <= 16
    cities = climateDict.get(climate)
    sum = 0
    for city in cities:
        sum += city[city['Month'] == 'Totals']['AC System Output (W)'][8760]
    return (sum / len(cities)) / 1000

# Helper function to get how many days in a year there are.
def days_in_month(month, year=2019):
    return monthrange(year, month)[1]