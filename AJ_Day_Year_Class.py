#Amy Jiang's code
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

monthbeg = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335] #first day of month
monthend = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365] #last day of month
lyear = [1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336] #for leap years
monthnames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class Day:
    """
    Class representing a day in the year.
    Attributes:
        weekday (int): day of the week of this Day
        season (string): season of this Day
        use (int[]): hourly energy use
    """
    def __init__(self, use):
        self.season = "winter"
        self.weekday = "weekday"
        self.use = use
       
        
    def setSeason(self, season):
        self.season = season
    
    def setDay(self, weekday):
        self.weekday = weekday


class Year:
    """
    Class representing a year. 
    Attributes:
        name (string): the energy source that the Year is representing
        daylist (Day[]): days in this Year
    """
    def __init__(self, dataframe=None, name=None, column=None):
        self.name = name  
        self.daylist = []  #an array of days
        use = []
        if dataframe is None:
            for i in range(0, 365): #assume 365 days in year
                self.daylist.append(Day(np.zeros(24)))
        else:
            for i in range(1, dataframe.shape[0] + 1):
                use.append(dataframe.loc[i - 1, column])
                if i%24 == 0:
                    self.daylist.append(Day(use))
                    use = []

    def distributeWeekday(self, jan1): 
        """
        Attributes a day of the week for each Day.
        Parameters:
            jan1 (int): day of week for the first day of the year (monday = 1, ...sunday = 7)
        """
        for day in self.daylist:
            if jan1%7 == 6 or jan1%7 == 0:
                day.weekday = 'weekend'
            jan1 = jan1 + 1
    def distributeSeason(self):
        """
        Attributes a season {winter, summer} to each Day of the Year, according to PG&E's description.
        """
        i = 1
        for day in self.daylist:
            if i >= monthbeg[5] and i < monthbeg[9]:  #june through SEpt as per SCE
                day.season = 'summer'                 #https://www.sce.com/residential/rates/Time-Of-Use-Residential-Rate-Plans
                i = i + 1
            else:
                 day.season = 'winter'
                 i = i+1
    
    def sumYear(self):
        """
        Sums daily energy use to find total energy use in the Year.
        """
        yearuse = 0
        for day in self.daylist:
            yearuse = yearuse + sum(day.use)
        return yearuse        
