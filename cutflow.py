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
                 
                 cuts = None,
                 
                 outFileName = None
                 
                 ):
        
        self.inFileName= inFileName
                        
        self.nameTree = nameTree
        
        self.cuts = cuts
        
        self.outFileName = outFileName
        
        self.inFile = ""
        
        self.outFile = ""
            
        self.tree = []
                         
        self.dataframe = []
        
        self.counts = []
        
        self.totalcounts = []
        
        self.table = []
        
        self.SNR = []
        
        sys.stdout = open(self.outFileName,'a')


    
    def SetTree (self):
        """ Open File  """    
        
        #Open the file .root
        self.inFile = ROOT.TFile.Open(self.inFileName, "Read")

    
        #Retrieve the TTree from the file
        for i in range(len(self.nameTree)):
           self.tree.append(self.inFile.Get(self.nameTree[i]))
    
     
    def SetDataFrame (self):
        """ Associate every tree to the class RDataFrame  """ 
        for i in range(len(self.nameTree)):
            self.dataframe.append(ROOT.RDataFrame(self.tree[i]))
        
    

    def SetCuts(self):
        """Filter all the data according to specific constraints"""
        self.SetDataFrame()
        
        for i in range(len(self.nameTree)):
            self.counts.append([])
            
            self.counts[i].append("")
            self.counts[i][0] = int(self.dataframe[i].Count())
            
            for j in range(len(self.cuts)):
                self.counts[i].append("")
                self.dataframe[i] = self.dataframe[i].Filter(str(self.cuts[j][1]))
                self.counts[i][j+1] = int(self.dataframe[i].Count())
            
            
          
            
    def SetTotalCounts(self):
        """  Sum all the data of all the branches for a given cut """ 
        self.totalcounts =[]
        
        
        for j in range(len(self.cuts)+1):
            self.totalcounts.append(0)
            
            
                
            for i in range(len(self.nameTree)):
                self.totalcounts[j]= int(self.totalcounts[j])+ int(self.counts[i][j])
                
            #print (self.totalcounts[j])
        
    
   
    def printTable (self, borderHorizontal = '-', borderVertical = '|', borderCross = '+'):
        cols = [list(x) for x in zip(*self.table)]
        lengths = [max(map(len, map(str, col))) for col in cols]
        f = borderVertical + borderVertical.join(' {:>%d} ' % l for l in lengths) + borderVertical
        
        s=borderCross
        for col in range(len(cols)):
            s = s + (borderHorizontal * (int(lengths[col])+2)) + borderCross
        
        #s = borderCross + borderCross.join(borderHorizontal * (l+2) for l in lengths) + borderCross
        

        print(s)
        for row in self.table:
            print(f.format(*row))
            if (row == ["CUT", "FILTERED DATA"] or row == ["CUT", "S/B RATIO"]):
                print(s)      
        print(s)        
        print("\n\n")
    
    
    #@staticmethod
    def GetCounts(self):
        """cout the results for all the counts according to the filters applied"""
        
        
        
        
        print("From Tree: "+ self.inFileName);
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)):
            print("\nTreeBranch: " + self.nameTree[i]);
            
            print("STARTING DATA: "+ str(self.counts[i][0])+"\n")
            
            self.table = []
            
            self.table.append(["CUT", "FILTERED DATA"])
            for j in range(len(self.cuts)):
                self.table.append([str(self.cuts[j][0]), str(self.counts[i][j+1])])
                #print("Cut: "+ self.cuts[j][0]+"\t\t\t\t\t\t"+str(self.counts[i][j+1]))
            self.printTable()    
        
        print("\n\n\n")
        
        


    def SetSNR(self, bkg ):
        """do all the S / B ratio for every signal and for every cut. Specifically it is the ratio of a branch of the signal over all the branches of the background"""
        bkg.SetTotalCounts()
        
        self.SNR = []
        for i in range(len(self.nameTree)):
            self.SNR.append([])
            
            self.SNR[i].append("")
            self.SNR[i][0] = (float (self.counts[i][0]) / float (bkg.totalcounts[0]))
            
            
                  
            for j in range(len(self.cuts)):
                self.SNR[i].append("")
                self.SNR[i][j+1] = (float(self.counts[i][j+1]) / float(bkg.totalcounts[j+1]))
            
                #print(self.SNR[i][j])
            
#   x = [['Length', 'Time(ms)'], [0, 0], [250, 6], [500, 21], [750, 50], [1000, 87], [1250, 135], [1500, 196], [1750, 269], [2000, 351]]
#   printTable(x)

    def GetSNR(self, bkg):
        """cout all the S/N according to the filters applied"""
        
        
        
        
        print("Signal / Backroung ratio from");
        print("S: "+ self.inFileName )
        print("B: "+ bkg.inFileName)
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)):
            print("\nTreeBranch: " + self.nameTree[i]);
            print("STARTING S/B RATIO :"+ str(self.SNR[i][0])+"\n" )
                                    
            self.table = []
            
            self.table.append(["CUT", "S/B RATIO"])
            for j in range(len(self.cuts)):
                self.table.append([str(self.cuts[j][0]), str(self.SNR[i][j+1])])
                #print("Cut: "+ self.cuts[j][0]+"\t\t\t\t\t\t"+str(self.counts[i][j+1]))
            self.printTable()    
        
        print("\n\n\n")    






outFile = open (outFileName, 'w')
outFile.close()


bkg = cutFlow(inFileName, nameTree, cuts, outFileName )
bkg.SetTree()
bkg.SetCuts()
bkg.SetTotalCounts()
bkg.GetCounts()




sig = cutFlow("signal_Demo.root",["C1N2_WZ_300_0_NoSys","C1N2_WZ_300_0_NoSys"],cuts,outFileName )
sig.SetTree()
sig.SetCuts()
sig.SetTotalCounts()
sig.GetCounts()

sig.SetSNR(bkg)
sig.GetSNR(bkg)

