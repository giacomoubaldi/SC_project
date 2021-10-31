from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut, TMVA


#TMVA.Tools.Instance()
#TMVA.PyMethodBase.PyInitialize()


#------------------
#declare Factory

inputFile_signal = TFile.Open("signal_Demo.root")
inputFile_bkg = TFile.Open("bkg2_Demo.root")

outputFile = TFile.Open( "outTMVA.root", 'RECREATE' )

factory = TMVA.Factory( "TMVAClassification", outputFile, "!V:ROC:!Correlations:!Silent:Color:"
"!DrawProgressBar:AnalysisType=Classification" )

#declare DataLoader
dataloader = TMVA.DataLoader('dataset')

#Define the input variables that shall be used for the classifier training
dataloader.AddVariable("nLep_base", 'F' )
dataloader.AddVariable("nLep_signal", 'F' )
dataloader.AddVariable("lep1Pt", 'F' )
dataloader.AddVariable("nJet30")
dataloader.AddVariable("nBJet30_DL1")
dataloader.AddVariable("met")
dataloader.AddVariable("met_Phi")
dataloader.AddVariable("nFatjets")
dataloader.AddVariable("mt")

#Set up Dataset
signal = inputFile_signal.Get('C1N2_WZ_300_0_NoSys')
background = inputFile_bkg.Get('multiboson_NoSys')

dataloader.AddSignalTree(signal, 1.0)
dataloader.AddBackgroundTree(background, 1.0)

#Apply additional cuts on the signal and background samples (can be different)
#TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
#TCut mycutb = "";
mycuts = "met>100 && nJet25>=1 && nLep_base<=2 && nLep_signal<=2 && mt>50"
mycutb = "met>100 && nJet25>=1 && nLep_base<=2 && nLep_signal<=2 && mt>50"



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



