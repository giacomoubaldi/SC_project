from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut, TMVA, TCanvas

import sys
import logging

#TMVA.Tools.Instance()
#TMVA.PyMethodBase.PyInitialize()



##SAY WHY NOT CONTROLL ON THE OTHER VARIABLES

def my_tmva(inFileName_sig, nameTree_sig, inFileName_bkg, nameTree_bkg, TMVA_variable, TMVA_cut_sig, TMVA_cut_bkg, TMVA_outFileName ):
	
	#------------------
	#declare Factory

	inputFile_signal = TFile.Open(inFileName_sig)
	inputFile_bkg = TFile.Open(inFileName_bkg)
	
	outputFile = []
	factory = []
	dataloader = []
	signal = []
	canvas = []
	
	for i in range(len(nameTree_sig)):
		
		title= TMVA_outFileName+"_"+nameTree_sig[i]+".root"
		
		outputFile.append(TFile.Open( title, 'RECREATE' ))
	
	
		factory.append(TMVA.Factory( "TMVAClassification", outputFile[i], "!V:ROC:!Correlations:!Silent:Color:"
		"!DrawProgressBar:AnalysisType=Classification" ))
	
	
	
		#declare DataLoader
		dataloader.append(TMVA.DataLoader('dataset'))

		#Define the input variables that shall be used for the classifier training      #CONTROL OF THE NAMES
		for keys in TMVA_variable :
			dataloader[i].AddVariable(keys, 'F' )
		
		
	
		#Set up Dataset
		signal.append(inputFile_signal.Get(nameTree_sig[i]))
	
		
		
	for keys in nameTree_bkg :
		background = inputFile_bkg.Get(keys)

		
		
	for i in range(len(nameTree_sig)):
		dataloader[i].AddSignalTree(signal[i], 1.0)
		dataloader[i].AddBackgroundTree(background, 1.0)

		#Apply additional cuts on the signal and background samples (can be different)
		#TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
		#TCut mycutb = "";
		mycuts = TMVA_cut_sig
		mycutb = TMVA_cut_bkg



		# Tell the dataloader how to use the trainig and testing events:
		# If no specifications, half of the events in the tree are used for training,
		# half for testing

		dataloader[i].PrepareTrainingAndTestTree(mycuts,mycutb,"NTrain_Signal=0:NTrain_Background=0:NTest_Signal=0:NTest_Background=0")


		#-----------------
		#Book the methods -- MLP
		factory[i].BookMethod(dataloader[i], TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )
		#H:!V:HiddenLayers=3

		exit();
		
		# Train MVAs
		#errors concerning wrong name of variables for the MVA and cuts are found here
		try:
			factory[i].TrainAllMethods()
	
		except Exception, e:
		
			#print 'type is:', e.__class__.__name__
    			if (e.__class__.__name__ == "runtime_error"):
    				logging.warning("\033[91mError TMVA analysis: Please be sure:\n \"TMVA_variable\" contains the right name of attributes you want to add to the dataloader \n \"my_cutsb\" or \"my_cutsa\" contains the right name of cuts you want to add  \n \033[1;0m")
    				# print "exception happened!"
                
                		sys.exit (1)
		
    
		# Test MVAs
		factory[i].TestAllMethods()
    
		# Evaluate MVAs
		factory[i].EvaluateAllMethods()    


		#-------------------
		#Plot ROC Curve
		
		canvas.append(factory[i].GetROCCurve(dataloader[i]))
		canvas[i].Draw("Same")
		name= nameTree_sig[i]+"_"+str(i)+"_ROC_Curve"+".png"
		canvas[i].SaveAs(name)
		
    
		# Save the output.
		outputFile[i].Close()
 		
 		#print ("=== wrote root file for signal "+ nameTree_sig[i])
 	
 	
 	
 	for branch in nameTree_sig:
		print ("=== wrote root file and stamped ROC Curve for signal "+ branch)
	print ("=== TMVAClassification is done!\n")
	
    
	# open the GUI for the result macros    
	#gROOT.ProcessLine( "TMVA::TMVAGui(\"outTMVA.root\")" )

	# keep the ROOT thread running
	#gApplication.Run() 


#nameTree_bkg =       ["multiboson_NoSys"]
#nameTree_sig=        ["C1N2_WZ_300_0_NoSys","C1N2_WZ_300_0_NoSys"]
#TMVA_variable =   ["nLep_base" , "nLep_signal" , "lep1Pt" , "nJet30" , "nBJet30_DL1" ," met" , "met_Phi" ,"nFatjets" , "mt"]
#TMVA_cut_bkg = "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50"
#my_tmva("signal_Demo.root", nameTree_sig, "bkg2_Demo.root", nameTree_bkg, TMVA_variable , "", TMVA_cut_bkg, "TMVAOutput_demo")
