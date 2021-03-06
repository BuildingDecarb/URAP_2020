import csv
import sys
from Housing_Class1 import HouseType
from Appliances_Class import *

hourly_energy = [{} for x in range(16)]

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

"""
def update_dictionary(cznum, year, end_use):
    
    For the code below, we assume a particular file.
    In reality, the file will change based on the climate zone and year.
    
    with open('pge-res-PGSA-res_misc-noKW-Care-0.4_0.5.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    curr_dict = hourly_energy[cznum];
    curr_dict[(year, end_use)] = []
    for row in readCSV:
        total_energy = row[5]
        curr_dict[(year, end_use)].append(total_energy)
"""


def update_dictionary(filename, year, end_use):
    with open(filename, 'r') as csvfile:
        read_csv = csv.reader(csvfile)
        for cznum in range(16):
            csvfile.seek(0)
            first = True
            hourly_energy[cznum][(year, end_use)] = []
            for row in read_csv:
                if first:
                    first = False
                    continue
                hourly_energy[cznum][(year, end_use)].append(float(row[cznum + 1]))


def get_hourly_usage_for_year(cznum, year, end_use):
    """
    Helper function to access the appropriate hourly usage for a particular cznum, year, and end use.
    Returns a list of size 8760 with all the hourly energy usage.
    """
    return hourly_energy[cznum - 1][(year, end_use)]


def get_annual_usage(cznum, year, end_uses):
    result = {}
    for end_use in end_uses:
        result[end_use] = sum(get_hourly_usage_for_year(cznum, year, end_use))
    return result


def get_hourly_usage_for_seasons(season, cznum, year, end_uses):
    """
    Calculates the energy used for a particular season.
    """
    st_month = seasons[season][0]
    end_month = seasons[season][1]
    return get_hourly_usage_for_months(st_month, end_month, cznum, year, end_uses)


def get_hourly_usage_for_months(st_month, end_month, cznum, year, end_uses, st_hour=0, end_hour=23):
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
    return hour_range(st_hour, end_hour, st_day, end_day, cznum, year, end_uses)


def get_peak_energy_usage_per_month(cznum, year, end_uses):
    """
    Gets the maximum energy usage and corresponding hour for each month
    """
    result = {}
    for end_use in end_uses:
        current = get_hourly_usage_for_year(cznum, year, end_use)
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


def hour_range(st_hour, end_hour, st_day, end_day, cznum, year, end_uses):
    """
    Calculates the energy used for a particular time range across a day range.
    Ex: st_hour = 10, end_hour = 18, st_day = 0, end_day = 30
    Returns the total hourly energy used from 10 a.m. to 6 p.m. each day
    from January 1st to January 31st.
    """
    result = {}
    for end_use in end_uses:
        total = 0
        hourly_usage_for_year = get_hourly_usage_for_year(cznum, year, end_use)
        for i in range(st_day, end_day + 1):
            for j in range(st_hour, end_hour + 1):
                day_in_hours = i * 24
                total += hourly_usage_for_year[day_in_hours + j]
        # print(end_day * 24 + end_hour)
        result[end_use] = total
    return result


if __name__ == "__main__":
    end_uses = []
    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
        end_use = filename[0:5]
        HouseType.update_dictionary(filename, 2014, end_use)
        end_uses.append(end_use)
    hp_sh = Device('HP_SH', None, None, None, 15, None, None, None, None, None, None, 1, None, None, hasRefrigerant=True, refrigerant=Ref11)
    hp_wh = Device('HP_WH', None, None, None, 15, None, None, None, None, None, None, None, None, None)
    # er_wh = Device('ER_WH', None, None, None, 3, None, None, None, None, None, None, None, None, None)
    devices = []
    devices.append(hp_sh)
    devices.append(hp_wh)
    #devices.append(er_wh)
    """for i in range(1, 17):
        house = HouseType('SF', 1, i, 0, 0, 0, devices)
        annual_usage = house.get_annual_usage(i, "2011", house.end_uses)
        print("Climate zone {} annual usage: {}".format(i, annual_usage))
        # year = get_hourly_usage_for_months("Jan", "Dec", i, "2011", end_use)"""
    devices_SH_HP = []
    devices_SH_HP.append(hp_sh)
    devices_SH_HP.append(hp_wh)
    house_SH_HP = HouseType('House in CZ 15 with SH and HP', 1, 15, 0, 0, 0, devices_SH_HP)
    house_SH_HP.create_year_dict(2014)

    for month in months:
        print("{} energy usage: {}".format(month, house_SH_HP.get_hourly_usage_for_months(month, month, 2014)))

    print("TEST ANNUAL ENERGY USAGE AND EMISSIONS")
    print("{} annual usage: {}".format(house_SH_HP.type, house_SH_HP.get_total_annual_usage(2014)))
    print("{} annual emissions including refrigerant leakage: {}".format(house_SH_HP.type, house_SH_HP.get_total_annual_emissions(2014)))
    print("{} annual emissions not including refrigerant leakage: {}\n".format(house_SH_HP.type, house_SH_HP.get_annual_emissions(2014)))

    print("TEST MONTHLY ENERGY USAGE AND EMISSIONS")
    print("{} January usage: {}".format(house_SH_HP.type, house_SH_HP.get_hourly_usage_for_months('Jan', 'Jan', 2014)))
    print("{} January emissions: {}\n".format(house_SH_HP.type, house_SH_HP.get_monthly_emissions('Jan', 'Jan', 2014)))

    print("TEST FLAT, TIERED, AND TOU RATE FOR ANNUAL ENERGY USAGE")
    print("Yearly energy costs under flat rate plan: {}".format(house_SH_HP.yearly_cost('flat')))
    print("April-December energy costs under flat rate plan: {}".format(house_SH_HP.flat_month(4, 12)))
    print("Yearly energy costs under tiered rate plan: {}".format(house_SH_HP.yearly_cost('tier')))
    print("April-December energy costs under tiered rate plan: {}".format(house_SH_HP.tier_month(4, 12)))
    # print("January energy costs under tiered rate plan: {}".format(house_SH_HP.tier_month(1, 1)))
    # print("June energy costs under tiered rate plan: {}".format(house_SH_HP.tier_month(6, 6)))
    print("Yearly energy costs under tou rate plan: {}".format(house_SH_HP.yearly_cost('tou')))  # STILL NEED TO TEST
    print("April-December energy costs under tou rate plan: {}".format(house_SH_HP.tou_month(4, 12)))

    # print("\nANNUAL EMISSIONS BASED ON HOURLY RATES")
    # print(house_SH_HP.get_annual_emissions_hourly())
"""
    total = 0
    for key in months.keys():
        monthly_usage = get_hourly_usage_for_months(key, key, i, "2011", end_use)
        total += monthly_usage
        print("{} monthly usage: {}".format(key, monthly_usage))
    print(total)
    """
