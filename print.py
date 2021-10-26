#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:52:55 2021
@author: giacomo
"""

from cutflow import cutFlow
#import ROOT
import sys
import ast
import logging



"""The script runs over a file .root and asks for a config file"""
if len(sys.argv) != 2:
    print ("\033[91mPlease type:  %s <config file>\033[1;0m"%(sys.argv [0]))
    sys.exit (1)
config_file = sys.argv[1]

try:
    file = open(config_file, "r")
    contents = file.read()
    file.close()
except:
    logging.warning("\033[91mPlease insert an existing file\033[1;0m") 
    sys.exit (1)
    
try:
    dictionary = ast.literal_eval(contents)
except:
    logging.warning("\033[91mPlease insert the right config readable file with a dictionary variable inside.\033[1;0m") 
    sys.exit (1)



try:
    inFileName_sig = dictionary["inFileName_sig"]
    nameTree_sig = dictionary["nameTree_sig"]
    inFileName_bkg = dictionary["inFileName_bkg"]
    nameTree_bkg = dictionary["nameTree_bkg"]
    cuts = dictionary["cuts"]
    weight = dictionary["weight"]
    outFileName = dictionary["outFileName"]
except:
    logging.warning("\033[91mPlease insert the right dictionary variable with the following keys: \n ""inFileName_sig"" \n ""nameTree_sig"" \n ""inFileName_bkg"" \n ""nameTree_bkg"" \n ""cuts"" \n ""weight"" \n ""outFileName\033[1;0m") 
    sys.exit (1)

file = open (outFileName, 'w')
file.close()


sig = cutFlow(inFileName_sig, nameTree_sig, cuts, weight, outFileName  )
sig.SetCuts()
sig.GetCounts()


bkg = cutFlow(inFileName_bkg, nameTree_bkg, cuts, weight, outFileName )
bkg.SetCuts()
bkg.GetCounts()

sig.SetSNR(bkg)
sig.GetSNR(bkg)
