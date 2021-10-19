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
                                  
                 nameTree= None,
                 
                 cuts = None
                 
                 
                 
                 ):
        
        self.inFileName= inFileName
        
        
        
        self.nameTree = nameTree
        
        self.cuts = cuts
        
        self.tree = []
         
        self.inFile= ""
        
        self.dataframe = []
        
        self.counts = []
        
    


    
    def SetTree (self):
        """ Open File  """    
        
        #Open the file .root
        self.inFile = ROOT.TFile.Open(self.inFileName, "Read")

    
        #Retrieve the TTree from the file
        for i in range(len(self.nameTree)):
           self.tree.append(self.inFile.Get(self.nameTree[i]))
    
     
    def SetDataFrame (self):
        """ Associate every tree to the cladd RDataFrame  """ 
        for i in range(len(self.nameTree)):
            self.dataframe.append(ROOT.RDataFrame(self.tree[i]))
        
    

    def SetCuts(self):
        """Filter all the data according to specific constraints"""
        self.SetDataFrame()
        for i in range(len(self.nameTree)):
            self.counts.append([])
            
            for j in range(len(self.cuts)):
                self.counts[i].append("")
                self.dataframe[i] = self.dataframe[i].Filter(str(self.cuts[j][1]))
                self.counts[i][j] = int(self.dataframe[i].Count())
            
        
            


inFileName = "bkg2_Demo.root"

nameTree = ["multiboson_NoSys"]

cuts = [
          ("Preselection 1 lepton, $E_\mathrm{T}^\mathrm{miss} > $ 150 GeV, $N_\mathrm{jet30} = $ 2-3, $m_{\mathrm{T}}$ $>$ 50 GeV", "trigMatch_metTrig&&met>150&&nJet30>=2&&nJet30<4&&nLep_base==1&&nLep_signal==1&&mt>50"),
          ("$N_{\mathrm{b-jets,30}} =$ 2", "nBJet30_DL1==2"),
          ("$m_{\mathrm{bb}}$ $>$ 50 GeV", "mbb>50"),
          ("105 $<$ $m_{\mathrm{bb}}$ $<$ 135 GeV", "mbb>105&&mbb<135"),
          ("$m_{\mathrm{CT}}$ $>$ 160 GeV", "mct>160"),
          ("$E_\mathrm{T}^\mathrm{miss} > $ 200 GeV", "met>200"),
           #("met>200", "met > 200"),
        ]

len(cuts)

bkg = cutFlow(inFileName, nameTree, cuts )

print (bkg.tree)
bkg.SetTree()
print(bkg.tree)
print(bkg.counts)

bkg.SetCuts()
print(bkg.counts)








"""
print ("init")
tree = ["d"]
print(tree)

SetTree(inFileName, numTrees, nameTree, tree)
print ("outside func")
print (tree)

"""