import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker




data_file_name = '../../data/ohio.json'
num_cases_file_name='../../figure/num_cases.svg'
num_new_cases_file_name='../../figure/num_new_cases.svg'
num_new_avg_7d_cases_file_name='../../figure/num_new_avg_7d_cases.svg' # number of average new cases in previous 7 days
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


# plot parameters
num_days=len(df['date'])
fig_height=8
fig_width=int(10*num_days/141) #lenght=15 and num_days=141 (08/10/20)
value_text_size=5
x_text_size=5
rotation_degree=90
marker_size=5
line_width=0.5
label_size=5

## num of total cases
x=df['date']
y=df['num_cases']
plt.figure(figsize=(fig_width, fig_height))
plt.title('Confirmed Cases in Ohio')
plt.plot(x, y, marker='.', markersize=marker_size, color='red', linewidth=line_width, label='Total Confirmed Cases')
# plt.legend()
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
#plt.xlabel('Date')
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
#plt.tick_params(axis='x', which='major', labelsize=label_size)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    # plt.annotate(str(j),xy=(i,j))
    #plt.text(i, j, str(j), size=value_text_size, ha='center', va='bottom')
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
    #plt.text(i, j, str(j), ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_cases_file_name)
plt.clf()
plt.cla()
plt.close()

## num of new cases
df['num_new_cases']=df['num_cases'].diff() # add newly confirmed cases
x=df['date']
z=df['num_new_cases']
plt.figure(figsize=(fig_width, fig_height))
plt.title('Newly Confirmed Cases in Ohio')
plt.plot(x, z, marker='.', markersize=marker_size, color='orange', linewidth=line_width, label='Newly Confirmed Cases')
# plt.legend()
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x[1:],z[1:]):
    #plt.text(i, j, str(int(j)), ha='center', va='bottom')
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_new_cases_file_name)
plt.clf()
plt.cla()
plt.close()

# number of average new cases in previous 7 days
df['num_new_avg_7d_cases']=df['num_cases'].diff(7)/7 # add newly confirmed cases
x=df['date']
z=df['num_new_avg_7d_cases']
plt.figure(figsize=(fig_width, fig_height))
plt.title('7-Day Average Newly Confirmed Cases in Ohio')
plt.plot(x, z, marker='.', markersize=marker_size, color='gold', linewidth=line_width, label='Avg Daily New in Last 7 Days')
# plt.legend()
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x[8:],z[8:]):
    #plt.text(i, j, str(int(j)), ha='center', va='bottom')
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_new_avg_7d_cases_file_name)
plt.clf()
plt.cla()
plt.close()

## num of total icu counts
y=df['num_icu'].dropna() # delete NaN entries
x=df['date'][len(df['date'])-len(y):] # subarray of dates with num_icu available
plt.figure(figsize=(fig_width, fig_height))
plt.title('Number of ICU admissions')
plt.plot(x, y, marker='.', markersize=marker_size, color='tan', linewidth=line_width)
bottom, top = plt.ylim()
plt.ylim(0, top*1.1)
#plt.xlabel('Date')
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    # plt.annotate(str(j),xy=(i,j))
    #plt.text(i, j, str(int(j)), ha='center', va='bottom')
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_icu_file_name)
plt.clf()
plt.cla()
plt.close()


x=df['date']
y=df['num_hospitalizations']
plt.figure(figsize=(fig_width, fig_height))
plt.title('Number of Hospitalizations in Ohio')
plt.plot(x, y, marker='.', markersize=marker_size, color='olive', linewidth=line_width)
bottom, top = plt.ylim()  
plt.ylim(0, top*1.1)
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    #plt.text(i, j, str(j), ha='center', va='bottom')
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_hospitalizations_file_name)
plt.clf()
plt.cla()
plt.close()


x=df['date']
y=df['num_death']
plt.figure(figsize=(fig_width, fig_height))
plt.plot(x, y, marker='^', markersize=marker_size, color='grey', linewidth=line_width)
plt.title('Number of Deaths')
bottom, top = plt.ylim()  
plt.ylim(0, top*1.1)     
plt.xticks(fontsize=x_text_size, rotation=rotation_degree)
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
for i,j in zip(x,y):
    #plt.text(i, j, str(j), ha='center', va='bottom')
    if np.isnan(j):
        j=np.nan_to_num(j)
    plt.text(i, j, str(int(j)), size=value_text_size, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(num_death_file_name)
plt.clf()
plt.cla()
plt.close()



