#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
Created on Mon Apr 27 21:07:53 2020

@author: Sophie
"""

from PIL import Image
import numpy as np
import disjointSet as ds
import reebGraph as rg
import hierarchy as hi
  
# get image data as a 2D boolean numpy array
def getImageData(init, suff, ind):
    picId = str(ind)
    im = Image.open(init + picId + suff)
    dat = ~np.array(im)
    dat = np.array(np.sum(dat,-1)/(3*255)).astype(bool)
    return dat

############################### MAIN PROGRAM ##################################

# Image file names
'''
Test set 1
init = '/Users/Sophie/Documents/MATH\ at\ UIUC/Physarum/Data/2018_02_28_crop_2_Binary'
suff = '.tif'
startInd = 1780; R = 1731; C = 1644; totalPic = 200
L = 6; step = 2**(L-1); numPass = 7; 
'''

''' 
Test set 2
init = '/Users/Sophie/Documents/MATH\ at\ UIUC/Physarum/Data/2018_06_06_crop_2_Binary'
suff = '.jpeg'
startInd = 1; R = 825; C = 773; totalPic = 200
L = 6; step = 2**(L-1); numPass = 7; 
'''

# Test set 2
init = '/Users/Sophie/Documents/MATH\ at\ UIUC/Physarum/Data/2018_06_10_crop_7_Binary'
suff = '.jpeg'
startInd = 1; R = 877; C = 883; totalPic = 200
L = 6; step = 2**(L-1); numPass = 7; 

M = R*C 

# First (long) pass: Build common pic and its components
# Note that every picture share 9/10 of its content with this common pic

Q = np.array([[1]*C]*R).astype(bool);
for i in range(startInd, startInd+totalPic):
    dat = getImageData(init, suff, i)
    if i == startInd:
        P = dat
    Q = Q&dat

print('Done getting image data for the first pass')
[common, commonRep] = ds.findCCPure(Q, R, C)
print('Done geting connected components of the intersection of all images')

# Initialize data for Reebgraph
# All CCs of first pic must be processed and later we build up from here
vert = []; adj = {}; curList = set()

# Second (long) pass: We process 33 images at a time in a (short) pass
# We first build up reasonably large info about CCs. The info is built 
# with divide and conquer style as we mentioned above
# With this info, updating Reebgraphs becomes much easier and faster task
# Then, (use this info to) build Reebgraphs when we go through 32 pairs of 
# two consecutive images during this batch of 33 images

# For each pass, passInd is the start index for a pass
passInd = startInd
for eachPass in range(numPass):
    # First extracting data step+1 images (33 images here)
    P = []
    for i in range(passInd, passInd+step+1):
        if i < startInd+totalPic:
            dat = getImageData(init, suff, i)
            dat = dat & ~Q       
        P.append(dat)
    print('Done extracting image data in pass ' + str(eachPass + 1))
    # Now get difference data 
    [dat, leftDat, rightDat] = hi.getDiffData(P, L)        
    # Find labels (and rep arrays) of CCs of all level for 32 data,
    # (32 pairs of intersections of this batch of 33 images)
    # 32 (common intersections) at level 1 and then 16-16 at level 2 and so on    
    [labels, reps] = \
        hi.getOneLabelBlock(common, commonRep, L, dat, R, C)
    # Now use the CCs info above to update the Reeb graph
    # each time we process ith and (i+1)th images in the (current) batch
    countPic = 0
    for i in range(step):
        #print('Pair ' + str(i+1))
        l = hi.labelsToUse(reps, labels, i, L)[0]
        l.append(labels[L][i])
        r = reps[L][i]
        picNum = eachPass*step+i+1
        # Note that the first pic number is 0
        if picNum < totalPic:
            countPic+=1
            rg.updateReeb(vert, adj, curList, l, r, \
                      leftDat[i], rightDat[i], R, C, picNum)
    passInd += step
    print('Updated Reeb graph. Done pass number ' + str(eachPass+1) \
          + ' for processing the next ' + str(countPic) + ' pictures.')

print('Done the second pass. Found Reeb graph!')
rg.drawGraph(vert, adj)
print('Done drawing Reeb graph. Program completed!')