void tmva_train()
{
//-------------------
//declare Factory

auto inputFile_signal = TFile::Open("signal_Demo.root");
auto inputFile_bkg = TFile::Open("bkg2_Demo.root");

auto outputFile = TFile::Open("TMVAOutputCV.root", "RECREATE");

TMVA::Factory factory("TMVAClassification", outputFile,
"!V:ROC:!Correlations:!Silent:Color:"
"!DrawProgressBar:AnalysisType=Classification");





//-------------------
//declare DataLoader

TMVA::DataLoader loader("dataset");


loader.AddVariable("nLep_base");
loader.AddVariable("nLep_signal");
loader.AddVariable("lep1Pt");
loader.AddVariable("nJet30");
loader.AddVariable("nBJet30_DL1");
loader.AddVariable("met");
loader.AddVariable("met_Phi");
loader.AddVariable("nFatjets");
loader.AddVariable("mt");


//-------------------
//Set up Dataset (code example 9 of user guide)

TTree* tsignal;
TTree* tbackground;
inputFile_signal->GetObject("C1N2_WZ_300_0_NoSys", tsignal);
inputFile_bkg->GetObject("multiboson_NoSys", tbackground);


loader.AddSignalTree(tsignal, 1.0);
loader.AddBackgroundTree(tbackground, 1.0);




//Apply additional cuts on the signal and background samples (can be different)
//TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
//TCut mycutb = "";
TCut mycuts = "met>100 && nJet25>=1 && nLep_base<=2 && nLep_signal<=2 && mt>50";
TCut mycutb = "met>100 && nJet25>=1 && nLep_base<=2 && nLep_signal<=2 && mt>50";


// Tell the dataloader how to use the trainig and testing events:
// If no specifications, half of the events in the tree are used for training,
// half for testing

loader.PrepareTrainingAndTestTree(mycuts, mycutb,"NTrain_Signal=0:NTrain_Background=0:NTest_Signal=0:NTest_Background=0");

//SplitMode=random:!V

//-----------------
//Book the methods

factory.BookMethod( &loader, TMVA::Types::kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );

//H:!V:HiddenLayers=3


//-------------------
//Train methods

factory.TrainAllMethods();







//-------------------
//Test and Evaluate Methods

factory.TestAllMethods();
factory.EvaluateAllMethods();


//-------------------
//Plot ROC Curve
auto c1 = factory.GetROCCurve(&loader);
c1->Draw();


//-------------------
// Save the output
outputFile->Close();
}

//to run via root: root -l tmva_train.C 
// TMVA::TMVAGui("TMVAOutputCV.root")





