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

def sentinelsearch(username,key,date,area) :
    
    ## Inputs:
     #   username: string, username to sentinel hub api
     #   key: string, password to sentinel hub api
     #   date: string, including time point and duration for searching data. For example: date=('NOW-300DAYS', 'NOW')
     #   area: Well-known_text_representation_of_geometry. indicating longitute and latitute  For example: area='POINT (19 49)' 
     
     
    api = SentinelAPI(username, key, 'https://scihub.copernicus.eu/dhus')
    
                                                                                   # search by polygon, time, and SciHub query keywords
    date=date
    area=area                                                                      #lon lat https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    result=api.query(date=date, area=area,producttype='SLC')                       # form 'result' as a dictionary containing meta data of the images found in that certain place
    
    
    dates=[]
    orbits=[]
    slicenumber=[]
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
               ax1.plot(dates[i],n-(id_spot+1)/(len(slicenumber_unique)+1),'o'+colors[n])
               ax1.plot(dates[i],n,'o'+colors[n])
     
    ax1.set_yticks(range(0,n+1))
    ax1.set_yticklabels(orbits_unique)
    
    
    
                                                                                   #plot footprint
    for key in result:
        print(i)
        i=+1
      
        if  isinstance(wkt.loads(result[key]['footprint']), Iterable):             # check if is itterabel
            for fp in wkt.loads(result[key]['footprint']):
                fp=fp
       
        else:
            fp= wkt.loads(result[key]['footprint'])
           
        if  hasattr(fp, 'geoms'):                                                  # check if fp hast the attributre geoms
            geom=fp.geoms
        else:
            geom=fp
            
        index=orbits_unique.index(result[key]['relativeorbitnumber'])
        
        xs, ys = geom.exterior.xy
        ax2.fill(xs, ys, alpha=0.5, fc='none', ec=colors[index])
        imax=np.argmax(xs)
        ax2.text(xs[imax],ys[imax],result[key]['slicenumber'],fontsize=13, color = colors[index], style = "italic")     
       
        
    ax2.plot(wkt.loads(area).x,wkt.loads(area).y,'+k')
    ax2.set_title('Slice Number & Area',fontsize=16)
    ax2.set(xlabel='Lat', ylabel='Lon')                                                                                   # plt.show()
    return                                   
                                                                               
username='oswald'
key='Hjs19970709'
                                                                               # search by polygon, time, and SciHub query keywords
date=('NOW-300DAYS', 'NOW')
area='POINT (19 49)'          

sentinelsearch(username,key,date,area)

