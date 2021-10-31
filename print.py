#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:52:55 2021
@author: giacomo
"""

from cutflow import cutFlow
from tmva_train import my_tmva


#import ROOT
import sys
import ast
import logging
#import pandas as pd

import os
import subprocess





#---------------------------------
#Ask to call Cutflow and TMVA
answer=''
while( not (answer == "y" or answer == "yes" or answer == "n" or answer == "no" )):
	print( " Do you want to run the Multivariate Data analysys? y/n ")
	answer = raw_input()

if (answer == "n" or answer == "no"):
	tmva_call =False
elif (answer == "y" or answer == "yes"):
 	tmva_call = True





#----------------------
#Parsing and controll of the config file


#The script runs over a file .root and asks for a config file
#If no 1 arg is given, then exit
if len(sys.argv) != 2:
    print ("\033[91mPlease type:  %s <config file>\033[1;0m"%(sys.argv [0]))
    sys.exit (1)
config_file = sys.argv[1]

#If the arg is not a real file, then exit
try:
    file = open(config_file, "r")
    contents = file.read()
    file.close()
except:
    logging.warning("\033[91mPlease insert an existing file\033[1;0m") 
    sys.exit (1)

#If the file does not contain a dictionary variable, then exit  
try:
    dictionary = ast.literal_eval(contents)
except:
    logging.warning("\033[91mPlease insert the right config readable file with a dictionary variable inside.\033[1;0m") 
    sys.exit (1)


#If the file does not contain a dictionary variable with the needed keys, then exit 
try:
    inFileName_sig = dictionary["inFileName_sig"]
    nameTree_sig = dictionary["nameTree_sig"]
    inFileName_bkg = dictionary["inFileName_bkg"]
    nameTree_bkg = dictionary["nameTree_bkg"]
    cuts = dictionary["cuts"]
    weight = dictionary["weight"]
    outFileName = dictionary["outFileName"]
    if (tmva_call == True):		#control the keys needed by tmva analysys only if it would be called
    	TMVA_variable = dictionary["TMVA_variable"]
    	TMVA_cut_sig = dictionary["TMVA_cut_sig"]
    	TMVA_cut_bkg = dictionary["TMVA_cut_bkg"]
    	TMVA_outFileName = dictionary["TMVA_outFileName"]
    
except:
    logging.warning("\033[91mPlease insert the right dictionary variable with the following keys: \n ""inFileName_sig"" \n ""nameTree_sig"" \n ""inFileName_bkg"" \n ""nameTree_bkg"" \n ""cuts"" \n ""weight"" \n ""outFileName\033[1;0m") 
    if (tmva_call == True): #if TMVA would be called
    	logging.warning("\033[91m For TMVA: \n \"TMVA_variable\" \n \"TMVA_cut_sig\" \n \"TMVA_cut_bkg\" \n \"TMVA_outFileName\"\033[1;0m")
    sys.exit (1)





#--------------
#Run the cutflow


#Open the output file in order to cancell all the previous data
file = open (outFileName, 'w')
file.close()

#make all the print() to stamp on the file 'outFileName' rather than on terminal
holder = sys.stdout
sys.stdout = open(outFileName,'a')

#Create the istance of signal, set and print the cutflow
sig = cutFlow(inFileName_sig, nameTree_sig, cuts, weight, outFileName  )
sig.SetCuts()
sig.GetCounts()

#Create the istance of background, set and print the cutflow
bkg = cutFlow(inFileName_bkg, nameTree_bkg, cuts, weight, outFileName )
bkg.SetCuts()
bkg.GetCounts()

#Set and print the S/B ratio between signal and background
sig.SetSNR(bkg)
sig.GetSNR(bkg)

#print back on terminal
sys.stdout = holder





#--------
#Run the Multi Variate Analysys 

if (tmva_call == True):
	print( "Push ENTER to start TMVA analysis")
	raw_input()
	my_tmva(inFileName_sig, 'C1N2_WZ_300_0_NoSys', inFileName_bkg, nameTree_bkg, TMVA_variable , TMVA_cut_sig, TMVA_cut_bkg, "a")





