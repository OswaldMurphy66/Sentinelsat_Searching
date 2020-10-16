#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:46:23 2020

@author: oswald
"""
## Remaning to do : 

#Add orbit number
#Sort by spots

# connect to the API
from sentinelsat import SentinelAPI
from datetime import date
import matplotlib.pyplot as plt
from shapely import wkt

api = SentinelAPI('oswald', 'Hjs19970709', 'https://scihub.copernicus.eu/dhus')

# search by polygon, time, and SciHub query keywords
date=('NOW-20DAYS', 'NOW')
area='POINT (19 49)' #lon lat https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
result=api.query(date=date, area=area,producttype='SLC')


dates=[]
orbits=[]
for key in result:
    print('relativeorbitnumber',result[key]['relativeorbitnumber'])
    orbits.append(result[key]['relativeorbitnumber'])
    dates.append(result[key]['beginposition'])

orbits_unique=list(set(orbits))    # get unique orbits in list 



colors=['r','g','b','k','c','y','m']            

fig, (ax1, ax2) = plt.subplots(2,1)
# plot timeline
for n in range(0,len(orbits_unique)-1):
    for i in range(0,len(orbits)):
        if orbits_unique[n]==orbits[i]:
            # plot
            ax1.plot(dates[i],n,'o'+colors[n])
            # beautify the x-labels
            # fig.autofmt_xdate()
            
            
#plot footprint


for key in result:
    print(i)
    i=+1            
    #print( result[key]['footprint'])
    
    #print(wkt.loads(result[key]['footprint']))
    
    for fp in wkt.loads(result[key]['footprint']):   
        
        if  hasattr(fp, 'geoms'):
            geom=fp.geoms
        else:
            geom=fp
            
        index=orbits_unique.index(result[key]['relativeorbitnumber'])
        
        xs, ys = geom.exterior.xy
        ax2.fill(xs, ys, alpha=0.5, fc='none', ec=colors[index])               
                 # # # plot
     # plt.plot(dates[i],n,'*')
     # # beautify the x-labels
# plt.gcf().autofmt_xdate()
ax2.plot(wkt.loads(area).x,wkt.loads(area).y,'+k')
            
            # plt.show()            