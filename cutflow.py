#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 14:33:23 2021

@author: giacomo
"""

import ROOT
import sys

class cutFlow:
    """help"""
    def __init__(self,
                 inFileName= None,
                 numTrees= None,
                 
                 nameTree= None,
                 
                 
                 
                 
                 
                 ):
        
        self.inFileName= inFileName
        
        self.numTrees = numTrees
        
        self.nameTree = nameTree
        
        self.tree = []
         
        self.inFile= ""
        
        self.dataframe = []
        
    


    
    def SetTree (self):
        """ Open File  """    
        
        """Open the file .root"""
        self.inFile = ROOT.TFile.Open(self.inFileName, "Read")

    
        """Retrieve the TTree from the file"""
        for i in range(self.numTrees):
           self.tree.append(self.inFile.Get(self.nameTree[i]))
    
     
    def SetDataFrame (self):
        """ Associate every tree to the cladd RDataFrame  """ 
        for i in range(self.numTrees):
            self.dataframe.append(ROOT.RDataFrame(self.tree[i]))
        
    



inFileName = "bkg2_Demo.root"
numTrees = 1
nameTree = ["multiboson_NoSys"]


bkg = cutFlow(inFileName, numTrees, nameTree )

print (bkg.tree)
bkg.SetTree()
print(bkg.tree)
print(bkg.dataframe)
bkg.SetDataFrame()
print(bkg.dataframe)


"""
print ("init")
tree = ["d"]
print(tree)

SetTree(inFileName, numTrees, nameTree, tree)
print ("outside func")
print (tree)

"""