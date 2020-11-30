"""
crawler csv summary daily
url: https://coronavirus.ohio.gov/static/COVIDSummaryData.csv
"""

import requests
# from parsel import Selector
import datetime as dt
import time
import sys
import os
import json
import pandas as pd
# import fnmatch as fnm
# from lxml import html
import addfips
import util.basic as basic
import filecmp

url='https://coronavirus.ohio.gov/static/COVIDSummaryData.csv'
csv_summary_dir='data/csv_summary/'
csv_county_summary_dir='data/csv_county_summary/'

today_date=basic.get_today_date()
yesterday_date=basic.get_yesterday_date()

csv_summary_file_name_today=csv_summary_dir+'COVIDSummaryData_'+today_date+'.csv'
csv_summary_file_name_yesterday=csv_summary_dir+'COVIDSummaryData_'+yesterday_date+'.csv'
csv_summary_file_name_today_tmp=csv_summary_dir+'COVIDSummaryData_'+today_date+'_tmp.csv'
# print(csv_summary_file_name_yesterday)
# print(csv_summary_file_name_today)

csv_county_summary_file_name_today=csv_county_summary_dir+'csv_county_summary_'+today_date+'.csv'

##===detect if website update===

csv_summary_today_tmp=requests.get(url, allow_redirects=True).content
if "<html lang=\"en\">" in str(csv_summary_today_tmp):
    print('URL of CSV today not available')
    sys.exit(1)

open(csv_summary_file_name_today_tmp, 'wb').write(csv_summary_today_tmp)

if os.path.exists(csv_summary_file_name_yesterday):
    with open(csv_summary_file_name_yesterday,'r') as csv_summary_file_yesterday:
        csv_summary_yesterday=csv_summary_file_yesterday.read()
    if filecmp.cmp(csv_summary_file_name_today_tmp,csv_summary_file_name_yesterday):
        print('Website not updated: ',url)
        os.remove(csv_summary_file_name_today_tmp)
        sys.exit(1)
    else:
        print('Begin crawling')

##===process today's csv summary data===
csv_summary_today=csv_summary_today_tmp
if os.path.exists(csv_summary_file_name_today_tmp):
    os.rename(csv_summary_file_name_today_tmp, csv_summary_file_name_today)
    print('Save today\'s csv summary data: ', csv_summary_file_name_today)

df = pd.read_csv(csv_summary_file_name_today)[:-1]
df['Case Count']=df['Case Count'].astype('int64')
df['Death Count']=df['Death Count'].astype('int64')
df['Hospitalized Count']=df['Hospitalized Count'].astype('int64')

df2=df.groupby('County', as_index=True)[['Case Count', 'Death Count', 'Hospitalized Count']].sum().reset_index()
af=addfips.AddFIPS()
df2['fips']=df2['County'].apply(lambda x: af.get_county_fips(x, 'OH'))

df2.to_csv(csv_county_summary_file_name_today, index=None, header=True)
print('Save today\'s csv county summary data: ', csv_county_summary_file_name_today)
