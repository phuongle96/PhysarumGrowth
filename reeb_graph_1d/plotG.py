#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 05:06:23 2020

@author: Sophie
"""

import matplotlib.pyplot as plt
import numpy as np

def hanging_line(point1, point2):
    import numpy as np

    a = (point2[1] - point1[1])/(np.cosh(point2[0]) - np.cosh(point1[0]))
    b = point1[1] - a*np.cosh(point1[0])
    x = np.linspace(point1[0], point2[0], 100)
    y = a*np.cosh(x) + b

    return (x,y)


def drawReeb(data):
    #data= {(0,1):[6,7],(2,1):[12],(6,2): [13],(8,2): [13],(10,2): [13],(11,2): [12],(9,2): [13],(16,5):[],
    #    (1,1):[12], (3,1):[], (15,5):[],(4,1):[8,9],(7,2): [],(5,1): [10,11],(12,3): [13],(13,4):[14,15,16],(14,5):[]}
    x_coord=[]
    y_coord= []  
        
    
    for key in sorted(data.keys()):
        x_coord.append(key[0])
        y_coord.append(key[1])  
        x = np.array(x_coord) - np.random.uniform(low=40, high=60, size=(len(x_coord),))
        #x = np.array(x_coord) - r.randrange(40, 60, 2) 
        #x = np.array(x_coord)
        y= np.array(y_coord) + np.random.uniform(low=-0.1, high=0.1, size=(len(x_coord),))
        #print(x,y)
        #plt.plot(x,y, 'ro')   

    #axes = plt.gca()
    #axes.set_ylim([-1,len(y)+5])
    #plt.yticks(np.arange(-1,len(y)+1, step=1))
    #fig,ax = plt.subplots()
    for key in sorted(data.keys()):
        if len(data[key])!=0:
            #plt.annotate(key[0],(x[key[0]],y[key[0]]),color='green')
            rel1 = np.array(data[key])
            for elt in rel1:
        #index = np.where(x==elt)[0]
        #print(index)
                point1 = [x[key[0]],y[key[0]]]
                point2 = [x[elt],y[elt]]
                #print(point1,point2)
                a,b = hanging_line(point1, point2)

                plt.plot(point1[0], point1[1],marker=".",markersize=3,color='black')
                plt.plot(point2[0], point2[1], marker=".",markersize=3,color='black')
                plt.plot(a,b)
        else: 
            plt.plot(x[key[0]],y[key[0]],marker=".",markersize=3,color='red')
            #plt.annotate(key[0],(x[key[0]],y[key[0]]))
    #ax.margins(x=0,y=0.002)
data= {(0,1):[6,7],(2,1):[12],(6,2): [13],(8,2): [13],(10,2): [13],(11,2): [12],(9,2): [13],(16,5):[],
(1,1):[12], (3,1):[], (15,5):[],(4,1):[8,9],(7,2): [],(5,1): [10,11],(12,3): [13],(13,4):[14,15,16],(14,5):[]}
drawReeb(data)  