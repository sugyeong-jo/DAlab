import plotly
import os
import argparse

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

import geopandas as gpd
import deckgljupyter.Layer as deckgl
#from geoband.API import *

#GetCompasData('../data/PJT001_h_100m_cell_flow.geojson')
from shapely.geometry import Polygon
import geopandas as gpd
import pyproj
from pyproj import Transformer

import matplotlib as mpl
import matplotlib.pylab as plt
import datetime

id_wgs_set=pd.read_csv('data/id_wgs_set.csv',index_col=0)
print('id_swg_set')
id_point=gpd.GeoDataFrame(id_wgs_set, geometry=gpd.points_from_xy(id_wgs_set.WGS_lon, id_wgs_set.WGS_lat))
df_=pd.read_csv('data_3/ULSAN_NG_2018_raw.csv',index_col=0)

print('df_')
df_=pd.merge(df_[['id', 'timezn_cd', 'total', 'admi_cd','etl_ymd','weekday']], id_point[['id','WGS_lat','WGS_lon','geometry']], on ='id', how = 'left') 
print(df_)
#df_.to_csv('data/df_fin2.csv') 

#df_=pd.read_csv('data/df_fin2.csv',index_col=0)
gpd.GeoDataFrame(df_, geometry=df_.geometry).to_file('data/df_fin2.jeoson')
