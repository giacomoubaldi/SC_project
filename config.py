#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:46:10 2021
@author: giacomo
"""





#file .root for the signal and the branches i am interested in

inFileName_sig = "signal_Demo.root"

nameTree_sig = ["C1N2_WZ_300_0_NoSys"]


#file .root for the background and the branches i am interested in

inFileName_bkg = "bkg2_Demo.root"

nameTree_bkg = ["multiboson_NoSys"]



#common cuts for the cutflow

cuts = [
          ("Preselection 1 lepton, $E_\mathrm{T}^\mathrm{miss} > $ 150 GeV, $N_\mathrm{jet30} = $ 2-3, $m_{\mathrm{T}}$ $>$ 50 GeV", "trigMatch_metTrig&&met>150&&nJet30>=2&&nJet30<4&&nLep_base==1&&nLep_signal==1&&mt>50"),
          ("$N_{\mathrm{b-jets,30}} =$ 2", "nBJet30_DL1==2"),
          ("$m_{\mathrm{bb}}$ $>$ 50 GeV", "mbb>50"),
          ("105 $<$ $m_{\mathrm{bb}}$ $<$ 135 GeV", "mbb>105&&mbb<135"),
          ("$m_{\mathrm{CT}}$ $>$ 160 GeV", "mct>160"),
          ("$E_\mathrm{T}^\mathrm{miss} > $ 200 GeV", "met>200"),
           #("met>200", "met > 200"),
        ]


weight = "genWeight*eventWeight*pileupWeight*leptonWeight*bTagWeight"
#weight = "1"



#common outfile for the read out

outFileName = "provaw.txt"