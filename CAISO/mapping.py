import pandas as pd 

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

month_table = pd.DataFrame(data_list, index=labels)
energy_table = pd.DataFrame(energy_data_list, index=labels)
# print("Emissions:")
# print(month_table)
# print("\nEnergy usage:")
# print(energy_table)
rates = month_table / energy_table
# print("\nEmission rates in kg CO2/kWh:")
# print(rates)
jan = rates.iloc[0]
print(jan)
for item in jan.iteritems():
    print(item[1])
# month_table.to_csv('month_table.csv', index=True)
# energy_table.to_csv('energy_table.csv', index=True)
# rates.to_csv('rates.csv', index=True)
