import pandas as pd
import matplotlib.pyplot as plt

months = {1: "Jan",
          2: "Feb",
          3: "Mar",
          4: "Apr",
          5: "May",
          6: "Jun",
          7: "Jul",
          8: "Aug",
          9: "Sep",
          10: "Oct",
          11: "Nov",
          12: "Dec"}

month_lengths = {1: 31,
                 2: 28,
                 3: 31,
                 4: 30,
                 5: 31,
                 6: 30,
                 7: 31,
                 8: 31,
                 9: 30,
                 10: 31,
                 11: 30,
                 12: 31}

"""for i in range(1, 12):
    demand = pd.read_csv('{}-1-19.csv'.format(i)).iloc[[2]]
    emissions = pd.read_csv('{}-1-19-Emissions.csv'.format(i))

    d_series = demand.mean(axis=1)
    e_series = emissions.mean(axis=1)
    avg_demand = d_series.iat[0]
    avg_emissions = e_series.iat[0]
    print("Month {} CO2 emissions rate: {} kgCO2/kWH".format(i, avg_emissions/avg_demand))"""

data_list = []
labels = ['Jan Hourly Avg', 'Feb Hourly Avg', 'Mar Hourly Avg', 'Apr Hourly Avg', 'May Hourly Avg', 'Jun Hourly Avg',
          'Jul Hourly Avg', 'Aug Hourly Avg', 'Sep Hourly Avg', 'Oct Hourly Avg', 'Nov Hourly Avg'] #No December data yet
for i in range(1, 12):
    storage = {}
    hour, segment, total = 1, 1, 0
    emissions = pd.read_csv('{}-1-19-Emissions.csv'.format(i))
    for i in range(1, emissions.shape[1]):
        total += emissions.iloc[0, i]
        segment += 1
        if segment == 13:
            segment = 1
            storage[hour] = total / 12
            hour += 1
            total = 0
    data_list.append(storage)

energy_data_list = []
for i in range(1, 12):
    energy_storage = {}
    hour, segment, total = 1, 1, 0
    energy_usage = pd.read_csv('{}-1-19.csv'.format(i))
    for i in range(1, energy_usage.shape[1]):
        total += energy_usage.iloc[0, i]
        segment += 1
        if segment == 13:
            segment = 1
            energy_storage[hour] = total / 12
            hour += 1
            total = 0
    energy_data_list.append(energy_storage)


def get_monthly_emissions(month):
    """
    Takes in a month number (1->January... 12->December) and returns the dataframe corresponding to the
    hourly emissions for each day of the month.
    """
    data_list = []
    labels = []
    for i in range(1, month_lengths[month] + 1):
        storage = {}
        hour, segment, total = 1, 1, 0
        emissions = pd.read_csv('{}-{}-19-Emissions.csv'.format(month, i))
        for i in range(1, emissions.shape[1]):
            total += emissions.iloc[0, i]
            segment += 1
            if segment == 13:
                segment = 1
                storage[hour] = total / 12
                hour += 1
                total = 0
        data_list.append(storage)
        labels.append("{} {} Hourly Avg".format(months[month], i))
    return pd.DataFrame(data_list, index=labels)


def get_monthly_energy(month):
    """
    Takes in a month number (1->January... 12->December) and returns the dataframe corresponding to the
    hourly energy usage for each day of the month.
    """
    energy_data_list = []
    labels = []
    for i in range(1, month_lengths[month] + 1):
        storage = {}
        hour, segment, total = 1, 1, 0
        emissions = pd.read_csv('{}-{}-19.csv'.format(month, i))
        for i in range(1, emissions.shape[1]):
            total += emissions.iloc[0, i]
            segment += 1
            if segment == 13:
                segment = 1
                storage[hour] = total / 12
                hour += 1
                total = 0
        energy_data_list.append(storage)
        labels.append("{} {} Hourly Avg".format(months[month], i))
    return pd.DataFrame(data_list, index=labels)


def get_monthy_rates(month):
    return get_monthly_emissions(month) / get_monthly_energy(month)


month_table = pd.DataFrame(data_list, index=labels)
energy_table = pd.DataFrame(energy_data_list, index=labels)
rates = month_table / energy_table


print("Emissions:")
print(month_table)
print("\nEnergy usage:")
print(energy_table)
print("\nEmission rates in kg CO2/kWh:")
print(rates)
"""

print("Jan Emissions:")
print(get_monthly_emissions(1))
print("\nJan Energy usage:")
print(get_monthly_energy(1))
print("\nJan Emission rates in kg CO2/kWh:")
print(get_monthy_rates(1))
"""


for i in range(1, 12):
    month = months[i]
    m = rates.iloc[i - 1]
    m = list(m.iteritems())
    m = [item[1] for item in m]
    x = range(24)
    plt.plot(x, m, label=month)
plt.legend()
plt.show()

for i in range(1, 12):
    month = months[i]
    m = get_monthy_rates(i)
    m = rates.iloc[i - 1]
    m = list(m.iteritems())
    m = [item[1] for item in m]
    x = range(month_lengths[i])
    plt.plot(x, m, label=month)
plt.legend()
plt.show()

# month_table.to_csv('month_table.csv', index=True)
# energy_table.to_csv('energy_table.csv', index=True)
# rates.to_csv('rates.csv', index=True)
