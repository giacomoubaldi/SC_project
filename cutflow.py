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
    This class takes a TTree from a .root dataset and filters all the events according to a cut-based event selection. Cuts are given manually by the user through a config file.
    At the end, the efficiency of the cuts is showed by the signal / background ratio.

    Args
    ----------
    
        inFileName: string
            name of the .root dataset 
        
        nameTree: list of string
            list of the names of all the branches of the TTree I am interested in
        
        cuts: list of string 
            list of all the cuts to apply to my dataset.
            
        weight: string
            a new column would be added in the dataset where every event would be weighted by what is written in this string
            
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
            list of all the branches but using the ROOT Class RDataFrame rather than TTree to exploit specific methods
        
        self.counts: []
            list of the number of the events after a cut for every branch of the dataset
        
        self.counts_w = []
            list of all the number of the weighted events after a cut for every branch of the dataset
        
        self.totalcounts = []
            list of all the number of the events (summed for all the branches) after a cut
            
        self.totalcounts_w = []
            list of all the number of the weighted events (summed for all the branches) after a cut
            
        self.SNR = []
            list of the ratio between Signal counts and background counts for every branch events of the signal
        
        self.SNR_w = []
            list of the ratio between Signal counts and background counts for every branch weighted events of the signal
        
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
        
 #I will use self. attributes in order to pass just 'self' as arguments of methods       


    
    def SetDataFrame (self):
        """ 
        Open .root dataset and associate its branches to a TTree list. Then shift the TTree list into a RDataFrame list;
        the advantage is that I am able to exploit specific methods of the RDataFrame class like Filter() and Count() fundamental for the cutflow.
        The column of the value of the weighted event is added to the RDataSet and it will be used in the cutflow analysis.
        Some checks are done to be sure the branch names and weight are inserted correctly.
        
        
        """    
        
        #inizialize the array         
        self.tree = []
        self.dataframe = []
        
        #Open the file .root
        #If the input name is wrong in the configfile, then exit
        try:
            self.inFile = ROOT.TFile.Open(self.inFileName, "Read")
        except:
            logging.warning("\033[91mError: please insert the right name of the input  dataset\033[1;0m") 
            sys.exit (1)
    
        
        for i in range(len(self.nameTree)): #for every branch
            
            #If the branch I am looking for is not present in the TFile, then exit
            if self.nameTree[i] not in [x.GetName() for x in list(self.inFile.GetListOfKeys())]:
                logging.warning("\033[91mError: the Tree '" + self.inFileName + "' does not contain this brench: '"+ self.nameTree[i] +"' . Please be sure of the name of the brench you are interested in.\n \033[1;0m")
                sys.exit (1)
            else:
                
                #Retrieve the TTree from the file               
                self.tree.append(self.inFile.Get(self.nameTree[i]))
                
                #shift a TTree array element in a RDataFrame array element that i will use for the cuflow
                self.dataframe.append(ROOT.RDataFrame(self.tree[i]))
                
                #Add the column "weight" for every RDataFrame branches that will be used in the cutflow
                #Since the dataset we are using are made of simulated data, weight rapresents how every single simulated data would be found in reality considering all the efficiency coefficients
                #If the weight is bad written in the configfile, then exit
                try:
                    self.dataframe[i] = self.dataframe[i].Define("weight", self.weight)
                except:
                    logging.warning("\033[91mERROR: Please be sure you have written the weight in the right way in your config file\033[1;0m") 
                    sys.exit (1)
     
       

    def SetCuts(self):
        """
        For every branch, a cut-based event selection is done and all the events which remain are counted and the number is collected in the array 'counts'.
        The array 'counts' is 2D: counts[i][j] where 'i' stands for the branch and 'j' for the cut.
            F.e. counts[2][3] contains the number of events of the 3° branch i am analizying after the 4° cut is applied.
            N.b.: it is a "projection" cutflow, so every cut is influenced by the previous one: it means that the order of the cuts makes the difference.
        
        Parallelly, all the events of all the branches are summed into 'totalcounts'. This is done because when we will do S/B ratio, it would be 1 signal branch / ALL bkg branches, so I need to summ all the counts.
        The array 'totalcounts' is 1D: totalcounts[j] where 'j' stands for the cut.
            F.e. counts[2] contains the number of ALL events (sum of all the 'i' branches) after the 3° cut is applied.
        
        The same is done but with weighted data for 'counts_w' and 'totalcounts_w'.
        Some checks are done to be sure the cut string is inserted correctly.
        
        We will use the counts of signal and of the background to determine the efficiency of the cutflow method (via S/B ratio)
        
        """
        
        #inizialize the array  
        self.counts = []
        self.counts_w = []
        self.totalcounts =[]
        self.totalcounts_w =[]
        
        #call SetDataFrame method to have the RDataFrame array 'self.dataframe' ready to be used for the cutflow
        self.SetDataFrame()
        
        
        self.totalcounts.append(0)
        self.totalcounts_w.append(0)
        
        
        #Start the cutflow
        for i in range(len(self.nameTree)): #for every branch
            
            #define the element of the i-sh branch
            self.counts.append([])
            self.counts_w.append([])
            
            #for every i element, define the element of the j-sh cut
            self.counts[i].append("")
            self.counts_w[i].append("")
            
            #for every i element, the j=0 element is the one when no cut is done, so of the starting data
            #the method dataframe[i].Count() just counts how many events are present in the i-sh branch
            self.counts[i][0] = self.dataframe[i].Count().GetValue()
            #the metod dataframe[i].Sum("weight").GetValue() sums the weight of all the events which are present in the i-sh branch
            self.counts_w[i][0] = self.dataframe[i].Sum("weight").GetValue()
            
            #Again, the j=0 element is the one when no cut is done, so in this case the sum of ALL the events of ALL the 'i' branches
            #just sum all the counts[i]
            self.totalcounts[0]= self.totalcounts[0]+ self.counts[i][0]
            #just sum all the counts_w[i]
            self.totalcounts_w[0]= self.totalcounts_w[0]+ self.counts_w[i][0]  
            
            #start to apply the cuts
            for j in range(len(self.cuts)): #for every cut
                #for the i-sh branch element, define the element of the j-sh cut
                self.counts[i].append("")
                self.counts_w[i].append("")
                
                #If the cut is bad written in the configfile, then exit
                try:                    
                    #Filter() is a method that loops on all the events and filter out the ones which do not satisfy the cuts given as arguments
                    #it means that after the filter(), dataframe losts the events forever
                    self.dataframe[i] = self.dataframe[i].Filter(str(self.cuts[j][1]))
                except:
                    logging.warning("\033[91mERROR: Please be sure you have written the "+str(j+1)+"° cut in the right way in your config file\033[1;0m") 
                    sys.exit (1)
        
                
                #for every i element, the j>0 element is filled with the number of events after the j cut
                #(as said before j=0 is the element before the cut, so i apply j+1 to obtain j>0 always)
                self.counts[i][j+1] = self.dataframe[i].Count().GetValue()
                self.counts_w[i][j+1] = self.dataframe[i].Sum("weight").GetValue()
                
                #the j>0 element is filled with the sum of ALL the events of ALL the 'i' branches
                self.totalcounts.append(0)
                self.totalcounts_w.append(0)
                self.totalcounts[j+1]= self.totalcounts[j+1]+ self.counts[i][j+1]
                self.totalcounts_w[j+1]= self.totalcounts_w[j+1]+ self.counts_w[i][j+1]        

            
            
    def SetSNR(self, bkg ):
        """
        For every brach, the Signal / Background ratio is computed, considering every cut.
        In particular, every branch of signal is divided for ALL the branches of background.
        N.B.: as argument you can choose every kind of cutFlow istance, so be careful. 
        N.B.: be sure that bkg is a cutFlow instance and
              that the method bkg.SetCuts() was runned, otherwise the bkg.counts[] are not filled!        
        """
        
        #check if SetCut() were called before this method
        if (self.counts == []) :
            logging.warning("\033[91mERROR SetSNR(): The instance is not initialized. Please call SetCuts() before this method.\033[1;0m")
            sys.exit (1)
        
        
        #if the argument is not of a cutFlow type, then exit
        if not isinstance(bkg, cutFlow):
            logging.warning("\033[91mERROR SetSNR(): the argument of the method is not a cutFlow type\033[1;0m")
            sys.exit (1)
        
        #if bkg is a cutFlow type but not initialized, then exit
        if (bkg.counts == []) :
            logging.warning("\033[91mERROR SetSNR(): the argument of the method is not initialized. Please call SetCuts() method.\033[1;0m")
            sys.exit (1)
            
        #initialize arrays    
        self.SNR = []
        self.SNR_w = []
        
        #start S/B ratio
        for i in range(len(self.nameTree)): #for every branch
            #define element for the i-sh branch
            self.SNR.append([])
            self.SNR_w.append([])
            
            #for the i-sh branch element, define the j=0 element where the cuts are still not applied
             #(as said before j=0 is the element before the cut, so i apply j+1 to obtain j>0 always)
            self.SNR[i].append("")
            self.SNR[i][0] = (float (self.counts[i][0]) / float (bkg.totalcounts[0]))
            
            self.SNR_w[i].append("")
            self.SNR_w[i][0] = (float (self.counts_w[i][0]) / float (bkg.totalcounts_w[0]))
                  
            for j in range(len(self.cuts)): #for every cut
                #for the i-sh branch element, define the j>0 element and fill the S/B ratio after the j-sh cut is applied 
                self.SNR[i].append("")
                self.SNR[i][j+1] = (float(self.counts[i][j+1]) / float(bkg.totalcounts[j+1]))
                self.SNR_w[i].append("")
                self.SNR_w[i][j+1] = (float(self.counts_w[i][j+1]) / float(bkg.totalcounts_w[j+1]))
    
   
    
   
    def printTable (self, borderHorizontal = '-', borderVertical = '|', borderCross = '+'):
        """
        A method to stamp a text-table. It takes an array of n columns and m raws (self.table) and print all of them.
        
        """
        #takes all the colums from the table
        cols = [list(x) for x in zip(*self.table)]
        #define the orizontal lenght of every column as the lenght of the longest column
        lengths = [max(map(len, map(str, col))) for col in cols]
        
        #define the vertical border of the text-table
        f = borderVertical + borderVertical.join(' {:>%d} ' % l for l in lengths) + borderVertical
        
        #define the orizontal border
        s=borderCross
        for col in range(len(cols)):
            s = s + (borderHorizontal * (int(lengths[col])+2)) + borderCross          
        
        #print the table
        print(s)
        for row in self.table:
            print(f.format(*row))
            if (row == ["CUT", "FILTERED DATA", "WEIGHTED DATA"] or row == ["CUT", "S/B RATIO", "S/B WEIGHTED RATIO"]):
                print(s)      
        print(s)        
        print("\n\n")
    
    
    
    def GetCounts(self):
        """
        It stamps all the results of the counts of events of a given branch after every cut.
        The results are arranged in a text-table for a better read-out
        
        """
        
        #check if SetCut() were called before this method
        if (self.counts == []) :
            logging.warning("\033[91mERROR GetSNR(): The instance is not initialized. Please call SetCuts() before this method.\033[1;0m")
            sys.exit (1)


        
        print("--------------------------------------")
        print("From Tree: "+ self.inFileName);
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)): #for every branch
            print("\nTreeBranch: " + self.nameTree[i]);
            
            print("STARTING DATA: "+ str(self.counts[i][0]))
            print("STARTING WEIGHTED DATA: "+ str(self.counts_w[i][0])+"\n")
            
            self.table = []            
            self.table.append(["CUT", "FILTERED DATA", "WEIGHTED DATA"])
            
            #table with 3 columns and raws for every cut. Inside every raw there are  the values of the counts after each cut.
            for j in range(len(self.cuts)): #for every cut
                self.table.append([str(self.cuts[j][0]), str(self.counts[i][j+1]), str(self.counts_w[i][j+1])])
            
            self.printTable()        
        print("\n\n\n")
        
        #Feedback of the stamp on terminal
        logging.warning("Results of the cut of "+self.inFileName+" on "+ self.outFileName)
        



            


    def GetSNR(self, bkg):
        """
        It stamps all the results of the S/B ratio of after the cuts.
        The results are arranged in a text-table for a better read-out
        
        """
        
        #check if SetCut() and SetSNR() were called before this method
        if (self.counts == [] or self.SNR== []) :
            logging.warning("\033[91mERROR GetSNR(): The instance is not initialized. Please call SetCuts() and/or SetSNR() before this method.\033[1;0m")
            sys.exit (1)        
        
        #check if SetCut()  were called before this method for bkg
        if (bkg.counts == [] ) :
            logging.warning("\033[91mERROR GetSNR(): The argument is not initialized. Please call SetCuts() and/or SetSNR() before this method.\033[1;0m")
            sys.exit (1)  
        
        
        #the same of GetCounts() but it stamps S/B ratio rather than counts
        print("--------------------------------------")
        print("Signal / Background ratio from");
        print("S: "+ self.inFileName )
        print("B: "+ bkg.inFileName)
        print("--------------------------------------")
        
        for i in range(len(self.nameTree)): #for every branch
            print("\nTreeBranch: " + self.nameTree[i]);
            print("STARTING S/B RATIO :"+ str(self.SNR[i][0]) )
            print("STARTING WEIGHTED S/B RATIO :"+ str(self.SNR_w[i][0])+"\n" )   
                  
            self.table = []            
            self.table.append(["CUT", "S/B RATIO", "S/B WEIGHTED RATIO"])
           
            for j in range(len(self.cuts)):  #for every cut
                self.table.append([str(self.cuts[j][0]), str(self.SNR[i][j+1]),str(self.SNR_w[i][j+1]) ])               
            self.printTable()    
            
                       
        print("\n\n\n")  
        
        #Feedback of the stamp on terminal
        logging.warning("Results of the S/B ("+self.inFileName+" / "+ bkg.inFileName+" ) on "+ self.outFileName)









