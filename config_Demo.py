
{
        #For signal:
        "inFileName_sig"    : "signal_Demo.root",           #name of .root dataset
        "nameTree_sig"      : ["C1N2_WZ_300_0_NoSys"],      #name of branches of the dataset I am interested in. 
                                                                #N.B.: it is a LIST of string even for just one value!
                                                                #N.B.: please be sure the names are correct!
        #For background:
        "inFileName_bkg"    : "bkg2_Demo.root",             #same specific and raccomandation as before
        "nameTree_bkg"      : ["multiboson_NoSys"],

        #common cuts for the cutflow
            #N.B.: it is a LIST even for one cut
            #N.B.: every element of the list contains the name of the cuts and the commands
            #N.B.: the events would be filtered out one cut after the other, so be sure even about the disposition
            #N.B.: please be sure that every cut contains names of columns which are actually present in the database! 
            #N.B.: don't use COMMAS in your titles!       
        "cuts"              : [
          ("Preselection 1 lepton - $E_\mathrm{T}^\mathrm{miss} > $ 150 GeV - $N_\mathrm{jet30} = $ 2-3, $m_{\mathrm{T}}$ $>$ 50 GeV", "trigMatch_metTrig&&met>150&&nJet30>=2&&nJet30<4&&nLep_base==1&&nLep_signal==1&&mt>50"),
          ("$N_{\mathrm{b-jets,30}} =$ 2", "nBJet30_DL1==2"),
          ("$m_{\mathrm{bb}}$ $>$ 50 GeV", "mbb>50"),
          ("105 $<$ $m_{\mathrm{bb}}$ $<$ 135 GeV", "mbb>105&&mbb<135"),
          ("$m_{\mathrm{CT}}$ $>$ 160 GeV", "mct>160"),
          ("$E_\mathrm{T}^\mathrm{miss} > $ 200 GeV", "met>200"),
           #("met>200", "met > 200"),
        ],

        #common weight for data
            #N.B.: it is JUST a string
            #N.B.: please be sure that it contains names of columns which are actually present in the database!            
        "weight"            : "genWeight*eventWeight*pileupWeight*leptonWeight*bTagWeight",
        
        #common outfile for the read out
            #N.B.: everytime you run the program, the output file would be rewashed
        "outFileName"       : "results_Demo.txt",
        
        
        #common outfile for TMVA analysis
                    
        "TMVA_variable"     : ["nLep_base" , "nLep_signal" , "lep1Pt" , "nJet30" , "nBJet30_DL1" ," met" , "met_Phi" ,"nFatjets" , "mt"],
        
        "TMVA_cut_sig"	     : "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50",
        
        "TMVA_cut_bkg"       : "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50",
        
        "TMVA_outFileName"  : "TMVAOutput_demo" #.root


}


