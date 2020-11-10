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
import math

api = SentinelAPI('oswald', 'Hjs19970709', 'https://scihub.copernicus.eu/dhus')

# search by polygon, time, and SciHub query keywords
date=('NOW-50DAYS', 'NOW')
area='POINT (19 49)' #lon lat https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
result=api.query(date=date, area=area,producttype='SLC')


dates=[]
orbits=[]
slicenumber=[]
for key in result:
    print('relativeorbitnumber',result[key]['relativeorbitnumber'])
    orbits.append(result[key]['relativeorbitnumber'])
    dates.append(result[key]['beginposition'])
    slicenumber.append(result[key]['slicenumber'])

orbits_unique=list(set(orbits))    # get unique orbits in list 
slicenumber_unique=list(set(slicenumber))    # get unique orbits in list 


colors=['r','g','b','k','c','y','m']            

fig, (ax1, ax2) = plt.subplots(2,1)
plt.subplots_adjust(hspace=0.6)

#ax1.plot(dates,orbits,'o')
#plt.show()


# plot timeline


for n in range(0,len(orbits_unique)):
    for i in range(0,len(orbits)):
        if orbits_unique[n]==orbits[i]:
            # plot
            ax1.plot(dates[i],n,'o'+colors[n])

ax1.set_yticks(range(0,n+1))
ax1.set_yticklabels(orbits_unique)
#ax1.set_yticklabels(['Orbit Nr. %d'%orbits_unique[1],'Orbit Nr. %d'%orbits_unique[2],'Orbit Nr. %d'%orbits_unique[3]])
            # beautify the x-labels
            # fig.autofmt_xdate()
ax1.set_title('Images Found Along Time',fontsize=16)
ax1.set(xlabel='Date', ylabel='Relative Orbit Number')
            
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
        
   # for n in range(0,len(slicenumber)):
   #  ax2.annotate(slicenumber[n], xy=(18, 48),  xycoords='data',
   #  xytext=(0.8, 0.95), textcoords='axes fraction',
   # arrowprops=dict(facecolor='black', shrink=0.05),
   # horizontalalignment='right', verticalalignment='top',
   # )
        
        
                 # # # plot
     # plt.plot(dates[i],n,'*')
     # # beautify the x-labels
# plt.gcf().autofmt_xdate()
ax2.plot(wkt.loads(area).x,wkt.loads(area).y,'+k')
ax2.set_title('Slice Number & Area',fontsize=16)
ax2.set(xlabel='Lat', ylabel='Lon')
            # plt.show()            