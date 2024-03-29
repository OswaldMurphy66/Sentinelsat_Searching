# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:43:57 2021

@author: oswald
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:46:23 2020

@author: oswald
"""
## Remaning to do :
                                                                               # connect to the API
from sentinelsat import SentinelAPI
from datetime import date
import matplotlib.pyplot as plt
from shapely import wkt
import math
import numpy as np
from collections.abc import Iterable 
import requests
from io import BytesIO
from PIL import Image
import geopandas
import contextily as ctx

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)
  
def getImageCluster(lat_deg, lon_deg, delta_lat,  delta_long, zoom):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmin, ymax =deg2num(lat_deg, lon_deg, zoom)
    xmax, ymin =deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)
    
    Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            try:
                imgurl=smurl.format(zoom, xtile, ytile)
                print("Opening: " + imgurl)
                imgstr = requests.get(imgurl, headers=headers)
                tile = Image.open(BytesIO(imgstr.content))
                Cluster.paste(tile, box=((xtile-xmin)*256 ,  (ytile-ymin)*255))
            except: 
                print("Couldn't download image")
                tile = None

    return Cluster

username='oswald'
key='Hjs19970709'
                                                                               # search by polygon, time, and SciHub query keywords
Date=('NOW-30DAYS', 'NOW')
area='POINT (103.5 30.8)'   
lat=19
lon=49
   
api = SentinelAPI(username, key, 'https://scihub.copernicus.eu/dhus')
                                                                                   # search by polygon, time, and SciHub query keywords
date=Date
area=area                                                                      #lon lat https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
result=api.query(date=date, area=area,producttype='SLC')                       # form 'result' as a dictionary containing meta data of the images found in that certain place

dates=[]
orbits=[]
slicenumber=[]
y_Ticks=[]
for key in result:
    print('relativeorbitnumber',result[key]['relativeorbitnumber'])
    orbits.append(result[key]['relativeorbitnumber'])                          # recording relative orbit number in an array
    dates.append(result[key]['beginposition'])                                 # recording beginposition orbit number in an array
    slicenumber.append(result[key]['slicenumber'])

orbits_unique=list(set(orbits))                                                # get unique orbits in list
slicenumber_unique=list(set(slicenumber))                                      # get unique slicenumbers in list

colors=['r','g','b','k','c','y','m']                                           # creating an array for applying different colors

fig, (ax1, ax2) = plt.subplots(2,1)                                            # form 2 separate plots 
plt.subplots_adjust(hspace=0.6)                                                # adjusting space between subplots


for i in range(0,len(orbits)):
    for n in range(0,len(orbits_unique)):

        if orbits_unique[n]==orbits[i]:
            id_spot=slicenumber_unique.index(slicenumber[i])
            y_tick=n-(id_spot+1)/(len(slicenumber_unique)+1)
            ax1.plot(dates[i],n-(id_spot+1)/(len(slicenumber_unique)+1),'o'+colors[n])
            ax1.plot(dates[i],n,'o'+colors[n])
            y_Ticks.append(y_tick)
         
   

ax1.set_yticks(range(0,n+1))
ax1.set_yticklabels(orbits_unique)

                                                                        #plot footprint
for key in result:
    print(i)
    i=+1
  
    if  isinstance(wkt.loads(result[key]['footprint']), Iterable):         # check if is itterabel
        for fp in wkt.loads(result[key]['footprint']):
            fp=fp
   
    else:
        fp= wkt.loads(result[key]['footprint'])
       
    if  hasattr(fp, 'geoms'):                                              # check if fp hast the attributre geoms
        geom=fp.geoms
    else:
        geom=fp
        
    index=orbits_unique.index(result[key]['relativeorbitnumber'])
    # geom = geom.to_crs(epsg=3857)           ???????
    
    xs, ys = geom.exterior.xy
    ax2.fill(xs, ys, alpha=0.5, fc='none', ec=colors[index])
    imax=np.argmax(xs)
    ax2.text(xs[imax],ys[imax],result[key]['slicenumber'],fontsize=13, color = colors[index], style = "italic")     
   
    
ax2.plot(wkt.loads(area).x,wkt.loads(area).y,'+k')
ax2.set_title('Slice Number & Area',fontsize=16)
ax2.set(xlabel='Lat', ylabel='Lon') 

                                                      
ctx.add_basemap(ax2, zoom=12)

# Trying a new way Geopandas
 
#sentinelsearch(username,key,Date,area,lat,lon)

