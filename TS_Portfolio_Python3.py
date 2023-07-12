#Automated Crypto Website API
# From CoinMarketCap API Documentation

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '9f4ff0ec-0b31-4ce8-8513-b16b5fed6594',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

# If it does not load do to data rate limit:
# Anaconda Prompt: jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10

import pandas as pd
global df
pd.set_option('display.max_columns',None)
df = pd.json_normalize(data['data'])

#Add a timestamp column
df['timestamp'] = pd.to_datetime('now')
df 

#Created function
def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '9f4ff0ec-0b31-4ce8-8513-b16b5fed6594',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    import pandas as pd

    pd.set_option('display.max_columns',None)
    df = pd.json_normalize(data['data'])

    #Add a timestamp column
    df['timestamp'] = pd.to_datetime('now')
    
    #Export into .csv file
    if not os.path.isfile(r'C:\Users\sathi\OneDrive\Desktop\Portfolio\Python\TS_Portfolio_Python3API.csv'):
        df.to_csv(r'C:\Users\sathi\OneDrive\Desktop\Portfolio\Python\TS_Portfolio_Python3API.csv',header='column_names')
    else: #Append df if the .csv already exists
        df.to_csv(r'C:\Users\sathi\OneDrive\Desktop\Portfolio\Python\TS_Portfolio_Python3API.csv',mode='a',header=False)

#Imports needed for time series (intervals)
import os
from time import time
from time import sleep

for i in range(333): #333 times a day allowed (from API)
    api_runner()
    print('API Runner completed sucessfully:',i,'/333')
    sleep(60) #run every minute 
exit

#Read the .csv file created earlier
df_Trial = pd.read_csv(r'C:\Users\sathi\OneDrive\Desktop\Portfolio\Python\TS_Portfolio_Python3API.csv')
df_Trial

#removes scientific notation (optional)
pd.set_option('display.float_format', lambda x: '%.5f' % x) 

#Group by cryptocurrency
df3 = df.groupby('name',sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d']].mean()
df3 

#Similar to a pivot table (Excel)
df4=df3.stack() 
df4

#convert to a dataframe from a series
df5=df4.to_frame(name='values') 
df5
df5.count()

#Add index based on count function from previous line of code 
ind = pd.Index(range(60))
df6 = df5.reset_index()
df6

#Rename column
df7 = df6.rename(columns={'level_1':'Percent_change'})
df7

#Change the parameter names on table
df7['Percent_change'] = df7['Percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df7

#Visualization
import seaborn as sns
import matplotlib.pyplot as plt
sns.catplot(x='Percent_change',y='values',hue='name',data=df7,kind='point')

#Get the price of bitcoin vs. timestamp
dfprice=df[['name','quote.USD.price','timestamp']]
dfquery = dfprice.query("name == 'Bitcoin'")
dfquery

#Price of bitcoin over automated time
sns.set_theme(style="darkgrid")
sns.lineplot(x='timestamp',y='quote.USD.price',data=dfquery)

