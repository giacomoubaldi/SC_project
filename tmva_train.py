from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut, TMVA


#TMVA.Tools.Instance()
#TMVA.PyMethodBase.PyInitialize()



def my_tmva(inFileName_sig, nameTree_sig, inFileName_bkg, nameTree_bkg, TMVA_variable, TMVA_cut_sig, TMVA_cut_bkg, TMVA_outFileName ):
	
	#------------------
	#declare Factory

	inputFile_signal = TFile.Open(inFileName_sig)
	inputFile_bkg = TFile.Open(inFileName_bkg)

	outputFile = TFile.Open( "outTMVA.root", 'RECREATE' )

	factory = TMVA.Factory( "TMVAClassification", outputFile, "!V:ROC:!Correlations:!Silent:Color:"
	"!DrawProgressBar:AnalysisType=Classification" )

	#declare DataLoader
	dataloader = TMVA.DataLoader('dataset')

	#Define the input variables that shall be used for the classifier training      #CONTROL OF THE NAMES
	for keys in TMVA_variable :
		dataloader.AddVariable(keys, 'F' )

	#Set up Dataset
	signal = inputFile_signal.Get('C1N2_WZ_300_0_NoSys')

	for keys in nameTree_bkg :
		background = inputFile_bkg.Get(keys)

	dataloader.AddSignalTree(signal, 1.0)
	dataloader.AddBackgroundTree(background, 1.0)

	#Apply additional cuts on the signal and background samples (can be different)
	#TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
	#TCut mycutb = "";
	mycuts = TMVA_cut_sig
	mycutb = TMVA_cut_bkg



	# Tell the dataloader how to use the trainig and testing events:
	# If no specifications, half of the events in the tree are used for training,
	# half for testing

	dataloader.PrepareTrainingAndTestTree(mycuts,mycutb,"NTrain_Signal=0:NTrain_Background=0:NTest_Signal=0:NTest_Background=0")


	#-----------------
	#Book the methods -- MLP
	factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )
	#H:!V:HiddenLayers=3


	# Train MVAs
	factory.TrainAllMethods()
    
	# Test MVAs
	factory.TestAllMethods()
    
	# Evaluate MVAs
	factory.EvaluateAllMethods()    


	#-------------------
	#Plot ROC Curve
	factory.GetROCCurve(dataloader).Draw()

    
	# Save the output.
	outputFile.Close()
    
	print ("=== wrote root file %s\n" )
	print ("=== TMVAClassification is done!\n")
    
	# open the GUI for the result macros    
	#gROOT.ProcessLine( "TMVA::TMVAGui(\"outTMVA.root\")" )

	# keep the ROOT thread running
	gApplication.Run() 



#TMVA_variable =   ["nLep_base" , "nLep_signal" , "lep1Pt" , "nJet30" , "nBJet30_DL1" ," met" , "met_Phi" ,"nFatjets" , "mt"]
#my_tmva("signal_Demo.root", 'C1N2_WZ_300_0_NoSys', "bkg2_Demo.root", 'multiboson_NoSys', TMVA_variable , "", "", "a")




 

