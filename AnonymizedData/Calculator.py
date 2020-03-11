import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from calendar import monthrange
from PricingScheme import *

wh_data, sh_data = None, None
care, noncare = [], []
care_cc, noncare_cc = [], []
def process_data():
    global wh_data, sh_data
    sh_data = pd.read_csv("../LoadHourlyProfileData/HP_SH_HourlyProfiles.csv")
    wh_data = pd.read_csv("../LoadHourlyProfileData/HP_WH_HourlyProfiles.csv")
    global care, noncare
    ds = pd.read_csv('anonymized_1in10_actual_actual_2014_cluster_summary.csv')
    for i in range(10):
        pre = 'pge-res-PGF1-res_misc-noKW-Care-'
        if i == 9:
            x = ds[ds['cluster'] == pre + '0.9_1.0'].loc[:, 'customer_count'].iloc[0]
            care_cc.append(int(x))
            care.append(pd.read_csv(pre + '0.9_1.0' + '.csv'))
        else:
            x = ds[ds['cluster'] == pre + '0.{}_0.{}'.format(i, i + 1)].loc[:, 'customer_count'].iloc[0]
            care_cc.append(int(x))
            care.append(pd.read_csv(pre + '0.{}_0.{}'.format(i, i + 1) + '.csv'))
    for i in range(10):
        pre = 'pge-res-PGF1-res_misc-noKW-nonCare-'
        if i == 9:
            x = ds[ds['cluster'] == pre + '0.9_1.0'].loc[:, 'customer_count'].iloc[0]
            noncare_cc.append(int(x))
            noncare.append(pd.read_csv(pre + '0.9_1.0' + '.csv'))
        else:
            x = ds[ds['cluster'] == pre + '0.{}_0.{}'.format(i, i + 1)].loc[:, 'customer_count'].iloc[0]
            noncare_cc.append(int(x))
            noncare.append(pd.read_csv(pre + '0.{}_0.{}'.format(i, i + 1) + '.csv'))

def energy_usage(data, month, climate_zone):
    total = 0
    days_in_month = monthrange(1, month)[1]
    for d in range(1, days_in_month + 1):
        day = date(1, month, d)
        r = date_to_range(day)
        for idx in range(r[0], r[1]):
            total += data.loc[idx].iloc[climate_zone]
    return total

# begin_date/end_date: use python datetime.date class
# pricing scheme will have a flat_rate, 
# tiers is a list of two-tuples: (threshold: price above that threshold)
# tou is a list of 3-tuples: (begin_time, end_time, rate)

'''
Calculates the cost of energe usage per month
'''
def cost(data, begin_date, end_date, climate_zone, pricing_scheme, div=1):
    # Take the appropriate column and data from climate_zone
    # Create data_climate_zone
    # PricingScheme.py
    return pricing_scheme.cost(data, climate_zone, begin_date, end_date, div)

process_data()
# june = energy_usage(sh_data, 6, 9)
# jan = energy_usage(sh_data, 1, 9)
# print(june, jan)
# c = cost(wh_data, date(1, 1, 1), date(1, 3, 1), 2, Scheme(scheme='tou'))

# total_care, total_noncare = [], []

# for i in range(10):
#     '''
#     total_care.append(sum(care[i].loc[:,'total']) / care_cc[i] / 8760) 
#     total_noncare.append(sum(noncare[i].loc[:,'total']) / noncare_cc[i] / 8760) 
#     '''
#     '''
#     total_care.append(cost(care[i], date(1, 1, 1), date(1, 12, 31), 5, Scheme(scheme='tiered'), div=care_cc[i]))
#     total_noncare.append(cost(noncare[i], date(1, 1, 1), date(1, 12, 31), 5, Scheme(scheme='tiered'), div=noncare_cc[i]))
#     '''
    
#     total_care.append(cost(care[i], date(1, 1, 1), date(1, 12, 31), 5, Scheme(scheme='tou')) / care_cc[i])
#     total_noncare.append(cost(noncare[i], date(1, 1, 1), date(1, 12, 31), 5, Scheme(scheme='tou')) / noncare_cc[i])
    

# print(total_care, total_noncare)
# import matplotlib.pyplot as plt
# labels = []
# for i in range(0, 100, 10):
#     labels.append("{}-{}".format(i, i + 10))
# x = np.arange(len(labels))
# width = 0.35
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, total_care, width, label='Care')
# rects1 = ax.bar(x + width/2, total_noncare, width, label='Non-care')
# ax.set_xlabel('Percentile')
# ax.set_ylabel('Cost of energy ($)')
# ax.set_title('Yearly cost of energy by consumption decile (TOU scheme)')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()
# fig.tight_layout()
# plt.show()
f, t, tou = [[], []], [[], []], [[], []]
for i in range(1, 14):
    f[0].append(cost(wh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='flat_rate', flat_rate=0.2)))
    f[1].append(cost(sh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='flat_rate', flat_rate=0.2)))
    t[0].append(cost(wh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='tiered')))
    t[1].append(cost(sh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='tiered')))
    tou[0].append(cost(wh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='tou')))
    tou[1].append(cost(sh_data, date(1, 1, 1), date(1, 12, 31), i, Scheme(scheme='tou')))
import matplotlib.pyplot as plt
labels = []
for i in range(1, 14):
    labels.append("CZ{}".format(i))
x = np.arange(len(labels))
width = 0.60
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, f[1], width / 3, label='Flat-rate')
rects1 = ax.bar(x - width/6, t[1], width / 3, label='Tiered')
rects1 = ax.bar(x + width/6, tou[1], width / 3, label='TOU')
ax.set_xlabel('Climate Zone')
ax.set_ylabel('Cost of energy ($)')
ax.set_title('Yearly space heating cost by climate zone/pricing scheme')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
fig.tight_layout()
plt.show()
