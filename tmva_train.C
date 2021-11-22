#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>


using namespace std;


void SplitString(string s, vector<string> &v){
//method to convert a string into a vector<string>: every time it finds a space, it splits the string in new elements
	string temp = "";
	for(int i=0;i<s.length();++i){
		
		if(s[i]==' '){
			v.push_back(temp);
			temp = "";
		}
		else{
			temp.push_back(s[i]);
		}
		
	}
	v.push_back(temp);
	
}



void tmva_train(string inFileName_sig, string nameTree_sig_string, string inFileName_bkg, string nameTree_bkg_string,  string TMVA_variable_string , string TMVA_cut_sig, string TMVA_cut_bkg, string TMVA_dataloader_name, string TMVA_ROC_name, string TMVA_outFileName)
{
// TMVA multivariate analysis 
//this function opens .root signal and background datasets and starts a multivariate analysis based on variables given as input. Once the methods to be used are booked, the MVA is trained and tested. The results are the weight of the variables for an efficient MVA (according to the choosen methods) and the ROC curve.

//As written in print.py file, the conversion from python list(string) to c++ vector<string> does not work well for every version of python. So, what I have done was to convert (in .py script) a list into a simple string before calling tmva_train.C function and now, once I am inside this function in c++ enviroment,
//I go back from string to vector<string>  using SplitString function
vector <string> nameTree_sig;
vector <string> nameTree_bkg;
vector <string> TMVA_variable;

SplitString(nameTree_sig_string, nameTree_sig);
SplitString(nameTree_bkg_string, nameTree_bkg);
SplitString(TMVA_variable_string, TMVA_variable);


//initialization of the .root files to open
auto inputFile_signal = TFile::Open(inFileName_sig.c_str());
auto inputFile_bkg = TFile::Open(inFileName_bkg.c_str());

//some initializations.
// N.B.: rather than Factory, DataLoader, TTree etc variables, I use a vector of them: I have to initialize new ones for every branch of my dataset and, since I don't know a priori how many branches I have,
// I cannot use just one variable nor arrays (because for arrays I have to initialize the size once for all). So I use vectors
vector<TFile*> 	outputfile;
vector<TMVA::Factory*>	factory;
vector<TMVA::DataLoader*>	dataloader;
vector<TTree*>	signal;
vector<TTree*>	bkg;
vector<TCanvas*>	canvas;
string title = "";
string name = "";
	

for (int i = 0; i < nameTree_sig.size(); i++){  // for every branch of the signal	
	 
	 title = TMVA_outFileName + "_"+nameTree_sig[i]+"_"+to_string(i)+".root";
	 //create an output file element
	 outputfile.push_back (TFile::Open(title.c_str(), "RECREATE"));
	 
	//declare Factory element in my vector 	  
	 factory.push_back (new TMVA::Factory("TMVAClassification", outputfile[i],
	"!V:ROC:!Correlations:!Silent:Color:"
	"!DrawProgressBar:AnalysisType=Classification"));
	
	//declare dataloader element
	title = TMVA_dataloader_name+"_"+nameTree_sig[i]+"_"+to_string(i);
        dataloader.push_back( new TMVA::DataLoader (title.c_str()));
        
        //Define the input variables that shall be used for the classifier training      //control of the names comes after      
        for (string keys : TMVA_variable) {
        		dataloader[i]->AddVariable(keys, 'F' );
			}
        
        
        
        
        //Set up Dataloader element
        signal.push_back(new TTree());
        inputFile_signal->GetObject(nameTree_sig[i].c_str(), signal[i]);
        
        //add signal tree
	dataloader[i] -> AddSignalTree(signal[i], 1.0);
	
	for (int j = 0; j < nameTree_bkg.size(); j++){  // for every branch of the bkg
		bkg.push_back(new TTree());
		inputFile_bkg->GetObject(nameTree_bkg[j].c_str(), bkg[j]);
		// add background tree
		dataloader[i] -> AddBackgroundTree(bkg[j], 1.0);
	
	// N.B: a dataloader[i] contains 1 signal branch and ALL bkg branches
	}
	

	//Apply additional cuts on the signal and background samples (can be different)
	//TCut mycuts = "";  // es. "abs(var1)< 0.5 && ..."
	//TCut mycutb = "";
	TCut mycuts = TMVA_cut_sig.c_str();
	TCut mycutb = TMVA_cut_bkg.c_str();

	
	//Tell the dataloader element how to use the trainig and testing events:
	//If no specifications, half of the events in the tree are used for training,
	//half for testing
	dataloader[i]->PrepareTrainingAndTestTree(mycuts,mycutb,"NTrain_Signal=0:NTrain_Background=0:NTest_Signal=0:NTest_Background=0");


	//-----------------
	//Book the methods for every factory element
	
	// Multi-Layer Perceptron (Neural Network)
	factory[i]->BookMethod(dataloader[i], TMVA::Types::kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );
	//H:!V:HiddenLayers=3


	// Boosted Decision Trees
	factory[i]->BookMethod(dataloader[i], TMVA::Types::kBDT, "BDT","!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=2:BoostType=AdaBoost:"
	"AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:"
	"SeparationType=GiniIndex:nCuts=20");

	
	
	
	//Train MVAs for factory element
	// If the name of the variables given for the training are bad written, then go to error
	try
  	{
	factory[i]->TrainAllMethods();		
	}
	
	catch (...) {
	cout << "WARNING:root:\033[91mError TMVA analysis: Please be sure:\n \"TMVA_variable\" contains the right name of attributes you want to add to the dataloader \n \"my_cutsb\" or \"my_cutsa\" contains the right name of cuts you want to add  \n \033[1;0m"<<endl;
	
	}
	
	
	//Test MVAs for factory element
	factory[i]->TestAllMethods();
    
	//Evaluate MVAs
	factory[i]->EvaluateAllMethods()  ;



	//-------------------
	//Plot ROC Curve for every signal branch
	canvas.push_back(factory[i]->GetROCCurve(dataloader[i]));
	canvas[i]->Draw("Same");
	name=TMVA_ROC_name+"_"+nameTree_sig[i]+"_"+to_string(i)+".png";
	canvas[i]->SaveAs(name.c_str());
		
    
	// Save the output.
	outputfile[i]->Close();
}


for (string branch : nameTree_sig) {
	cout<<"=== written root file and stamped ROC Curve for signal "<< branch.c_str()<<endl;;	
}
cout << "\n\n=== TMVAClassification is done!\n";
//exit(EXIT_SUCCESS);
}

//to run output file via root:
// TMVA::TMVAGui("TMVAOutput_name.root")


