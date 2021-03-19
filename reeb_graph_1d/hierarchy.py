#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
Created on Mon Apr 27 21:09:32 2020

@author: Sophie
"""

import numpy as np
import math
import disjointSet as ds

####### DIVIDE AND CONQUER STYLE THAT MAKE USE OF EXISTING CCS #########
 
# Helper fct: find the set of labels l that provide existing CCs 
#(don't have to find CCs again for vertices already there-the ones not in add)
# the previous representative array that help to find current rep array faster
def labelsToUse(reps, labels, n, level):
    # Find representative list r to use
    # for the call findCC(labels, rep, add, R, C)
    # This method make use of previous data 
    # to build a data (connected comps) on larger complex
    n += 1
    if level == 1:
        r = reps[0][0]
    else:
        r = reps[level-1][int(math.ceil(n/2))-1]
    # Now iteratively add a necessary mappings (of verts to component names)
    # to the list l. ex: ind 4 -> 5(lev 4) -> 3(lev 3) -> 2(lev 2) -> 1(lev 1)
    l = [labels[0][0]]; 
    while level > 1:
        n = int(math.ceil(n/2))
        l.insert(1, labels[level-1][n-1])
        level -= 1
    return [l,r]
    
# Divide data into level. level 0 is common data
# L is the maximum level. from 1 to L there are 2^{l-1} data 
# if you're in level l. dat is the data of difference. Data of difference
# only have L-1 level however because the common data is not counted here
# dat[level-1] is an array with 2^{level-1} elements. Each element
# contains pairs of coordinate that are added to the previous level
def getOneLabelBlock(common, commonRep, L, dat, R, C):
    labels = [[common]]; reps = [[commonRep]]
    for lev in range(1, L+1):
        #print('Get one block at level ' + str(lev))
        labels.append([]); reps.append([])
        for i in range(2**(lev-1)):
            # Set of labels l for existing connected component info
            # previous representative array to use r
            [l, r] = labelsToUse(reps, labels, i, lev)
            # From l and r above find label info 
            # (map each vertex of the same component to a label)
            tmp = ds.findCC(l, r, dat[lev-1][i], R, C)
            labels[lev].append(tmp[0]); reps[lev].append(tmp[1])
    return [labels, reps]

def getDiffData(P, L):
    tmp = []; leftDat = []; rightDat = []
    for i in range(len(P)-1):
        tmp.append(P[i] & P[i+1])
        test = P[i] & ~tmp[i]
        leftDat.append(np.array(np.where(test == 1)).T)
        test = P[i+1] & ~tmp[i]
        rightDat.append(np.array(np.where(test == 1)).T) 
    P = tmp; dat = []
    for lev in range(L): dat.append([])
    for lev in range(L-1, -1,-1):
        tmp = [];
        if lev > 0:
            for i in range(2**(lev-1)):
                tmp.append(P[2*i] & P[2*i+1])
            for i in range(2**lev):
                P[i] = P[i] & ~tmp[i//2]
                dat[lev].append(np.array(np.where(P[i] == 1)).T) 
            P = tmp;
        else:
            dat[0].append(np.array(np.where(P[0] == 1)).T)
    return [dat,leftDat,rightDat]

