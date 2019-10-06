import csv

"""For the code below, we assume a particular file.
   In reality, the file will change based on the
   climate zone and year"""

def update_dictionary(cznum, year, end_use):
	with open('pge-res-PGSA-res_misc-noKW-Care-0.4_0.5.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter = ',')
	curr_dict = hourly_energy[cznum];
	curr_dict[(year, end_use)] = []
	for row in readCSV:
		total_energy = row[5]
		curr_dict[(year, end_use)].append(total_energy)


months_to_hours = {}
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


def get_hourly_usage_for_year(cznum, year, end_use):
    return hourly_energy[cznum][(year, end_use)]


def get_hourly_usage_for_seasons(season, cznum, year, end_use):
    st_month = seasons[season][0]
    end_month = seasons[season][1]
    return get_hourly_usage_for_months(st_month, end_month, cznum, year, end_use)


def get_hourly_usage_for_months(st_month, end_month, cznum, year, end_use, st_hour=0, end_hour=23):
    st_month_num = months[st_month]
    end_month_num = months[end_month]
    st_day = 0
    for i in range(st_month_num):
        st_day += days_in_months[i]
    end_day = 0
    for i in range(end_month_num + 1):
        end_day += days_in_months[i]
    end_day -= 1
    return hour_range(st_hour, end_hour, st_day, end_day, cznum, year, end_use)


def hour_range(st_hour, end_hour, st_day, end_day, cznum, year, end_use):
    total = 0
    hourly_usage_for_year = get_hourly_usage_for_year(cznum, year, end_use)
    for i in range(st_day, end_day):
        for j in range(st_hour, end_hour):
            total += hourly_usage_for_year[i + j]
    return total