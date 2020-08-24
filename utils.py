
#Dependancies 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import urllib
#geoplot
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs,init_notebook_mode,plot, iplot
from datetime import date,datetime, timedelta
from pandas.io.html import read_html



def load_data(url):
    '''
    Get data from url and save to local disk for further analysis
    Data saved in 'data/covid' created if it does not exist.
    '''
    file_path = os.path.join('data','covid')
    os.makedirs(file_path, exist_ok=True)
    csv_path = os.path.join(file_path, 'WHO-COVID-19-global-data.csv')
    urllib.request.urlretrieve(url, csv_path)
    return pd.read_csv(csv_path)

def remove_white_spaces(df):
    '''
    removes trailing white spaces in columns names to make it easier to use 
    '''
    df.columns = [col.strip() for col in df.columns]

def feature_engineer_dates(df, date_col):
    '''
     We might find it useful to analyse monthly/yearly stats
    So let's format the date feature to allow for this
    '''
    df[date_col] = pd.to_datetime(df[date_col])
    df['month'] = df[date_col].apply(lambda date:date.month)
    df['year'] = df[date_col].apply(lambda date:date.year)
    

def rename_country(df,current_country_name, new_country_name ):
    '''
    Some reports have different country names for example keeping names in a foreign language
    like 'Cote d'Ivoire' or abrreviations like Congo DR et.
    So there is a need to rename them, 
    especially when we are using more that one data sets with country manes
    '''
    df['Country'].replace(to_replace =current_country_name, 
                value =new_country_name, inplace=True)



def select_latest_data(df):
    datetime.today().utcnow().strftime('%d-%m-%Y')
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    return df[(df.Date_reported == yesterday)]

def visualize_on_map(df, scope,file_name):
    '''
    Data visualisation in maps using choromap. Scope denote the part of the maps to display
    In case we are only interested in 'Africa'
    The interactive output html file is save in a folder/filename as specified 
    '''
    data = dict(
        type = 'choropleth',
        colorscale = 'Viridis',
        reversescale = True,
        locations = df['Country'],
        locationmode = "country names",
        z =  df['Cumulative_cases'],
        text = 'Total Cases ',
        colorbar = {'title' : 'Total Cases'}
      ) 

    layout = dict(
    title = 'Total Cases Africa',
    width = 900,
    height =  800,
    geo = dict(
        showframe = False,
        projection = {'type':'mercator'},
        scope = scope
        )
    ) 

    choromap = go.Figure(data = [data],layout = layout)
    plot(choromap,validate=False, filename='images/' + file_name) 

def sort_by_stats(df, stats, asc):
    #sorting countries
    return df.sort_values(by=[stats], ascending=asc)


def read_wikipedia_table(wikipage):
    '''
    read tables from wikipedia. if no table found, return erro. else, return first table.
    this in case the page expands over time 
    '''
    tables = read_html(wikipage,  attrs={"class":"wikitable"})
    if(len(tables)>=1):
        return tables[0]
    else:
        return 'no table found'

def visualize_with_plot(title, data, x_axis, y_axis, xlabel, ylabel):
    '''
    seaborn plot, given data and display parameters
    '''
    image_path = 'images/'
    filename= os.path.join(image_path, title.lower() + '.png')
    plt.figure(figsize=(15,8))
    peak = sns.lineplot(x=x_axis,
                        y=y_axis, 
                        hue="Country",
                        data=data)
    peak.set(xlabel=xlabel, ylabel=ylabel)
    peak.set_title(title)
    plt.savefig(filename, bbox_inches="tight")