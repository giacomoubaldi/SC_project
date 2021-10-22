#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:52:55 2021

@author: giacomo
"""

from cutflow import cutFlow
from config import * 
import ROOT
import sys

outFile = open (outFileName, 'w')
outFile.close()


bkg = cutFlow(inFileName_bkg, nameTree_bkg, cuts, outFileName )
bkg.SetTree()
bkg.SetCuts()
bkg.SetTotalCounts()
bkg.GetCounts()




sig = cutFlow(inFileName_sig, nameTree_sig, cuts, outFileName  )
sig.SetTree()
sig.SetCuts()
#sig.SetTotalCounts()
sig.GetCounts()

sig.SetSNR(bkg)
sig.GetSNR(bkg)
