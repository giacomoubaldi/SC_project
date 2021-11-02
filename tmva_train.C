#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>


using namespace std;


//DELETE ARRAY!
// remember the check of keys in config_demo if wants even tmva 




void tmva_train(string inFileName_sig, vector <string> nameTree_sig, string inFileName_bkg, vector <string> nameTree_bkg,  vector <string> TMVA_variable , string TMVA_cut_sig, string TMVA_cut_bkg, string TMVA_outFileName)
{







//-------------------



auto inputFile_signal = TFile::Open(inFileName_sig.c_str());
auto inputFile_bkg = TFile::Open(inFileName_bkg.c_str());

vector<TFile*> 	outputfile;
vector<TMVA::Factory*>	factory;
vector<TMVA::DataLoader*>	dataloader;
vector<TTree*>	signal;
vector<TTree*>	bkg;
vector<TCanvas*>	canvas;
string title = "";
string name = "";
	


/*
for (string x : TMVA_variable) 
        cout << x << " ";
*/



for (int i = 0; i < nameTree_sig.size(); i++){
	
	 //cout << nameTree_sig[i] << " ";
	 title = TMVA_outFileName + "_"+nameTree_sig[i]+"_"+to_string(i)+".root";
	 outputfile.push_back (TFile::Open(title.c_str(), "RECREATE"));
	 
	//declare Factory 	 
	 factory.push_back (new TMVA::Factory("TMVAClassification", outputfile[i],
	"!V:ROC:!Correlations:!Silent:Color:"
	"!DrawProgressBar:AnalysisType=Classification"));
	
	//declare dataloader
	title = "dataset_signal_"+nameTree_sig[i]+"_"+to_string(i);
         dataloader.push_back( new TMVA::DataLoader (title.c_str()));
        
        //Define the input variables that shall be used for the classifier training      #CONTROL OF THE NAMES        
        for (string keys : TMVA_variable) {
        		//cout << keys << endl;
			dataloader[i]->AddVariable(keys, 'F' );
			}
        
        
        
        
        //#Set up Dataloader
        signal.push_back(new TTree());
        inputFile_signal->GetObject(nameTree_sig[i].c_str(), signal[i]);
        
	dataloader[i] -> AddSignalTree(signal[i], 1.0);
	
	for (int j = 0; j < nameTree_bkg.size(); j++){
		bkg.push_back(new TTree());
		inputFile_bkg->GetObject(nameTree_bkg[j].c_str(), bkg[j]);
		dataloader[i] -> AddBackgroundTree(bkg[j], 1.0);
	}


	//Apply additional cuts on the signal and background samples (can be different)
	//TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
	//TCut mycutb = "";
	TCut mycuts = TMVA_cut_sig.c_str();
	TCut mycutb = TMVA_cut_bkg.c_str();

	
	//Tell the dataloader how to use the trainig and testing events:
		//If no specifications, half of the events in the tree are used for training,
		//half for testing

	dataloader[i]->PrepareTrainingAndTestTree(mycuts,mycutb,"NTrain_Signal=0:NTrain_Background=0:NTest_Signal=0:NTest_Background=0");


	//-----------------
	//Book the methods -- MLP
	factory[i]->BookMethod(dataloader[i], TMVA::Types::kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );
	//H:!V:HiddenLayers=3


	//Train MVAs
	factory[i]->TrainAllMethods();
	
	//Test MVAs
	factory[i]->TestAllMethods();
    
	//Evaluate MVAs
	factory[i]->EvaluateAllMethods()  ;



	//-------------------
	//Plot ROC Curve
		
	canvas.push_back(factory[i]->GetROCCurve(dataloader[i]));
	canvas[i]->Draw("Same");
	name= nameTree_sig[i]+"_"+to_string(i)+"_ROC_Curve"+".png";
	canvas[i]->SaveAs(name.c_str());
		
    
	// Save the output.
	outputfile[i]->Close();
}


for (string branch : nameTree_sig) {

	cout<<"=== wrote root file and stamped ROC Curve for signal "<< branch.c_str();
	
}
cout << "=== TMVAClassification is done!\n";
//exit(EXIT_SUCCESS);
}

//to run via root: root -l tmva_train.C 
// TMVA::TMVAGui("TMVAOutputCV.root")


