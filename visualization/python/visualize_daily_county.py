from bokeh.io import output_file, show, save
from bokeh.models import *
from bokeh.palettes import *
from bokeh.plotting import *
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as us_counties
from bokeh.resources import CDN
from jinja2 import Template
from bokeh.embed import *
import numpy as np
import pandas as pd
import util.basic as basic
import re
import os

today_date=basic.get_today_date()
csv_file_name='data/csv_county_summary/csv_county_summary_'+today_date+'.csv'
index_file_name='index.html'

if os.path.exists(csv_file_name):
	df=pd.read_csv(csv_file_name)
else:
	print('csv file not exists: '+csv_file_name)
	exit(1)


counties = {
    code: county for code, county in us_counties.items() if county["state"] == "oh"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]


county_names = [county['name'] for county in counties.values()]
# county_rates = [unemployment[county_id] for county_id in counties]
county_counts = []
for index, county_name in enumerate(county_names):
    county_count = df.loc[df['County']==county_name]['Case Count'].values
    if len(county_count)==0:
        county_counts.append(0)
    else:
        county_counts.append(county_count[0])


palette=all_palettes['Inferno'][256]+('#ffffff',)
palette = tuple(reversed(palette))
color_mapper = LinearColorMapper(palette=palette, low=0, high=500)

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    count=county_counts,
)

# TOOLS = "pan,wheel_zoom,reset,hover,save"
TOOLS = "hover,save"

p = figure(
    title="Confirmed Cases in Counties of Ohio", 
    tools=TOOLS,
    x_axis_location=None, 
    y_axis_location=None,
    plot_width=600,
    #sizing_mode='stretch_both',
    match_aspect=True,
    tooltips=[
        ("Name", "@name"), 
        ("Num of Cases", "@count"), 
        #("(Long, Lat)", "($x, $y)")
    ])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 
          'y', 
          source=data,
          fill_color={
              'field': 'count', 
              'transform': color_mapper
          },
          fill_alpha=0.7, 
          line_color="black", 
          #line_width=0.5
         )

script, div = components(p)

div=re.sub(r'<div',r'<div align="center"', div)

bokeh_string = script + '\n'+ div
bokeh_js_string = r'''\n
<script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-2.0.0.min.js"></script>
\n
'''


with open(index_file_name, 'r') as f:
    text = f.read()


str_insert=bokeh_js_string + bokeh_string

text = re.sub(r'<!-- bokeh_block_start -->.*<!-- bokeh_block_end -->','<!-- bokeh_block_start -->\n'+str_insert+r'\n<!-- bokeh_block_end -->', text, flags=re.DOTALL)

with open(index_file_name, 'w') as f:
    f.write(text)