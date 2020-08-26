#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
plt.style.use('fivethirtyeight')
sns.set_context("notebook")
import datetime


# 2014-07-31 19:00:00 has highest demand

# Based on PGF1

# In[2]:


decile_0 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.0_0.1.csv") 
decile_1 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.1_0.2.csv") 
decile_2 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.2_0.3.csv") 
decile_3 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.3_0.4.csv") 
decile_4 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.4_0.5.csv") 
decile_5 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.5_0.6.csv") 
decile_6 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.6_0.7.csv") 
decile_7 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.7_0.8.csv") 
decile_8 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.8_0.9.csv") 
decile_9 = pd.read_csv("CLEAN_BASE_COOLING_base_pge-res-PGF1-res_misc-noKW-Care-0.9_1.0.csv") 


# In[3]:


decile_0.columns = ["datetime", "cooling", "cooling+baseload"]
decile_0["datetime"] = pd.to_datetime(decile_0["datetime"])
decile_0["date"] = 0
for i in range(0, len(decile_0)):
    decile_0["date"][i] = str(decile_0["datetime"][i].date())
decile_0["cooling percent"] = decile_0["cooling"]/decile_0["cooling+baseload"]
highest = decile_0.loc[(decile_0["date"] == "2014-07-31")]
highest["hour"] = highest.datetime.dt.hour


# In[4]:


decile_1.columns = ["datetime", "cooling", "cooling+baseload"]
decile_1["datetime"] = pd.to_datetime(decile_1["datetime"])
decile_1["date"] = 0
for i in range(0, len(decile_1)):
    decile_1["date"][i] = str(decile_1["datetime"][i].date())
decile_1["cooling percent"] = decile_1["cooling"]/decile_1["cooling+baseload"]
highest_1 = decile_1.loc[(decile_1["date"] == "2014-07-31")]
highest_1["hour"] = highest_1.datetime.dt.hour


# In[5]:


decile_2.columns = ["datetime", "cooling", "cooling+baseload"]
decile_2["datetime"] = pd.to_datetime(decile_2["datetime"])
decile_2["date"] = 0
for i in range(0, len(decile_2)):
    decile_2["date"][i] = str(decile_2["datetime"][i].date())
decile_2["cooling percent"] = decile_2["cooling"]/decile_2["cooling+baseload"]
highest_2 = decile_2.loc[(decile_2["date"] == "2014-07-31")]
highest_2["hour"] = highest_2.datetime.dt.hour


# In[6]:


decile_3.columns = ["datetime", "cooling", "cooling+baseload"]
decile_3["datetime"] = pd.to_datetime(decile_3["datetime"])
decile_3["date"] = 0
for i in range(0, len(decile_3)):
    decile_3["date"][i] = str(decile_3["datetime"][i].date())
decile_3["cooling percent"] = decile_3["cooling"]/decile_3["cooling+baseload"]
highest_3 = decile_3.loc[(decile_3["date"] == "2014-07-31")]
highest_3["hour"] = highest_3.datetime.dt.hour


# In[7]:


decile_4.columns = ["datetime", "cooling", "cooling+baseload"]
decile_4["datetime"] = pd.to_datetime(decile_4["datetime"])
decile_4["date"] = 0
for i in range(0, len(decile_4)):
    decile_4["date"][i] = str(decile_4["datetime"][i].date())
decile_4["cooling percent"] = decile_4["cooling"]/decile_4["cooling+baseload"]
highest_4 = decile_4.loc[(decile_4["date"] == "2014-07-31")]
highest_4["hour"] = highest_4.datetime.dt.hour


# In[8]:


decile_5.columns = ["datetime", "cooling", "cooling+baseload"]
decile_5["datetime"] = pd.to_datetime(decile_5["datetime"])
decile_5["date"] = 0
for i in range(0, len(decile_5)):
    decile_5["date"][i] = str(decile_5["datetime"][i].date())
decile_5["cooling percent"] = decile_5["cooling"]/decile_5["cooling+baseload"]
highest_5 = decile_5.loc[(decile_5["date"] == "2054-07-31")]
highest_5["hour"] = highest_5.datetime.dt.hour
summer_data5 = decile_5.loc[(decile_5["date"] > "2014-05-31") & (decile_5["date"] < "2014-09-01")]


# In[9]:


decile_6.columns = ["datetime", "cooling", "cooling+baseload"]
decile_6["datetime"] = pd.to_datetime(decile_6["datetime"])
decile_6["date"] = 0
for i in range(0, len(decile_6)):
    decile_6["date"][i] = str(decile_6["datetime"][i].date())
decile_6["cooling percent"] = decile_6["cooling"]/decile_6["cooling+baseload"]
highest_6 = decile_6.loc[(decile_6["date"] == "2014-07-31")]
highest_6["hour"] = highest_6.datetime.dt.hour


# In[10]:


decile_7.columns = ["datetime", "cooling", "cooling+baseload"]
decile_7["datetime"] = pd.to_datetime(decile_7["datetime"])
decile_7["date"] = 0
for i in range(0, len(decile_7)):
    decile_7["date"][i] = str(decile_7["datetime"][i].date())
decile_7["cooling percent"] = decile_7["cooling"]/decile_7["cooling+baseload"]
highest_7 = decile_7.loc[(decile_7["date"] == "2014-07-31")]
highest_7["hour"] = highest_7.datetime.dt.hour


# In[11]:


decile_8.columns = ["datetime", "cooling", "cooling+baseload"]
decile_8["datetime"] = pd.to_datetime(decile_8["datetime"])
decile_8["date"] = 0
for i in range(0, len(decile_8)):
    decile_8["date"][i] = str(decile_8["datetime"][i].date())
decile_8["cooling percent"] = decile_8["cooling"]/decile_8["cooling+baseload"]
highest_8 = decile_8.loc[(decile_8["date"] == "2014-07-31")]
highest_8["hour"] = highest_8.datetime.dt.hour


# In[12]:


decile_9.columns = ["datetime", "cooling", "cooling+baseload"]
decile_9["datetime"] = pd.to_datetime(decile_9["datetime"])
decile_9["date"] = 0
for i in range(0, len(decile_9)):
    decile_9["date"][i] = str(decile_9["datetime"][i].date())
decile_9["cooling percent"] = decile_9["cooling"]/decile_9["cooling+baseload"]
highest_9 = decile_9.loc[(decile_9["date"] == "2014-07-31")]
highest_9["hour"] = highest_9.datetime.dt.hour


# In[13]:


#0
line1, = plt.plot(highest["hour"], highest["cooling"], color = 'b', marker='o')
line2, = plt.plot(highest["hour"], highest["cooling+baseload"], color = 'b')

line3, = plt.plot(highest_1["hour"], highest_1["cooling"], color = 'g', marker='o')
line4, = plt.plot(highest_1["hour"], highest_1["cooling+baseload"], color = 'g')
#2
line5, = plt.plot(highest_2["hour"], highest_2["cooling"], color = 'm', marker='o')
line6, = plt.plot(highest_2["hour"], highest_2["cooling+baseload"], color = 'm')
#3
line7, = plt.plot(highest_3["hour"], highest_3["cooling"], color = 'y', marker='o')
line8, = plt.plot(highest_3["hour"], highest_3["cooling+baseload"], color = 'y')
#4
line9, = plt.plot(highest_4["hour"], highest_4["cooling"], color = 'k', marker='o')
line10, = plt.plot(highest_4["hour"], highest_4["cooling+baseload"], color = 'k')
#5
line11, = plt.plot(highest_5["hour"], highest_5["cooling"], color = 'c', marker='o')
line12, = plt.plot(highest_5["hour"], highest_5["cooling+baseload"], color = 'c')
#6
line13, = plt.plot(highest_6["hour"], highest_6["cooling"], color = 'r', marker='o')
line14, = plt.plot(highest_6["hour"], highest_6["cooling+baseload"], color = 'r')
#7
line15, = plt.plot(highest_7["hour"], highest_7["cooling"], color = 'lime', marker='o')
line16, = plt.plot(highest_7["hour"], highest_7["cooling+baseload"], color = 'lime')
#8
line17, = plt.plot(highest_8["hour"], highest_8["cooling"], color = 'darkgrey', marker='o')
line18, = plt.plot(highest_8["hour"], highest_8["cooling+baseload"], color = 'darkgrey')
#9
line19, = plt.plot(highest_9["hour"], highest_9["cooling"], color = 'lightpink', marker='o')
line20, = plt.plot(highest_9["hour"], highest_9["cooling+baseload"], color = 'lightpink')

plt.legend([line1, line3, line5, line7, line9, line11, line13, 
           line15, line17, line19], [ '0-0.1','.1-.2', '.2-.3','.3-.4', '.4-.5','.5-.6',
                                                                            '.6-.7', '.7-.8', '.8-.9','.9-1.0'], loc="upper left", bbox_to_anchor=(0.5, -0.15), ncol= 2)
plt.title("Peak Day (7/31/14) Cooling + Baseload and Cooling")
plt.xlabel("Hours")
plt.ylabel("Load in kWh")
plt.show()


# In[14]:


line1, = plt.plot(highest["hour"], highest["cooling percent"], color = 'b')

line2, = plt.plot(highest_1["hour"], highest_1["cooling percent"])

line3, = plt.plot(highest_2["hour"], highest_2["cooling percent"])

line4, = plt.plot(highest_3["hour"], highest_3["cooling percent"])

line5, = plt.plot(highest_4["hour"], highest_4["cooling percent"])

line6, = plt.plot(highest_5["hour"], highest_5["cooling percent"])

line7, = plt.plot(highest_6["hour"], highest_6["cooling percent"])

line8, = plt.plot(highest_7["hour"], highest_7["cooling percent"], color = 'y')

line9, = plt.plot(highest_8["hour"], highest_8["cooling percent"], color = 'k')

line10, = plt.plot(highest_9["hour"], highest_9["cooling percent"], color = 'g')


plt.legend([line1, line2, line3, line4, line5, line6, line7, line8, line9, line10], ['0-0.1', '.1-.2', '.2-.3', '.3-.4', '.4-.5',
                                                                            '.5-.6', '.6-.7', '.7-.8', '.8-.9', '.9-1.0'], loc="upper left", bbox_to_anchor=(0.5, -0.15), ncol= 2)
#plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol= 2)
plt.title("Cooling/Total on Peak Day (7/31/14)")
plt.xlabel("Hours")
plt.ylabel("Load in kWh")
plt.show()


# In[15]:


line1, = plt.plot(summer_data5["datetime"], summer_data5["cooling"])
line2, = plt.plot(summer_data5["datetime"], summer_data5["cooling+baseload"]);
plt.legend([line1, line2], ['cooling','cooling+baseload'])
plt.xticks(rotation = 90)
plt.title(".5-.6 Cooling and Baseload for Summer Months")
plt.xlabel("Dates")
plt.ylabel("Load")


# In[16]:


mean_day = summer_data5.groupby("date").mean()
mean_day = mean_day.reset_index()


# In[17]:


line1, = plt.plot(mean_day["date"], mean_day["cooling"])
line2, = plt.plot(mean_day["date"], mean_day["cooling+baseload"]);
plt.legend([line1, line2], ['cooling','cooling+baseload'])
plt.xticks(rotation = 90)
plt.xlabel("date")
plt.ylabel("load")
plt.title("Average Cooling+Baseload and Cooling for .5-.6")
plt.show()


# In[18]:


top_10_highest_demand = decile_5.sort_values("cooling+baseload", ascending = False).head(10)["datetime"]
top_10_highest_demand


# In[20]:


august_data = summer_data5.loc[(decile_5["date"] > "2014-07-31") & (summer_data5["date"] < "2014-09-01")]


# In[25]:


chart = sns.boxplot(x = 'date', y = 'cooling+baseload', data =august_data)
chart.set_xticklabels(labels = august_data["date"].unique(), rotation=90)
plt.title(".5-.6 August Cooling + Baseload")
plt.show()


# In[22]:


top_10_lowest_demand = decile_5.sort_values("cooling+baseload", ascending = True).head(10)["datetime"]
top_10_lowest_demand


# In[23]:


april_data = decile_5.loc[(decile_5["date"] >= "2014-04-01") & (decile_5["date"] < "2014-05-01")]


# In[27]:


chart = sns.boxplot(x = 'date', y = 'cooling+baseload', data =april_data)
chart.set_xticklabels(labels = april_data["date"].unique(), rotation=90)
plt.title(".5-.6 April Cooling + Baseload")
plt.show()

