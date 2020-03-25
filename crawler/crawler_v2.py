"""
crawler version 2: match strings to get values
"""

import requests
from parsel import Selector
import datetime as dt
import json
import time
import sys
import os
import pandas as pd
from lxml import html

# start = time.time()

url='https://coronavirus.ohio.gov/wps/portal/gov/covid-19/'

today_date = dt.date.today().strftime("%Y-%m-%d")
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday_date = yesterday.strftime("%Y-%m-%d")
timestamp_utc=str(dt.datetime.utcnow())
timestamp_iso=str(dt.datetime.now(dt.timezone.utc).astimezone().isoformat())

stat_card_dir='../data/stat_card/'
stat_card_file_name_today=stat_card_dir+today_date+'.html'
stat_card_file_name_yesterday=stat_card_dir+yesterday_date+'.html'

data_file_name = '../data/ohio.json'
csv_file_name = '../data/ohio.csv'


##===detect if website has updated===start
response = requests.get(url)
selector = Selector(response.text)
stat_card_today=selector.xpath('//*[@id="odx-main-content"]/article/section[2]/div').getall()[0]

# if os.path.exists(stat_card_file_name_today):
#     print('Crawling for today finished previously. Exit.')
#     sys.exit(1)

if os.path.exists(stat_card_file_name_yesterday):
    with open(stat_card_file_name_yesterday,'r') as stat_card_file_yesterday:
        stat_card_yesterday=stat_card_file_yesterday.read()
    if stat_card_today == stat_card_yesterday:
        print('Website not updated: ',url)
        sys.exit(1)
    else:
        print('Begin crawling')

print('Save today\'s stat_card: ',today_date+'.html')
with open(stat_card_file_name_today, 'w+') as stat_card_file_today:
    stat_card_file_today.write(stat_card_today)
##===detect if website has updated===end


##===load today's data===start
daily={}

daily['date'] = today_date
daily['timestamp_iso']=timestamp_iso

items1=selector.xpath('//*[@id="odx-main-content"]/article/section[2]/div/div[1]/div')
if items1 is None or len(items1)==0:
    print('crawler: no data items found')
    sys.exit(1)
# print(items1)

for item in items1:
    title=item.xpath('div[2]/text()').get().strip()
    value=int(item.xpath('div/div/text()').get().strip())
    # print(title+': ', value)
    if 'cases' in title.lower():
        num_cases=value
        daily['num_cases']=num_cases
    elif 'icu' in title.lower():
        num_icu=value
        daily['num_icu']=num_icu
    elif 'hospitalizations' in title.lower():
        num_hospitalizations=value
        daily['num_hospitalizations']=num_hospitalizations
    elif 'death' in title.lower():
        num_death=value
        daily['num_death']=num_death

county_cases=selector.xpath('//*[@id="odx-main-content"]/article/section[2]/div/div[4]/div/div/div/div[1]/div/p').getall()
if county_cases is not None and len(county_cases)>0:
    county_cases=county_cases[0]
    county_cases=county_cases.replace('<p dir="ltr">*','')
    county_cases=county_cases.replace('</p>','')
    daily['county_cases']=county_cases.strip()

county_death=selector.xpath('//*[@id="odx-main-content"]/article/section[2]/div/div[4]/div/div/div/div[2]/div/p').getall()
if county_death is not None and len(county_death)>0:
    county_death=county_death[0]
    county_death=county_death.replace('<p dir="ltr">**','')
    county_death=county_death.replace('</p>','')
    daily['county_death']=county_death.strip()

print(daily)
# ##===load today's data===end


##===add today's data to daily entries===start
with open(data_file_name, 'r') as data_file:
    data=json.load(data_file)

if data is not None:
    daily_entries=data['daily']
    daily_entries_new=[]
    for d in daily_entries:
        if d['date'].lower()!=today_date.lower():
            daily_entries_new.append(d)
    daily_entries=daily_entries_new
else:
    daily_entries=[]

daily_entries.append(daily)
data['daily']=daily_entries
##===add today's data to daily entries===end

##===dump to json file===
with open(data_file_name, 'w') as data_file:
    json.dump(data, data_file, indent=4)
print('data dumped in json file:',data_file_name)

##===dump to csv file===
with open(csv_file_name, 'w+') as csv_file:
    df = pd.DataFrame(daily_entries)
    df.to_csv (csv_file_name, index = None, header=True)
print('data dumped in csv file:', csv_file_name)

