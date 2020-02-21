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

parser = argparse.ArgumentParser()
parser.add_argument('filename', type = str, help="File name is :" )
args=parser.parse_args()
filename = args.filename


print(filename)
df_pop = pd.read_csv('data/'+filename)
df_pop['etl_ymd2'] = df_pop['etl_ymd'].apply(str)
#날짜datetime 형식으로 변경하는 함수 생성
fconvert = lambda x : datetime.datetime.strptime(x, "%Y%m%d").date()
#날짜를 datetime 형식으로 변경
df_pop['etl_ymd2'] = df_pop['etl_ymd2'].apply(fconvert)

#날짜를 요일로 변경하는 함수(월요일:0 화요일:1 ~ 일요일:6)
fweekday = lambda x : datetime.datetime.weekday(x)
#날짜를 요일로 변경
df_pop['weekday'] = df_pop['etl_ymd2'].apply(fweekday)

print('save')    

df_pop.to_csv('data_3/'+filename) 