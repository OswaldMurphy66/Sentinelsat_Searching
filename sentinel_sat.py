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
import contextily as cx

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



  
def getImageCluster(lat_deg, lon_deg, zoom):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    x, y =deg2num(lat_deg, lon_deg, zoom)
    
    NW=num2deg(x, y, zoom)                                      # calculate extension NW-corner
    SE=num2deg(x+1, y+1, zoom)                                      # calculate extension SE-corner
    extent=[NW[1],SE[1], SE[0], NW[0]]                       # extent for image (left, right, bottom, top)

    
    
    
    try:
        imgurl=smurl.format(zoom, x, y)
        print("Opening: " + imgurl)
        imgstr = requests.get(imgurl, headers=headers)
        tile = Image.open(requests.get(imgurl, stream=True).raw)
        
    except: 
        print("Couldn't download image")
        tile = None

    return tile,extent

def sentinelsearch(username,key,Date,area,lon,lat) :
    ## Inputs:
     #   username: string, username to sentinel hub api
     #   key: string, password to sentinel hub api
     #   date: string, including time point and duration for searching data. For example: date=('NOW-300DAYS', 'NOW')
     #   area: Well-known_text_representation_of_geometry. indicating longitute and latitute  For example: area='POINT (19 49)' 
     
     
    api = SentinelAPI(username, key, 'https://scihub.copernicus.eu/dhus')
                                                                                       # search by polygon, time, and SciHub query keywords
    date=Date
    area=area                                                                      #lon lat https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    result=api.query(date=date, area=area,producttype='SLC')                       # form 'result' as a dictionary containing meta data of the images found in that certain place
    
    df = api.to_geodataframe(result)
    
    dates=[]
    orbits=[]
    slicenumber=[]
    y_Ticks=[]
    
    #result = {result[key] for key in result if result[key]['sensoroperationalmode'] == "IW"]
    result = {key:value for (key, value) in result.items() if value['sensoroperationalmode'] != "WV"}
    #result = dict.fromkeys(result)
    
    for key in result:
        print('relativeorbitnumber',result[key]['relativeorbitnumber'])
        orbits.append(result[key]['relativeorbitnumber'])                          # recording relative orbit number in an array
        dates.append(result[key]['beginposition'])                                 # recording beginposition orbit number in an array
        slicenumber.append(result[key]['slicenumber'])
    
    orbits_unique=list(set(orbits))                                                # get unique orbits in list
    slicenumber_unique=list(set(slicenumber))                                      # get unique slicenumbers in list
    
    slice_list = [[] for i in range(len(orbits_unique))]
    slice_list_unique = [[] for i in range(len(orbits_unique))]
    for i in range(0, len(orbits_unique)):                                     
        for n in range(0, len(orbits)):
            if orbits[n] == orbits_unique[i]:
                slice_list[i].append(slicenumber[n])
        slice_list_unique[i] = list(set(slice_list[i]))
            
    colors=['r','g','b','k','c','y','m']                                           # creating an array for applying different colors
    
    fig, (ax1, ax2) = plt.subplots(2,1)                                            # form 2 separate plots 
    plt.subplots_adjust(hspace=0.6)                                              # adjusting space between subplots
    
    idx_list = []
    idx_list_unique = []
    for i in range(0, len(orbits_unique)):
        idx_list.append([(orbits_unique[i])])
        idx_list.append(slice_list_unique[i])
        y_Ticks.append(i)
        for n in range(0, len(orbits)):
            if orbits[n] == orbits_unique[i]:
                id_spot = slice_list_unique[i].index(slicenumber[n])
                y_tick = i - (id_spot+1) / (len(slice_list_unique[i])+1)
                ax1.plot(dates[n], y_tick, 'o'+colors[i])
                ax1.plot(dates[n],i,'o'+colors[i])
                y_Ticks.append(y_tick)
    
    y_Ticks_unique = list(dict.fromkeys(y_Ticks))
    idx_list_unique = [col for row in idx_list for col in row]
    ax1.set_yticks(y_Ticks_unique)
    ax1.set_yticklabels(idx_list_unique)
    
    idx = 0
    for i in range(0, len(orbits_unique)):
        txt = ax1.get_yticklabels()[idx]
        txt.set_fontsize(18)
        idx = idx + len(idx_list[i*2]) + len(idx_list[i*2+1])                  # position of relative orbit number in the whole list
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
        
        xs, ys = geom.exterior.xy
        ax2.fill(xs, ys, alpha=0.5, fc='none', ec=colors[index])
        imax=np.argmax(xs)
        ax2.text(xs[imax],ys[imax],result[key]['slicenumber'],fontsize=13, color = colors[index], style = "italic")     
       
        
    ax = df.plot(ax=ax2, alpha=0)
    cx.add_basemap(ax, crs=df.crs)
    
    ax2.plot(wkt.loads(area).y,wkt.loads(area).x,'+k')
    ax2.set_title('Slice Number & Area',fontsize=16)
    ax2.set(xlabel='Lat', ylabel='Lon')
    
    return                                   
                                                                               
username='oswald'
key='Hjs19970709'
                                                                               # search by polygon, time, and SciHub query keywords
Date=('NOW-1000DAYS', 'NOW')
lon= 7.01847572282207
#lon=9
#lat=49
#lon =117.963
lat=51.45850017456052
#at =40.953
area='POINT ('+str(lon)+' '+ str(lat)+')'   

     

sentinelsearch(username,key,Date,area,lon,lat)

