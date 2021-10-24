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




"""The script runs over a file .root and asks for a config file"""
if len(sys.argv) != 2:
    print ("USAGE: %s <config file>"%(sys.argv [0]))
    sys.exit (1)
config_file = sys.argv[1]


file = open(config_file, "r")
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()

inFileName_sig = dictionary["inFileName_sig"]
nameTree_sig = dictionary["nameTree_sig"]
inFileName_bkg = dictionary["inFileName_bkg"]
nameTree_bkg = dictionary["nameTree_bkg"]
cuts = dictionary["cuts"]
weight = dictionary["weight"]
outFileName = dictionary["outFileName"]


file = open (outFileName, 'w')
file.close()


sig = cutFlow(inFileName_sig, nameTree_sig, cuts, weight, outFileName  )
sig.SetAllCuts()
sig.GetCounts()


bkg = cutFlow(inFileName_bkg, nameTree_bkg, cuts, weight, outFileName )
bkg.SetAllCuts()
bkg.GetCounts()

sig.SetSNR(bkg)
sig.GetSNR(bkg)
