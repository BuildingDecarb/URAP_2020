months_to_hours = {}
days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]

def get_hourly_usage_for_year(cznum, year, end_use):
    return hourly_energy[cznum][(year, end_use)]

def hour_range(st_hour, end_hour, cznum, year, end_use):
    total = 0
    hourly_usage_for_year = get_hourly_usage_for_year(cznum, year, end_use)
    for i in range(8760):
        for j in range(st_hour, end_hour):
            total += hourly_usage_for_year[i + j]
    return total