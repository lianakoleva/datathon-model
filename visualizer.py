#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 05:53:32 2020

@author: lputnam
source referenced: https://www.datacamp.com/community/tutorials/geospatial-data-python
"""

# Load all importance packages
import geopandas as gp
import numpy as np
import pandas as pd
import fiona as fi
from shapely.geometry import Point, Polygon
import missingno as msn
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import os
import time
from selenium import webdriver


#importing files to dataframes
country = gp.read_file('ExternalData/gz_2010_us_040_00_20m/gz_2010_us_040_00_20m')
points = pd.read_csv('GivenData/Master.csv')
zc = pd.read_csv('GivenData/zip_code_database.csv')

#cleaning zc
zc = zc.drop(['type', 'decommissioned', 'primary_city', 'acceptable_cities', 
              'state', 'county', 'timezone', 'area_codes', 'world_region',
              'country', 'irs_estimated_population_2015', 
              'unacceptable_cities'], axis=1)
zc = zc.rename(columns={"zip" : "GEO.id"})

#cleaning points
points = points.drop(['GEO.display-label', 'NAICS.id', 'NAICS.display-label', 
                      'REVENUE (k)', 'ESTAB', 'INCOME.aggregate'], axis=1)
points['GEO.id'] = points['GEO.id'].str.slice(start=9, stop=14).astype(int)
points = points.rename(columns={"MS.percent" : "MSpercent"})

points = pd.merge(left=points, right=zc, how='left', on='GEO.id') #merging

points['coordinates'] = points[['longitude', 'latitude']].values.tolist()
points['coordinates'] = points['coordinates'].apply(Point)

usa = gp.read_file('zip://'+'/home/lputnam/Downloads/tl_2019_us_zcta510.zip')# Set datum and projection info for census.gov 2015 Tiger 
usa.crs = {'datum': 'NAD83', 'ellps': 'GRS80', 'proj':'longlat', 'no_defs':True}
map = folium.Map(location=[42.5, -76], zoom_start=7, tiles='cartodbpositron' )
map

points = gp.GeoDataFrame(points, geometry='coordinates')
max_amount = float(points['MSpercent'].max())
hmap = folium.Map(location=[42.5, -75.5], zoom_start=7, )
hm_wide = HeatMap( list(zip(points.latitude.values, points.longitude.values, points.MSpercent.values)),
                   min_opacity=0.15,
                   max_val=max_amount,
                   radius=17, blur=15, 
                   max_zoom=1, 
                 )

hmap.add_child(hm_wide)
hmap.save(os.path.join('GivenData', 'heatmap.html'))


#fig, ax = plt.subplots(1, figsize=(30,10))
#
#points.plot(ax=base, color='darkred', marker="*", markersize=10);