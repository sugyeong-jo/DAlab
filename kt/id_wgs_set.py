#ID-WGS set 

import plotly
import os

# for data aggregation.
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy.distance import distance, lonlat

# for data visualisation.
#import plotly_express as px
import plotly.plotly as py
import cufflinks as cf 
cf.go_offline(connected=True)
cf.set_config_file(theme='polar')
import deckgljupyter.Layer as deckgl

import warnings
warnings.filterwarnings('ignore')

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from tqdm import tqdm_notebook
plotly.__version__

import deckgljupyter.Layer as deckgl
#from geoband.API import *

#GetCompasData('../data/PJT001_h_100m_cell_flow.geojson')
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import nearest_points
import pyproj
from pyproj import Transformer

import matplotlib as mpl
import matplotlib.pylab as plt
import datetime

import pycrs 
import geoplot as gplt
import geoplot.crs as gcrs

from tqdm import tqdm, trange
from time import sleep


filepath = './data/ULSAN_NG_2018.csv'
df_=pd.read_csv(filepath,index_col=0)


id_set=list(set(df_.id))

id_wgs=[] #it takes 1h 30m
for i in tqdm(id_set):
    id_wgs.append([i,df_[df_.id==i]['x'].iloc[0],df_[df_.id==i]['y'].iloc[0]])
    
df_pop= pd.DataFrame(id_wgs)
df_pop.columns=['id','x','y']

transproj_eq = Transformer.from_proj(
    '+proj=tmerc     +lat_0=38     +lon_0=128     +k=0.9999     +x_0=400000     +y_0=600000     +ellps=bessel     +towgs84=-115.8,474.99,674.11,1.16,-2.31,-1.63,6.43 +units=m +no_defs',
    'EPSG:4326',
    always_xy=True,
    skip_equivalent=True)

coor_array=np.array(df_pop[['x','y']])
coor=[]
for i in range(len(df_pop)):
    coor.append((coor_array[i][0],coor_array[i][1]))
WGS_list=[]
for pt in transproj_eq.itransform(coor):
    WGS=('{:.10f} {:.10f}'.format(*pt).split(' '))
    WGS_list.append((float(WGS[0]),float(WGS[1])))


WGS_lat=[]
WGS_lon=[]

for i in WGS_list: 
    WGS_lon.append(i[0])
    WGS_lat.append(i[1])
# Data frame에 한번에 연결시켜주기
df_pop['WGS_lat']=np.nan
df_pop['WGS_lon']=np.nan

for i in range(len(df_pop)):
    df_pop['WGS_lon'][i]=WGS_lon[i]
    df_pop['WGS_lat'][i]=WGS_lat[i]

    
df_pop.to_csv('data/id_wgs_set.csv')