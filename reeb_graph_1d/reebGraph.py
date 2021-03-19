#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:49:08 2020

@author: Sophie
"""

import disjointSet as ds
import plotG as pg

######### REEB GRAPHS UPDATING #############
# A few structs that help update Reebgraph from one pic to the next
# See updateReeb function below
    
# id is one representative position in the original grid
class ReebNode:
    def __init__(self, id, level):
        self.id = id
        self.level = level
        
class Node:
    def __init__(self):
        self.id = 0
        self.child = []
    def addChild(self, id):
        self.child.append(id)
        
class ChildNode:
    def __init__(self):
        self.p1 = -1
        self.p2 = -1

def addNode(vert, adj, curList, id, level):
     vert.append(ReebNode(id, level))
     adj[len(vert)-1] = []
     curList.add(len(vert)-1)

def initReebGraph(vert, adj, curList, r, M):
    for key in r:
        vert.append(ReebNode(r[key], 0))
        adj[key-M] = []
        curList.add(key-M)
    print('Done initializing Reeb graph. First picture processed.')

def dataForDrawing(vert, adj):
    data = {}
    for i in range(len(vert)):
        data[(i, vert[i].level)] = adj[i]
    return data

def drawGraph(vert, adj):
    pg.drawReeb(dataForDrawing(vert, adj))

# Second pass: Go through all pairs of consecutive images in chunks 
# and update vert, adj, and curList
# Add components that are split from previous step
# or components that are merged or new component to curList
def updateReeb(vert, adj, curList, labels, rep, add1, add2, R, C, picNum):
    M = R*C
    # From existing CCs data (labels and rep) of the intersection of 2 pics
    # We find CCs data for current two consecutive pics
    [l1, r1] = ds.findCC(labels, rep, add1, R, C)
    if picNum == 1 and len(vert) == 0:
        initReebGraph(vert, adj, curList, r1, M)
        
    [l2, r2] = ds.findCC(labels, rep, add2, R, C)
    # node1, node2, childs are 3 vertice sets of  a small tripartite graph 
    # that help update the existing Reeb graph
    node1 = []; node2 = []; childs = []
    for i in range(len(r1)): node1.append(Node())
    for i in range(len(r2)): node2.append(Node())
    for i in range(len(rep)):
        childs.append(ChildNode());  
        childs[i].p1 = l1[i+M]-M; childs[i].p2 = l2[i+M]-M
        node1[l1[i+M]-M].addChild(i)
        node2[l2[i+M]-M].addChild(i)
    # Find 1-1 mapping btw ids in curList and ids in node1
    for i in curList:
        #print(vert[i].id)
        curId = ds.findLabel(labels, vert[i].id)
        if curId != -1:
            curId = l1[curId]
        else:
            curId = l1[vert[i].id]
        node1[curId-M].id = i
    # Remove nodes in node1 that split or merge or dies
    node1ToRemove = set()
    # and add nodes in node2 splitted or merged from node1
    # or newborn. To find newborns, need  to track node2Left
    # nodes in node2 haven't been processed
    node2Left = set()
    for i in range(len(r2)): node2Left.add(i)
    
    # Now go through all vertices in node1 (CCs in pic1 indeed)
    # then see which one is split, merge or die based on 
    # its children in childs and the parent of those children in node2
    for i in range(len(r1)):
        # Nodes split
        if len(node1[i].child) > 1:
            for c in node1[i].child:
                p2 = childs[c].p2
                if len(node2[p2].child)==1:
                    addNode(vert, adj, curList, r2[p2+M], picNum)
                    adj[node1[i].id].append(len(vert)-1)
                    node2Left.discard(childs[c].p2)
            node1ToRemove.add(node1[i].id)
        # Nodes merge or going to be the same
        elif len(node1[i].child) == 1:
            p2 = childs[node1[i].child[0]].p2
            if len(node2[p2].child) > 1:
                if p2 in node2Left:
                    addNode(vert, adj, curList, r2[p2+M], picNum)
                    node2Left.discard(p2)
                adj[node1[i].id].append(len(vert)-1)
                node1ToRemove.add(node1[i].id)
            # Node will be the same. No need to consider it for curList
            else:
                node2Left.discard(p2)
                # This node in pic1 persist but
                # Important: have to update id(original cell in grid)
                # of this node in pic1
                vert[node1[i].id].id = rep[node1[i].child[0]+M]
        else:
            node1ToRemove.add(node1[i].id)
    # To avoid breaking the above iterator's internal structure,
    # node1ToRemove is created to keep track of nodes in pic1 that
    # should be removed from current list for processing Reebgraph
    for node in node1ToRemove:
        curList.discard(node)
    # Finally add newborns in node2 (new CCs in pic2) to this current list
    for node in node2Left:
        addNode(vert, adj, curList, r2[node+M], picNum)