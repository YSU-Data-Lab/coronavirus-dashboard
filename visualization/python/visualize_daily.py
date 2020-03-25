import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker

# fig_width=8
# fig_height=3
value_text_size=11
rotation_degree=90

data_file_name = '../../data/ohio.json'
num_cases_file_name='../../figure/num_cases.svg'
# num_counties_file_name='../../figure/num_counties.svg'
num_icu_file_name='../../figure/num_icu.svg'
num_hospitalizations_file_name='../../figure/num_hospitalizations.svg'
num_death_file_name='../../figure/num_death.svg'

with open(data_file_name, 'r') as data_file:
    data=json.load(data_file)

if data is not None:
    daily_entries=data['daily']
else:
    daily_entries=[]
    
df = pd.DataFrame(daily_entries)
df['num_new_cases']=df['num_cases'].diff() # add newly confirmed cases

x=df['date']
y=df['num_cases']
z=df['num_new_cases']
# plt.figure(figsize=(fig_width, fig_height))
plt.title('Confirmed Cases in Ohio')
plt.plot(x, y, marker='.', markersize=12, color='red', linewidth=2, label='Total Confirmed Cases')
plt.plot(x, z, marker='.', markersize=12, color='orange', linewidth=2, label='Newly Confirmed Cases')
plt.legend()
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
#plt.xlabel('Date')
plt.xticks(rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    # plt.annotate(str(j),xy=(i,j))
    plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
for i,j in zip(x[1:],z[1:]):
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_cases_file_name)
plt.clf()
plt.cla()
plt.close()



y=df['num_icu'].dropna() # delete NaN entries
x=df['date'][len(df['date'])-len(y):] # subarray of dates with num_icu available
# plt.figure(figsize=(fig_width, fig_height))
plt.title('Number of ICU admissions')
plt.plot(x, y, marker='.', markersize=12, color='tan', linewidth=2)
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
#plt.xlabel('Date')
plt.xticks(rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    # plt.annotate(str(j),xy=(i,j))
    plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_icu_file_name)
plt.clf()
plt.cla()
plt.close()


x=df['date']
y=df['num_hospitalizations']
# plt.figure(figsize=(fig_width, fig_height))
plt.title('Number of Hospitalizations in Ohio')
plt.plot(x, y, marker='.', markersize=12, color='olive', linewidth=2)
bottom, top = plt.ylim()  
plt.ylim(0, top*1.1)
plt.xticks(rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_hospitalizations_file_name)
plt.clf()
plt.cla()
plt.close()


x=df['date']
y=df['num_death']
# plt.figure(figsize=(fig_width, fig_height))
plt.plot(x, y, marker='^', color='grey', linewidth=2)
plt.title('Number of Deaths')
bottom, top = plt.ylim()  
plt.ylim(0, top*1.1)     
plt.xticks(rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_death_file_name)
plt.clf()
plt.cla()
plt.close()


# x=df['date']
# y=df['num_counties']
# # plt.figure(figsize=(fig_width, fig_height))
# plt.title('Number of Counties in Ohio')
# plt.plot(x, y, marker='.', markersize=12, color='tan', linewidth=2)
# bottom, top = plt.ylim()
# plt.ylim(0, top*1.1)
# #plt.xlabel('Date')
# plt.xticks(rotation=rotation_degree)
# plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
# for i,j in zip(x,y):
#     # plt.annotate(str(j),xy=(i,j))
#     plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
# plt.tight_layout()
# plt.savefig(num_counties_file_name)
# plt.clf()
# plt.cla()
# plt.close()