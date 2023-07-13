#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Web scraper for wikipedia table
#import libraries
from bs4 import BeautifulSoup
import requests 


# In[4]:


#connect to wikipedia page
url='https://en.wikipedia.org/wiki/List_of_largest_companies_in_Canada'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


# In[12]:


#second table (Forbes Global 2000 for the year 2019)
table=soup.find_all('table')[1] 
table


# In[21]:


#get the headers for the second table
tableheading=table.find_all('th') 
tablehead = [title.text.strip() for title in tableheading] #iterate
tablehead


# In[22]:


import pandas as pd


# In[23]:


#create dataframe df
df=pd.DataFrame(columns=tablehead)


# In[26]:


column_data=table.find_all('tr')[1:] #cutoff headers so start at 1:


# In[34]:


#iterate through each row of data
for row in column_data:
    row_data=row.find_all('td')
    ind_row_data=[data.text.strip() for data in row_data]
    
    #append each row
    length=len(df)
    df.loc[length] = ind_row_data
    
df


# In[36]:


df.to_csv(r'',index=False) #enter file location

