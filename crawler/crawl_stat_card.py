import requests
from parsel import Selector
from datetime import date
import json
import time
import os, sys

today_date = date.today().strftime("%Y-%m-%d")

stat_card_dir='../data/stat_card/'
stat_card_file_name=stat_card_dir+today_date+'.html'

if os.path.exists(stat_card_file_name):
    print('Crawling for today finished previously. Exit.')
    sys.exit(1)

response = requests.get('https://coronavirus.ohio.gov/wps/portal/gov/covid-19/')
selector = Selector(response.text)
stat_card=selector.xpath('//*[@id="odx-main-content"]/article/section[2]/div').getall()[0]

# print(stat_card)

with open(stat_card_file_name, 'w+') as stat_card_file:
	stat_card_file.write(stat_card)
	
