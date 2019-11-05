import pandas as pd 

demand = pd.read_csv('01-01-19.csv').iloc[[2]]
emissions = pd.read_csv('01-01-19-Emissions.csv')

dseries = demand.mean(axis = 1)
eseries = emissions.mean(axis = 1)

print(dseries.iat[0])
print(eseries.iat[0])
