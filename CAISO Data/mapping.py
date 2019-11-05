import pandas as pd 

for i in range(1, 12):
    demand = pd.read_csv('{}-1-19.csv'.format(i)).iloc[[2]]
    emissions = pd.read_csv('{}-1-19-Emissions.csv'.format(i))

    d_series = demand.mean(axis=1)
    e_series = emissions.mean(axis=1)
    avg_demand = d_series.iat[0]
    avg_emissions = e_series.iat[0]
    print("Month {} CO2 emissions rate: {} kgCO2/kWH".format(i, avg_emissions/avg_demand))
