#This file contains a dictionary in which there are all the information a user has to set manually. It is done in order to make it simpler to change the input / output variables
#without making the user go directly inside the classes or the function scripts.



{
        #For signal:
        "inFileName_sig"    : "/home/ATLAS-T3/student-34/SC/ntuples_studenti/allTrees_signal_NoSys.root",           #name of .root dataset
        "nameTree_sig"      : ["C1N2_WZ_300_0_NoSys","C1N2_WZ_800_0_NoSys","C1C1_WW_1000_0_NoSys"],      #name of branches of the dataset I am interested in. 
                                                                #N.B.: it is a LIST of string even for just one value!
                                                                #N.B.: please be sure the names are correct!
                                                                #N.B.: do not insert free space -> the tmva_train() function is space sensitive
                                                                
#(I use a list of strings because in this way I can choose just one branch or more than one with the same structure in a dinamic way.) 
       
        #For background:
        "inFileName_bkg"    : "/home/ATLAS-T3/student-34/SC/ntuples_studenti/allTrees_bkg_NoSys.root",             #same specific and raccomandation as before
        "nameTree_bkg"      : ["multiboson_NoSys","diboson_NoSys","singletop_NoSys","ttbar_NoSys","tth_NoSys","ttv_NoSys","vh_NoSys","wjets_NoSys","zjets_NoSys"],

        #common cuts for the cutflow
            #N.B.: it is a LIST even for one cut
            #N.B.: every element of the list contains the name of the cuts and the commands
            #N.B.: the events would be filtered out one cut after the other, so be sure even about the disposition
            #N.B.: please be sure that every cut contains names of columns (variables) which are actually present in the database                  
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
        "outFileName"       : "results/cutflow_results_All.txt",
              
                   
                   
                   
                   
        #common outfile for TMVA analysis
        
        #variables for MVA; it's a LIST of string    
        #N.B.: do not insert free space -> the tmva_train() function is space sensitive   
        "TMVA_variable"     : ["nLep_base" , "nLep_signal" , "lep1Pt" , "nJet30" , "nBJet30_DL1" ,"met" , "met_Phi" ,"nFatjets" , "mt"],
        
        #cuts for signal events
        #N.B.: please be sure that it contains names of columns (variables) which are actually present in the database
        "TMVA_cut_sig"	  	: "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50",
        
        #cuts for bkg events
        "TMVA_cut_bkg"       : "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50",
        
        #output name of dataloader
        "TMVA_dataloader_name" : "results/TMVA_dataloader_All",
        
        #output name of ROC curve graph
        "TMVA_ROC_name" : 	"results/TMVA_ROC_Curve_All",
        
        #output name of TMVA analysis (it can be opened as  TMVA::TMVAGui("TMVAOutputCV.root")
        "TMVA_outFileName"  : "results/TMVA_Output_All" #.root


}


