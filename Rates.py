import csv

consumption_patterns = {
    'summer_weekday' : [1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1],
    'summer_weekend' : [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    'nonsummer_weekday' : [3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3],
    'nonsummer_weekend' : [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
}
class Day:
    def __init__(self, season, weekday, use=None):
        if use is None:
            use = []
        self.season = season
        self.weekday = weekday
        self.use = use
        if not self.use:
            if season == "summer":
                if weekday == "weekday":
                    self.use = consumption_patterns['summer_weekday']
                else:
                    self.use = consumption_patterns['summer_weekend']
            else:
                if weekday == "weekday":
                    self.use = consumption_patterns['nonsummer_weekday']
                else:
                    self.use = consumption_patterns['nonsummer_weekend']
        self.dayuse = sum(self.use)


with open('filler.csv') as file:
    read = csv.reader(file, delimiter=',')
    # assumes data in the format {date, season, day of week, use}
    daylist = []
    for row in read:
        daylist.append(Day(row[1], row[2]))


def flat(daylist, price=0.17):
    totaluse = 0
    for day in daylist:
        totaluse = totaluse + day.dayuse
    return totaluse * price


def tier(daylist, baseline=15, tier1=0.22376, tier2=0.28159, tier3=0.49334):
    # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-1.pdf
    totaluse = 0
    for day in daylist:
        totaluse = totaluse + day.dayuse
    return min(baseline, totaluse) * tier1 + max(0, totaluse - baseline) * tier2 + max(0, totaluse - 4*baseline) * tier3


def tou(daylist, speak=0.25354, soffpeak=0.20657, wpeak=0.18022, woffpeak=0.17133):
    # https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_EL-TOU.pdf
    speaksum = 0
    soffpeaksum = 0
    wpeaksum = 0
    woffpeaksum = 0
    for day in daylist:
        if day.season == "summer":
            if day.weekday == "weekday":
                speaksum = speaksum + sum(day.use[15:20])
                soffpeaksum = soffpeaksum + sum(day.use[0:14]) + sum(day.use[21:23])
            else:
                soffpeaksum = soffpeaksum + sum(day.use)
        else:
            if day.weekday == "weekday":
                wpeaksum = wpeaksum + sum(day.use[15:20])
                woffpeaksum = woffpeaksum + sum(day.use[0:14]) + sum(day.use[21:23])
            else:
                woffpeaksum = woffpeaksum + day.dayuse
    return speaksum * speak + soffpeaksum * soffpeak + wpeaksum * wpeak + woffpeaksum * woffpeak


print(flat(daylist))
print(tier(daylist))
print(tou(daylist))

