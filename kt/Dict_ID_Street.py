## Street - ID mapping code

import os

# for data aggregation.
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy.distance import distance, lonlat

import warnings
warnings.filterwarnings('ignore')

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from shapely.geometry import Polygon, LineString, Point
from shapely.ops import nearest_points
import pyproj
from pyproj import Transformer

from tqdm import tqdm, trange
from time import sleep

import json
'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath")
args = parser.parse_args()
filepath=args.filepath

'''




# Function
def read(filename):
    df_=pd.read_csv(filename,index_col=0 )
    if df_['WGS_lon'][0] < 100:
        df_ = df_.rename(columns={'WGS_lat': 'WGS_lon', 'WGS_lon': 'WGS_lat'})
    if sum(df_.columns.isin(['Unnamed: 0.1']))==1:
        df_=df_.drop(['Unnamed: 0.1'],axis=1)
    return (df_)





## Street information

#Coordinate information
#crs=pycrs.load.from_file("GRS80_UTMK.prj").to_proj4()
crs='+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +units=m +no_defs'
transproj_eq = Transformer.from_proj(
    crs,
    'EPSG:4326',
    always_xy=True,
    skip_equivalent=True)

transproj_eq

street_file = "./data/street/TL_SPRD_MANAGE.shp"
street = gpd.read_file(street_file, encoding='euckr')
#street[['RN','RN_CD','geometry']]    

def line_to_coordinates(x):
    L=x.coords[:]
    lat=[]
    lon=[]
    for i in range(len(L)):
        lat.append(L[i][1])
        lon.append(L[i][0])
    return [(x,y) for x,y in zip(lon,lat)]

street['coordinates'] = np.nan
street['coordinates'] = street['geometry'].apply(line_to_coordinates) 
street_0= gpd.GeoDataFrame(street[['RN','RN_CD','coordinates']] )

WGS_street_list=[]

for i in range(len(street_0)):
    WGS_list=[]
    for pt in transproj_eq.itransform(street_0['coordinates'][i]):
        WGS=('{:.10f} {:.10f}'.format(*pt).split(' '))
        WGS_list.append((float(WGS[0]),float(WGS[1])))
    WGS_street_list.append(WGS_list)

geo_total=[]
for i in range(len(WGS_street_list)):
    geo=gpd.GeoDataFrame(index=[0], crs={'init': 'epsg:4326'}, geometry=[LineString(WGS_street_list[i])])
    geo_total.append([street_0['RN'][i],street_0['RN_CD'][i],geo['geometry']])

street_line=gpd.GeoDataFrame(geo_total)
street_line.columns=['RN','RN_CD','geometry']

filepath = './data/id_wgs_set.csv'

df=pd.read_csv(filepath,index_col=0)
id_set = list(set(df['id']))


print('making a wgs_set which is [id, WGS_lon, WGS_lat]')
wgs_set=[]
for i in tqdm(id_set):
    wgs_set.append([i, df[df.id==i].iloc[0]['WGS_lon'],df[df.id==i].iloc[0]['WGS_lat']])
wgs_set=pd.DataFrame(wgs_set)
wgs_set.columns = ['id','WGS_lon', 'WGS_lat']


id_info=gpd.GeoDataFrame(wgs_set, geometry=gpd.points_from_xy(wgs_set.WGS_lon, wgs_set.WGS_lat))
#print(nearest_points(street_line.geometry[0][0],gdf_time_0_1.geometry[0])[0])
print('making a RN_CD_set which is [RN_CD]')
RN_CD_list=[]
id_list =[]
for j in tqdm(range(len(id_info))):
    p = id_info.geometry[j]
    id_list.append(int(id_info.id[j]))
    p_dist=[]
    for i in range(len(street_line)):
        line = street_line.geometry[i][0]
        p_dist.append([street_line.RN_CD[i],p.distance(line)])    
    a=pd.DataFrame(p_dist)
    a.columns=['RN_CD','dist']
    RNs=str(a[a.dist.isin([min(a['dist'])])]['RN_CD'].to_list()[0])
    RN_CD_list.append(RNs)
    

dict_id_street=dict(zip(id_list,RN_CD_list))


#json 파일로 저장
with open('dict/dict_id_street.json', 'w', encoding='utf-8') as make_file:
    json.dump(dict_id_street, make_file, indent="\t")
