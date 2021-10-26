#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 14:33:23 2021

@author: giacomo
"""

import ROOT
import sys
import logging



class cutFlow:
    '''
    This class takes a TTree from a .root dataset and filters all the events according to cuts given by the user.
    At the end, the efficiency of the cuts is showed by the signal / background ratio.

    Args
    ----------
    
        inFileName: string
            name of the .root dataset 
        
        nameTree: list of string
            array of all the branches of the TTree I am interested in
        
        cuts: list of string 
            array of all the cuts to apply to my dataset
            
        weight: string
            a new column would be added in the dataset where every event would be weighted according to the string 
            
        outFileName: string
           name of the file where to save the results 

    Attributes
    ----------
    
        self.inFileName: string
            take the homonym arg value
            
        self.nameTree: string
            take the homonym arg value
        
        self.outFileName: string
            take the homonym arg value
        
        self.cuts: string
            take the homonym arg value
            
        self.weight: string
            take the homonym arg value
                
        self.inFile: ROOT.TFile
            it will open the input .root dataset in a TFile
        
        self.tree: []
            list of all the branches of the TFile
        
        self.dataframe: []
            list of all the branches but using the ROOT Class RDataFrame rather than TFile to exploit specific methods
        
        self.counts: []
            list of all the events after a cut for every branch of the dataset
        
        self.counts_w = []
            list of all the weighted events after a cut for every branch of the dataset
        
        self.totalcounts = []
            list of all the events (summed for all the branches) after a cut
            
        self.totalcounts_w = []
            list of all the weighted events (summed for all the branches) after a cut
            
        self.SNR = []
            list of the ratio between Signal counts and background counts between events for every branch of the signal
        
        self.SNR_w = []
            list of the ratio between Signal counts and background counts between weighted events for every branch of the signal
        
        self.table = []
            list of strings to create a table for the Get - methods 
    
    '''
    
    def __init__(self,
                 inFileName= None,
                                  
                 nameTree= None,
                 
                 cuts = None,
                 
                 weight = None,
                 
                 outFileName = None
                 
                 ):
        
        self.inFileName= inFileName          
        self.nameTree = nameTree
        self.outFileName = outFileName
        self.inFile = ""
        self.cuts = cuts
        self.weight = weight
        self.tree = []
        self.dataframe = []
        self.table = []
        self.counts = []
        self.counts_w = []
        self.totalcounts = []
        self.totalcounts_w = []
        self.SNR = []
        self.SNR_w = []
        
        sys.stdout = open(self.outFileName,'a')


    
    def SetTree (self):
        """ 
        Open .root dataset and associate the branches to a TFile list variable.
        Some checks are done to be sure the name of the file and of the branches are inserted correctly.
        
        """    
        
        
        self.tree = []
        #Open the file .root
        
        try:
            self.inFile = ROOT.TFile.Open(self.inFileName, "Read")
        except:
            logging.warning("\033[91mError: please insert the right name of the input  dataset\033[1;0m") 
            sys.exit (1)
    
        #Retrieve the TTree from the file
        for i in range(len(self.nameTree)):
            
            if self.nameTree[i] not in [x.GetName() for x in list(self.inFile.GetListOfKeys())]:
                logging.warning("\033[91mError: the Tree '" + self.inFileName + "' does not contain this brench: '"+ self.nameTree[i] +"' . Please be sure of the name of the brench you are interested in.\n \033[1;0m")
                sys.exit (1)
            else:
                self.tree.append(self.inFile.Get(self.nameTree[i]))
    
     
    def SetDataFrame (self):
        """ 
        Associate the TTree list to a RDataFrame list. It's still an array variable of all the branches of the starting dataset,
            but with the RDataFrame variable I am able to exploit specific methods like Filter() and Count()
        The column of the value of the weighted event is added to the RDataSet.
        Some checks are done to be sure the weight is inserted correctly.
        
        """ 
        
        self.dataframe = []
        self.SetTree()
        for i in range(len(self.nameTree)):
            self.dataframe.append(ROOT.RDataFrame(self.tree[i]))
            
            try:
                self.dataframe[i] = self.dataframe[i].Define("weight", self.weight)
            except:
                logging.warning("\033[91mERROR: Please be sure you have written the weight in the right way in your config file\033[1;0m") 
                sys.exit (1)
        
        
       
            
        
        
        

    def SetCuts(self):
        """
        For every branch, a cut is done and all the events which remains are counted and collente in the array counts.
        Parallelly, all the events of all the branches are summed into totalcounts
        The same is done but with weighted data for counts_w and totalcounts_w.
        Some checks are done to be sure the cut string is inserted correctly.
        
        
        """
        
        self.counts = []
        self.counts_w = []
        
        self.totalcounts =[]
        self.totalcounts_w =[]
        
        self.SetDataFrame()
        
        self.totalcounts.append(0)
        self.totalcounts_w.append(0)
        
        
        
        for i in range(len(self.nameTree)):
            
            self.counts.append([])
            self.counts_w.append([])
            
            self.counts[i].append("")
            self.counts_w[i].append("")
            
            self.counts[i][0] = int(self.dataframe[i].Count())
            self.counts_w[i][0] = self.dataframe[i].Sum("weight").GetValue()
            
            self.totalcounts[0]= self.totalcounts[0]+ self.counts[i][0]
            self.totalcounts_w[0]= self.totalcounts_w[0]+ self.counts_w[i][0]  
            
            
            for j in range(len(self.cuts)):
                self.counts[i].append("")
                self.counts_w[i].append("")
                
                try:
                    self.dataframe[i] = self.dataframe[i].Filter(str(self.cuts[j][1]))
                except:
                    logging.warning("\033[91mERROR: Please be sure you have written the "+str(j+1)+"° cuts in the right way in your config file\033[1;0m") 
                    sys.exit (1)
        
                
                
                self.counts[i][j+1] = self.dataframe[i].Count().GetValue()
                self.counts_w[i][j+1] = self.dataframe[i].Sum("weight").GetValue()
                
                
                self.totalcounts.append(0)
                self.totalcounts_w.append(0)
                self.totalcounts[j+1]= self.totalcounts[j+1]+ self.counts[i][j+1]
                self.totalcounts_w[j+1]= self.totalcounts_w[j+1]+ self.counts_w[i][j+1]        

            
            
    def SetSNR(self, bkg ):
        """
        For every brach, the Signal / Background ratio is computed, considering every cut.
        In particular, every branch of signal is divided for ALL the branches of background.
        N.B.: as argument you can choose every kind of cutFlow istance, so be careful. 
                
        """
        
        #bkg.SetTotalCounts()
        bkg.SetCuts()
        
        self.SNR = []
        self.SNR_w = []
        for i in range(len(self.nameTree)):
            self.SNR.append([])
            self.SNR_w.append([])
            
            self.SNR[i].append("")
            self.SNR[i][0] = (float (self.counts[i][0]) / float (bkg.totalcounts[0]))
            
            self.SNR_w[i].append("")
            self.SNR_w[i][0] = (float (self.counts_w[i][0]) / float (bkg.totalcounts_w[0]))
                  
            for j in range(len(self.cuts)):
                self.SNR[i].append("")
                self.SNR[i][j+1] = (float(self.counts[i][j+1]) / float(bkg.totalcounts[j+1]))
                self.SNR_w[i].append("")
                self.SNR_w[i][j+1] = (float(self.counts_w[i][j+1]) / float(bkg.totalcounts_w[j+1]))
    
   
    
   
    def printTable (self, borderHorizontal = '-', borderVertical = '|', borderCross = '+'):
        """
        A method to print a table. It takes an array of n columns and m raws (self.table) and print all of them.
        
        """
        
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
            if (row == ["CUT", "FILTERED DATA", "WEIGHTED DATA"] or row == ["CUT", "S/B RATIO", "S/B WEIGHTED RATIO"]):
                print(s)      
        print(s)        
        print("\n\n")
    
    
    #@staticmethod
    def GetCounts(self):
        """
        It stamps all the results of the counts of events of a given branch after the cuts.
        The results are arranged in a text-table for a better read-out
        
        """
                
        print("--------------------------------------")
        print("From Tree: "+ self.inFileName);
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)):
            print("\nTreeBranch: " + self.nameTree[i]);
            
            print("STARTING DATA: "+ str(self.counts[i][0]))
            print("STARTING WEIGHTED DATA: "+ str(self.counts_w[i][0])+"\n")
            
            self.table = []            
            self.table.append(["CUT", "FILTERED DATA", "WEIGHTED DATA"])
            
            for j in range(len(self.cuts)):
                self.table.append([str(self.cuts[j][0]), str(self.counts[i][j+1]), str(self.counts_w[i][j+1])])
            
            self.printTable()        
        print("\n\n\n")
       
        logging.warning("Results of the cut of "+self.inFileName+" on "+ self.outFileName)
        



            


    def GetSNR(self, bkg):
        """
        It stamps all the results of the S/B ratio of after the cuts.
        The results are arranged in a text-table for a better read-out
        
        """
        
        print("--------------------------------------")
        print("Signal / Background ratio from");
        print("S: "+ self.inFileName )
        print("B: "+ bkg.inFileName)
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)):
            print("\nTreeBranch: " + self.nameTree[i]);
            print("STARTING S/B RATIO :"+ str(self.SNR[i][0]) )
            print("STARTING WEIGHTED S/B RATIO :"+ str(self.SNR_w[i][0])+"\n" )   
                  
            self.table = []            
            self.table.append(["CUT", "S/B RATIO", "S/B WEIGHTED RATIO"])
           
            for j in range(len(self.cuts)):
                self.table.append([str(self.cuts[j][0]), str(self.SNR[i][j+1]),str(self.SNR_w[i][j+1]) ])               
            self.printTable()    
            
            #c2 = ROOT.TCanvas('c2', 'c2', 700, 500)
           # myHisto = self.dataframe[i].Histo1D("mt")
            #myHisto.Draw()
            #c2.SaveAs("hist.png")             
        print("\n\n\n")  
        
        logging.warning("Results of the S/B ("+self.inFileName+" / "+ bkg.inFileName+" ) on "+ self.outFileName)









