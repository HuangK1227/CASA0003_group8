#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as geopd
import pandas as pd
from shapely.geometry import Polygon,box
from os import path as osPath 


# In[2]:


rootPath = r'H:\gismap\data'
dataSaveRoot = r'H:\gismap\static'


# In[3]:


# 涂鸦点
graffitiFileName = 'Graffiti'
graffitiFilePath = osPath.join(rootPath,'{0}.csv'.format(graffitiFileName))
graffitiDataset = pd.read_csv(graffitiFilePath)

graffitiDatasetnew = graffitiDataset[graffitiDataset['Request Details'].str.contains('Building',na=False)]
coordData = graffitiDatasetnew['Point'].str.replace('(','').str.replace(')','')
coordData = coordData.str.split(',',expand=True)
print(graffitiDatasetnew.size,graffitiDataset.size)


# In[4]:


dataset_out = pd.DataFrame()
dataset_out['lon'] =coordData[1].to_list()
dataset_out['lat'] = coordData[0].to_list()
dataset_out['type'] = graffitiDatasetnew['Request Details'].to_list()
dataset_out['type'] = dataset_out['type'].str.replace('Not_Offensive','0')
dataset_out['type'] = dataset_out['type'].str.replace('Offensive','1')
splitData = dataset_out['type'].str.split('-',expand=True)
splitData[1] = splitData[1].str.replace('Post_Abatement_Inspection','3')
splitData[1] = splitData[1].str.replace('Commercial ','3')
dataset_out['type'] = splitData[1].astype(int)
print(splitData[2]=='None',splitData[1])
print(splitData[splitData[2]==None],splitData)
print(dataset_out.to_csv('test.csv'))


# In[67]:


# graffitiDataset.drop('Point',axis=1,inplace=True)
# ouput graffiti data geojson
geo_graffitiDataset = geopd.GeoDataFrame(dataset_out,geometry=geopd.points_from_xy(dataset_out.lon,dataset_out.lat,crs='EPSG:4326'),crs='EPSG:4326',)
# .box(minx, miny, maxx, maxy, ccw=True)EmEditor
extentBox = geopd.GeoSeries([box(-122.672,37.611,-122.255,37.911)],crs='EPSG:4326')

geo_graffitiDataset = geopd.clip(geo_graffitiDataset,extentBox)
print(geo_graffitiDataset)
geo_graffitiDataset.to_file(osPath.join(dataSaveRoot,'{0}.geojson'.format('points_graffiti_05')),driver='GeoJSON')


# In[5]:


# Bay region
bayAreaFileName = 'BayArea'
bayAreaFilePath = osPath.join(rootPath,'BayArea','{0}.shp'.format(bayAreaFileName))
bayAreaDataset = geopd.read_file(bayAreaFilePath)
price_dataset = pd.read_csv(osPath.join(rootPath,'2000-2020_Zipcode_housing price index_US.csv'))
# price_dataset.rename(columns={'RegionName':'zip'},inplace=True)

bayAreaDataset['zip'] = bayAreaDataset['zip'].astype(str).to_list()
price_dataset['zip'] = price_dataset['RegionName'].astype(str).to_list()
bayAreaDataset.set_index('zip',inplace=True)
price_dataset.set_index('zip',inplace=True)

dataset_join = bayAreaDataset.join(price_dataset,how='left',on ='zip',lsuffix='_l',rsuffix='_r')
# print(bayAreaDataset,price_dataset)
dataset_join = dataset_join[dataset_join['City']=='San Francisco']
dataset_join.crs = "EPSG:4326"
dataset_join.to_file(osPath.join(dataSaveRoot,'{0}_left_price_01.geojson'.format(bayAreaFileName)),driver='GeoJSON')
print(osPath.join(dataSaveRoot,'{0}_price.geojson'.format(bayAreaFileName)))


# In[88]:


price_dataset.columns = price_dataset.columns.map(lambda x: x.split('-')[0])
print(price_dataset.columns)


# In[95]:


# SF region
SFAreaFileName = 'SF'
SFAreaFilePath = osPath.join(rootPath,'SFcityArea','{0}.shp'.format(SFAreaFileName))
SFAreaDataset = geopd.read_file(SFAreaFilePath)
price_SF_dataset = pd.read_csv(osPath.join(rootPath,'housing_price_SF_2019.csv'))
# 均值
meanPrice = price_SF_dataset.groupby('Zip')['Price'].mean()/10000
# price_SF_dataset = price_SF_dataset.abs
# price_dataset.rename(columns={'RegionName':'zip'},inplace=True)
meanPriceDataset = pd.DataFrame({'zip':meanPrice.keys().to_list(),'meanPrice':meanPrice.round(decimals=2).astype(int).to_list()})

SFAreaDataset['zip'] = SFAreaDataset['zip'].astype(str).to_list()
meanPriceDataset['zip'] = meanPriceDataset['zip'].astype(str).to_list()
SFAreaDataset.set_index('zip',inplace=True)
meanPriceDataset.set_index('zip',inplace=True)
dataset_SF_join = SFAreaDataset.join(meanPriceDataset,how='left',on ='zip',lsuffix='_l',rsuffix='_r')
dataset_SF_join.rename(columns={'po_name':'City'},inplace=True)
print(SFAreaDataset,dataset_SF_join)
dataset_SF_join.crs = "EPSG:4326"
dataset_SF_join.to_file(osPath.join(r'H:\gismap\static','{0}_left_price_01.geojson'.format(SFAreaFileName)),driver='GeoJSON')
print(osPath.join(dataSaveRoot,'{0}_price.geojson'.format(SFAreaFileName)))


# In[92]:


print(meanPrice.to_list())


# In[ ]:




