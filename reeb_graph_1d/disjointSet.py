#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:10:07 2020

@author: Sophie
"""
# Here disjoint-set data structure is implemented
# This structure is then used to find the connected components
# based on previous connected components and new edges added
class Subset: 
    def __init__(self, parent, rank): 
        self.parent = parent 
        self.rank = rank 
        
def find(subsets, node): 
    if subsets[node].parent != node: 
        subsets[node].parent = find(subsets, subsets[node].parent) 
    return subsets[node].parent 
  
# A function that does union of two sets  
# of u and v(uses union by rank) 
def union(subsets, u, v): 
    u = find(subsets, u)
    v = find(subsets, v)
    # Attach smaller rank tree under root  
    # of high rank tree(Union by Rank)
    if u == v:
        return
    if subsets[u].rank > subsets[v].rank: 
        subsets[v].parent = u 
    elif subsets[v].rank > subsets[u].rank: 
        subsets[u].parent = v 
          
    # If ranks are same, then make one as  
    # root and increment its rank by one 
    else: 
        subsets[v].parent = u 
        subsets[u].rank += 1
        
        
#######  FINDING CONNECTED COMPONENTS ###########
### Helpers that incrementally build up connected components info with efficiency ###
        
# Given a position(id) in original grid
# try to use chain of labels to find the latest label that is used
# to label the grid at this position
def findLabel(labels, id):
    #print('Label size' + str(len(labels)))
    for i in range(len(labels)-1, -1,-1):
        if id in labels[i]:
            for j in range(i, len(labels)):
                id = labels[j][id]
            return id
    return -1

def findCC(labels, rep, add, R, C):
    # Create cells and do the union on set of vertices
    # including added one and the components contracted
    # from the last figure (last labels)
    M = R*C; cells = {}; numComp = len(rep)
    #print('Connected comp: ' + str(numComp) + ', add size: ' + str(len(add)))
    for i in range(numComp):
        cells[M + i] = Subset(M+i, 0)
    for i, j in add:
        cells[i*C+j] = Subset(i*C+j, 0)
    # Incrementally add edges and do union-find operations
    for i,j in add:
        # Listing possible neighbors of a black cell added
        val = i*C+j; nei = []
        if i < R-1: nei.append((i+1)*C+j)
        if i > 0: nei.append((i-1)*C+j)
        if j < C-1: nei.append(i*C+j+1)
        if j > 0: nei.append(i*C+j-1)
        
        for id in nei:
            if id in cells:
                union(cells, id, val)
            else:
                curId = findLabel(labels, id)
                if curId != -1:
                    union(cells, curId, val)
    
    # create label for components and return curRep
    # (representative ids in the original grid for each component)
    label = {}; curRep = {}; comp = {}
    count = M
    for e1 in cells:
        root = find(cells, e1)
        if root not in comp:
            if root >= M:
                curRep[count] = rep[root]
            else:
                curRep[count] = root
            comp[root] = count
            label[e1] = count
            count += 1
        else:
            label[e1] = comp[root]
    return [label, curRep]

# Find CCs data purely based on grid using two-pass algorithms with union-find
def findCCPure(Q, R, C):
    M = R*C; label = {}; cells = []
    # First pass

    # First pass: do a coarse labeling
    for i in range(R):
        for j in range(C):
            if Q[i][j] == 0:
                continue
            # Listing possible neighbors of a black cell added
            val = i*C+j; neis = [];
            if i > 0 and Q[i-1][j] == 1: neis.append((i-1)*C+j)
            if j > 0 and Q[i][j-1] == 1: neis.append(i*C+j-1)
            if len(neis) == 0:
                label[val] = len(cells)
                cells.append(Subset(len(cells), 0))
            else:
                cur = neis[0]; minLabel = label[cur]
                for ind in range(1, len(neis)):
                    prev = cur; cur = neis[ind]
                    union(cells, label[prev], label[cur])
                    minLabel = min(minLabel, label[cur])
                label[val] = minLabel                
    # Second pass: Reassign CCs
    allLabels = {}; rep = {}
    for e in label:
        label[e] = find(cells, label[e])
        if label[e] not in allLabels:
            allLabels[label[e]] = len(allLabels)+M
            rep[allLabels[label[e]]] = e
        label[e] = allLabels[label[e]]    
    return [label, rep]