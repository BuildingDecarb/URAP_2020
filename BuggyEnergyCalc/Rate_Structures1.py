SeasonDict = {1: 'Winter', 2: 'Winter', 3: 'Winter', 4: 'Winter', 5: 'Winter', 6: 'Summer', 7: 'Summer',
                     8: 'Summer', 9: 'Summer', 10: 'Winter', 11: 'Winter', 12: 'Winter'}  

month_indices = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6,
                     'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}


month_names= {0:'January', 1:'February', 2:'March', 3: 'April', 4: 'May', 5: 'June', 6: 'July',
                     7: 'August', 8:'September', 9: 'October', 10:'November', 11: 'December' }# reversed

beg = [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016] #first day of month
end = [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760] #last day of month
#leapYear = [744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040, 8784] #for leap years


class Rate_Struct():

    @staticmethod
    def peakDays():
        return [0, 1, 2, 3, 4]
    @staticmethod
    def offPeakDays():
        return [5, 6]    #Weekend
    @staticmethod
    def peakHours():   
        return [  17, 18, 19, 20]
    @staticmethod
    def offPeakHours():
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,16,21, 22,  23]
#______BELOW PGE Residential E-TOU_E..............
  
    @staticmethod
    def monthlyBaseAmt(monthName):
        delMinBillAmt = 0.32854   #PGE_E_TOU_D ++both for summer and winter
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/28
       # print "test month_days", monthName,month_days
        return delMinBillAmt * month_days           # ~fixed cost

    @staticmethod
    def baselineCredit(monthName):
        basecredit = 0   #PGE_E_TOU_D ++both for summer and winter
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/28
        #print "test month_days", monthName,month_days
        return basecredit * month_days           # ~fixed cost
    

    @staticmethod
    def feedInTariff():    #SOLAR excess generation fed into the ground
        return 0.05
 
    @staticmethod
    def summerPeakRate():
        return 0.36618
    @staticmethod
    def summerOffPeakRate():
        return 0.27122

    @staticmethod
    def winterPeakRate():
        return 0.29231

    @staticmethod
    def winterOffPeakRate():
        return 0.27493




class Rate_Struct_C(Rate_Struct):

    @staticmethod
    def peakHours():
        return [ 16, 17, 18, 19, 20,21]
    @staticmethod
    def offPeakHour():
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,  22,  23]
#-------------------     
    @staticmethod
    def baselineCredit(monthName):
        basecredit = 0.07315   #PGE_E_TOU_D ++both for summer and winter
        index = month_indices.get(monthName)
        monthBeg = beg[index]
        monthEnd = end[index]
        month_days = (monthEnd - monthBeg)/28
      #  print "test month_days", monthName,month_days
        return basecredit * month_days           # ~fixed cost
    

    @staticmethod
    def feedInTariff():    #SOLAR excess generation fed into the ground
        return 0.05
 
    @staticmethod
    def summerPeakRate():
        return 0.40392
    @staticmethod
    def summerOffPeakRate():
        return 0.30086

    @staticmethod
    def winterPeakRate():
        return 0.26645

    @staticmethod
    def winterOffPeakRate():
        return 0.24765

#==========================================================================


def findRate(season, day, time, rs):

    if (time in rs.peakHours()) and (day in rs.peakDays()):
            if season == 'Winter':
                    rate = rs.winterPeakRate()
            if season == 'Summer': 
                    rate = rs.summerPeakRate()
               
    elif (time in rs.peakHours()) and (day in rs.offPeakDays()):
            if season == 'Winter':
                rate = rs.winterPeakRate()
            if season == 'Summer': 
                    rate = rs.summerPeakRate()
               
    elif (time in rs.offPeakHours()) and (day in rs.offPeakDays()):
            if season == 'Winter':
                rate = rs.winterOffPeakRate()
            if season == 'Summer': 
                rate = rs.summerOffPeakRate()
        
    else:
            if season == 'Winter':
                rate = rs.winterOffPeakRate()
            if season == 'Summer': 
                rate = rs.summerOffPeakRate()
    #print "season rate", season, day, time, rate       
    return rate



