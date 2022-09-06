#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib_inline


# In[2]:


df_sandbox_calls = pd.read_csv('Sandbox_Calls.csv',index_col=0)


# In[37]:


df_sandbox_calls.info()


# In[5]:


df_sandbox_calls.head(2)


# In[6]:


df_sandbox_calls['Date'] = pd.to_datetime(df_sandbox_calls['client_received_start_timestamp'])


# In[7]:


df_sandbox_calls = df_sandbox_calls[['apiproxy','Date']]
df_sandbox_calls['No_of_Calls'] = 1


# In[8]:


df_sandbox_calls.head(2)


# In[9]:


df_sandbox = df_sandbox_calls[['apiproxy','Date']]
df_sandbox.head(2)


# In[10]:


df_sandbox.apiproxy.value_counts()


# In[11]:


get_ipython().system('pip install sidetable')


# In[12]:


import sidetable
# sidetable is mix of crosstab, groupby and value_counts
# sidetable can also be used for groupby totals, counts, subtotal, missing values, flattening table
# check the article https://github.com/chris1610/sidetable
df_sandbox.stb.freq(['apiproxy'],style = True, thresh = 99, other_label='Rest of Proxies')


# In[13]:


df_sandbox.head()


# In[16]:


df_sandbox["No_Of_Calls"] = 1


# In[38]:


#Pivot table using Grouper function
df_analysis_grouper = df_sandbox.pivot_table(index=pd.Grouper(key='Date', freq='M'),values=['apiproxy','No_Of_Calls'],aggfunc = np.sum)
df_analysis_grouper.head()


# In[39]:


plt.figure(figsize=(8,5))
sns.set(style="ticks")
ax1 = sns.lineplot(x='Date',y='No_Of_Calls',data=df_analysis_grouper)
# To avoid y axis values to convert in exponential format
ax1.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.title(label = 'Month wise no of calls',fontdict = {"fontsize":"15","color":"r"})
plt.yticks(np.arange(0,2400000,200000 ))
plt.grid()
plt.show()


# In[19]:


df_sandbox.head(2)


# In[20]:


#groupby using Grouper function
df_analysis_groupby = df_sandbox.groupby(['apiproxy',pd.Grouper(key = 'Date', freq='M')])["No_Of_Calls"].sum()
df_analysis_groupby.head()


# In[21]:


df_analysis_groupby=df_analysis_groupby.reset_index()
df_analysis_groupby.head()


# In[22]:


df_analysis_groupby = df_analysis_groupby.sort_values(by=['apiproxy','Date'],ascending=[True,False]).groupby(by='apiproxy').head(2)
df_analysis_groupby.head()


# In[23]:


#Filtering only april/may 2021 records
df_analysis_groupby = df_analysis_groupby.query("Date == '2021-05-31' or Date == '2021-04-30'")
df_analysis_groupby.head()


# In[40]:


#Percentage change in last 2 months
df_pct_change = df_analysis_groupby
df_pct_change['Pct_Change'] = df_pct_change.sort_values(by=['apiproxy','Date']).groupby(by = ['apiproxy'],sort=False)['No_Of_Calls'].apply(pd.Series.pct_change)
df_pct_change.head(10)


# In[25]:


df_prev_month = df_pct_change.query("No_Of_Calls>100 and Date=='2021-04-30'")
df_prev_month


# In[26]:


df_curr_month = df_pct_change.query("No_Of_Calls>100 and Date=='2021-05-31' and Pct_Change>0")
df_curr_month


# In[57]:


df_consolidated_col = df_curr_month.merge(df_prev_month,how='inner',on='apiproxy')
df_consolidated_col.sort_values(by='Pct_Change_x',ascending=False, inplace=True)
df_consolidated_col.head()


# In[58]:


df_consolidated_col['Pct_Change_x'] = df_consolidated_col.Pct_Change_x.apply(lambda x: x*100)
df_consolidated_col.head()


# In[80]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

ax = sns.barplot(x='apiproxy', y='Pct_Change_x', data=df_consolidated_col.head(10),hatch='/')

for p in ax.patches:
   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+0.1))

plt.title("% Increase in No of Calls (from last month)",fontdict={'family': 'serif',
        'color':  'darkred',
        'weight': 'bold',
        'size': 16,})
plt.xticks(rotation=90)
plt.plot()


# In[90]:


df_curr_month_decrease = df_pct_change.query("No_Of_Calls>10 and Date=='2021-05-31' and Pct_Change<0")
df_curr_month_decrease['Pct_Change'] = df_curr_month_decrease.Pct_Change.apply(lambda x: x*100)
df_curr_month_decrease = df_curr_month_decrease.sort_values(by='Pct_Change')
df_curr_month_decrease.head()


# In[92]:


df_consolidated_decrease = df_curr_month_decrease.merge(df_prev_month,how='inner',on='apiproxy')
df_consolidated_decrease.sort_values(by='Pct_Change_x', inplace=True)
df_consolidated_decrease.head()


# In[100]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

ax = sns.barplot(x='apiproxy', y='Pct_Change_x', data=df_consolidated_decrease.head(10),hatch='/')

for p in ax.patches:
   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()-1.5))

plt.title("% Decrease in No of Calls (from last month)",fontdict={'family': 'serif',
        'color':  'darkred',
        'weight': 'bold',
        'size': 16,})
plt.xticks(rotation=90)
plt.plot()


# In[29]:


# we can also use grouper function on date column (no need to index the Date as we do in resample function)
df_sandbox_calls["No_Of_Calls"] = 1
df_sandbox_calls_monthly = df_sandbox_calls.groupby(['apiproxy',pd.Grouper(key = 'Date', freq='M', origin='2021-01-01')])["No_Of_Calls"].sum().reset_index()


# In[141]:


df_sandbox_calls_monthly_S4HANACloudAPIs = df_sandbox_calls_monthly.query("apiproxy == 'SAPCloudforCustomer'")
df_sandbox_calls_monthly_S4HANACloudAPIs


# In[47]:


#using sidetable with 'value'
df_sandbox_calls_monthly.stb.freq(['apiproxy'],value='No_Of_Calls', style = True, thresh = 99, other_label='Rest of Proxies')


# In[45]:


df_sandbox.head(2)


# In[32]:


##using sidetable without value (just to count the no of occurence)
df_sandbox.stb.freq(['apiproxy'],style = True, thresh = 99, other_label='Rest of Proxies')


# In[143]:


plt.figure(figsize=(16,9))

fig, ax = plt.subplots(3, 3,figsize=(16, 9),constrained_layout=True)
 
# We can use the following arguments to customize the titles of the subplots:

# fontsize: The font size of the title
# loc: The location of the title (“left”, “center”, “right”)
# x, y: The (x, y) coordinates of the title
# color: The font color of the title
# fontweight: The font weight of the title
# plt.show()
sns.lineplot(ax =ax[0][0] ,x='Date', y = 'No_Of_Calls',label='S/4HANA', data=(df_sandbox_calls_monthly.query("apiproxy == 'S4HANACloudAPIs'")))
ax[0][1].ticklabel_format(useOffset=False, style='plain', axis='y')
sns.lineplot(ax =ax[0][1] ,x='Date', y = 'No_Of_Calls',label = 'SuccessFactors', data=(df_sandbox_calls_monthly.query("apiproxy == 'SuccessFactors'")))
ax[0][1].set_title('No of Calls Per Month',fontsize=18, color = 'red',fontweight='bold')
sns.lineplot(ax =ax[0][2] ,x='Date', y = 'No_Of_Calls',label = 'SAP BTP', data=(df_sandbox_calls_monthly.query("apiproxy == 'CloudPlatformIntegration'")))
sns.lineplot(ax =ax[1][0] ,x='Date', y = 'No_Of_Calls',label = 'Ariba', data=(df_sandbox_calls_monthly.query("apiproxy == 'SAPAribaOpenAPIs'")))
sns.lineplot(ax =ax[1][1] ,x='Date', y = 'No_Of_Calls',label = 'SAPCleaProductImageClassification', data=(df_sandbox_calls_monthly.query("apiproxy == 'SAPCleaProductImageClassification'")))
sns.lineplot(ax =ax[1][2] ,x='Date', y = 'No_Of_Calls',label = 'SAPOmniChannelBanking', data=(df_sandbox_calls_monthly.query("apiproxy == 'SAPOmniChannelBanking'")))
sns.lineplot(ax =ax[2][0] ,x='Date', y = 'No_Of_Calls',label = 'DataqualityMicroservices', data=(df_sandbox_calls_monthly.query("apiproxy == 'DataqualityMicroservices'")))
sns.lineplot(ax =ax[2][1],x='Date', y = 'No_Of_Calls',label = 'SAPCPServicesProductConfiguration',data=(df_sandbox_calls_monthly.query("apiproxy == 'SAPCPServicesProductConfiguration'")))

sns.lineplot(ax =ax[2][2] ,x='Date', y = 'No_Of_Calls',label = 'APIPortal', data=(df_sandbox_calls_monthly.query("apiproxy == 'APIPortal'")))
# sns.lineplot(ax =ax[1][0] ,x='Date', y = 'No_Of_Calls',label = 'SAPOmniChannelBanking', data=(df_sandbox_calls_monthly.query("apiproxy == 'SAPOmniChannelBanking'")))
# sns.lineplot(ax =ax[1][1] ,x='Date', y = 'No_Of_Calls',label = 'APIPortal', data=(df_sandbox_calls_monthly.query("apiproxy == 'APIPortal'")))
# plt.grid()
# # plt.yticks(np.arange(0,35000,1000))

# plt.legend();

plt.show();


# In[49]:


df_sandbox_calls_last_month = df_sandbox_calls_monthly.query("Date == '2021-05-31'")
df_sandbox_calls_last_month.head(2)


# In[50]:


df_sandbox_calls_last_month = df_sandbox_calls_last_month.sort_values(by='No_Of_Calls', ascending=False)
df_sandbox_calls_last_month.head()


# # Maximum No of Calls (Top 10)

# In[75]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

ax = sns.barplot(x='apiproxy', y='No_Of_Calls', data=df_sandbox_calls_last_month.head(10),hatch='/')
ax.ticklabel_format(useOffset=False, style='plain', axis='y')

for p in ax.patches:
   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+0.1))

plt.title("Maximum No of Calls (Top 10)",fontdict={'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,})
plt.xticks(rotation=90)
plt.plot();


# # Minimum no of Calls

# In[76]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

ax = sns.barplot(x='apiproxy', y='No_Of_Calls', data=df_sandbox_calls_last_month.sort_values(by='No_Of_Calls').head(10),hatch='/')

for p in ax.patches:
   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+0.1))

plt.title("Minimum No of Calls (Bottom 10)",fontdict={'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,})
plt.xticks(rotation=90)
plt.plot()


# In[154]:


import pandas as pd
#Request class is used to read the APIs and store it in dataframe
import requests
import json

response_package = requests.get("https://api.sap.com/api/1.0/containergroup/ContentTypes?$expand=containers?$format=json")
response_package


# In[156]:


response_package.json()


# In[155]:


response_package.json().keys()


# In[161]:


response_package.json()['containers'][0]['aggregation']


# In[162]:


import json
API_Aggregation = json.loads(response_package.json()['containers'][0]['aggregation'])
API_Aggregation


# In[163]:


API_Aggregation['TotalArtifacts']


# In[164]:


API_Aggregation['ArtifactType']['API']['subType']['SOAP']['count']


# In[1]:


API_Aggregation['ArtifactType']['API']['subType']['REST']['count']


# In[ ]:




