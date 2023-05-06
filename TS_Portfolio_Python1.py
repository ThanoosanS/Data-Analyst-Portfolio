# Amazon Web Scraper using Python on Jupyter Notebooks

# import libraries 
import requests
from bs4 import BeautifulSoup
import time
import datetime

# Connect to Website and pull in data
URL = 'https://www.amazon.ca/Coup-Card-Game-Resistance-Universe/dp/B00GDI4HX4/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=PdHyS&content-id=amzn1.sym.51ce09d4-a5e1-4c26-916a-dd527820dcd6&pf_rd_p=51ce09d4-a5e1-4c26-916a-dd527820dcd6&pf_rd_r=XCZ6NKKV1BQHF2PETGX6&pd_rd_wg=7wKxA&pd_rd_r=f7529644-b941-49eb-93b8-4a861e151d8b&pd_rd_i=B00GDI4HX4&th=1'

# Retrieve header information from: http://httpbin.org/get
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

page = requests.get(URL, headers=headers,cookies={'_hs_opt_out':'no'}) #Turn cookies on

soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), "html.parser") #Prettify makes the html easier to read

title = (soup2.find(id ='title').get_text()).strip()
price = (soup2.find('span',{'class':"a-offscreen"}).text.strip()).strip()[1:] #Price was a bit harder so we used the class method

print(title)
print(price)

today = datetime.date.today()

import csv #for creating .csv files

header = ['Title','Price','Date']
data = [title,price,today]

with open('AmazonWebScrapData.csv','w', newline='',encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)

# Using pandas to view .csv file
import pandas as pd

df = pd.read_csv(r'C:\Users\sathi\AmazonWebScrapData.csv')

print(df)

# Append data
with open('AmazonWebScrapData.csv','a+', newline='',encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)

# Price monitoring 
def check_price():
    URL = 'https://www.amazon.ca/Coup-Card-Game-Resistance-Universe/dp/B00GDI4HX4/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=PdHyS&content-id=amzn1.sym.51ce09d4-a5e1-4c26-916a-dd527820dcd6&pf_rd_p=51ce09d4-a5e1-4c26-916a-dd527820dcd6&pf_rd_r=XCZ6NKKV1BQHF2PETGX6&pd_rd_wg=7wKxA&pd_rd_r=f7529644-b941-49eb-93b8-4a861e151d8b&pd_rd_i=B00GDI4HX4&th=1'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

    page = requests.get(URL, headers=headers,cookies={'_hs_opt_out':'no'})

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    
    title = (soup2.find(id ='title').get_text()).strip()
    price = (soup2.find('span',{'class':"a-offscreen"}).text.strip()).strip()[1:]
    
    import datetime
    
    today = datetime.date.today()
    
    import csv

    header = ['Title','Price','Date']
    data = [title,price,today]
    
    with open('AmazonWebScrapData.csv','a+', newline='',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

while(True):
    check_price()
    time.sleep(86400) #Time interval in s (24 h)
    

