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
import fnmatch as fnm
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
xpath_stat_card='//*[@class="stats-cards__container"]'
xpath_stat_card_item='//*[@class="stats-cards__item"]'


##===detect if website has updated===start
response = requests.get(url, headers={'Cache-Control': 'no-cache'})
selector = Selector(response.text)
stat_card_today=selector.xpath(xpath_stat_card).getall()[0]

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


#===load today's data===start
daily={}

daily['date'] = today_date
daily['timestamp_iso']=timestamp_iso

items1=selector.xpath(xpath_stat_card_item)
if items1 is None or len(items1)==0:
    print('crawler: no data items found')
    sys.exit(1)
# print(items1)

for item in items1:
    title=item.xpath('div[2]/text()').get()
    value=item.xpath('div[1]/text()').get()
    if title is None or value is None:
        print('crawling xpath error of title and value')
        exit(1)
    else:
        title=title.strip()
        valute=value.strip()
    # print(title)
    # print(value)
    if 'cases' in title.lower():
        daily['num_cases']=int(value.replace(',', ''))
    elif 'icu' in title.lower():
        daily['num_icu']=int(value.replace(',', ''))
    elif 'hospitalizations' in title.lower():
        daily['num_hospitalizations']=int(value.replace(',', ''))
    elif 'death' in title.lower():
        daily['num_death']=int(value.replace(',', ''))
    elif "age range" in title.lower():
        daily['age_range']=value
    elif "median age" in title.lower():
        daily['median_age']=value
    elif fnm.fnmatch(title.lower(),"sex*females"):
        daily['sex_females']=value
    elif fnm.fnmatch(title.lower(),"sex*males"):
        daily['sex_males']=value

print(daily)
##===load today's data===end


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

