#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>

using std::cout; using std::cerr;
using std::endl; using std::string;
using std::ifstream; using std::ostringstream;
using std::istringstream;



string readFileIntoString(const string& path) {
    auto ss = ostringstream{};
    ifstream input_file(path);
    if (!input_file.is_open()) {
        cerr << "Could not open the file - '"
             << path << "'" << endl;
        exit(EXIT_FAILURE);
    }
    ss << input_file.rdbuf();
    return ss.str();
}




void Config(string& inFileName_sig, string&  inFileName_bkg, string&  TMVA_outFileName, string&  TMVA_cutsig, string& TMVA_cutbkg
,string *& TMVA_variable ,string *& nameTree_sig, string *& nameTree_bkg
)
{

    string filename("dict_file.csv");
    string file_contents;
    std::map<int, std::vector<string>> csv_contents;
    char delimiter = ',';

    file_contents = readFileIntoString(filename);

    istringstream sstream(file_contents);
    std::vector<string> items;
    string record;

    int counter = 0;
    while (std::getline(sstream, record)) {
        istringstream line(record);
       
        while (std::getline(line, record, delimiter)) {
            items.push_back(record);
        }


        csv_contents[counter] = items;
        //cout << items.size()<<" ";
        
        for (int i= 0; i<items.size(); i++)  {
        //delete the char [ ] ' " ( ) from records
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), '"'), csv_contents[counter][i].end());
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), '\''), csv_contents[counter][i].end());
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), '['), csv_contents[counter][i].end());
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), ']'), csv_contents[counter][i].end());
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), '('), csv_contents[counter][i].end());
        csv_contents[counter][i].erase(std::remove(csv_contents[counter][i].begin(), csv_contents[counter][i].end(), ')'), csv_contents[counter][i].end());
        
        }
        
               
        items.clear();
        counter += 1;
    }


   
    
    	inFileName_sig = csv_contents[0][1];
    	inFileName_bkg = csv_contents[2][1];
     	TMVA_outFileName = csv_contents[10][1];
     	TMVA_cutsig = csv_contents[8][1];
     	TMVA_cutbkg = csv_contents[9][1];
     	
     	
     	delete[] TMVA_variable;
     	delete[] nameTree_sig;
     	delete[] nameTree_bkg;
     	
     	TMVA_variable = new string [csv_contents[7].size()-1];
     	for (int i=1; i< (csv_contents[7].size()); i++) {
     	TMVA_variable[i-1] = csv_contents[7][i];
     	}
     	
     	nameTree_sig = new string [csv_contents[1].size()-1];
     	for (int i=1; i< (csv_contents[1].size()); i++) {
     	nameTree_sig[i-1] = csv_contents[1][i];
     	}
     	
     	nameTree_bkg = new string [csv_contents[3].size()-1];
     	for (int i=1; i< (csv_contents[3].size()); i++) {
     	nameTree_bkg[i-1] = csv_contents[3][i];
     	}
   
    	
    }







//DELETE ARRAY!




void tmva_train()
{

//--------------
//Take value from config file
string inFileName_sig;
string inFileName_bkg;
string TMVA_outFileName;
string TMVA_cutsig;
string TMVA_cutbkg;
string * TMVA_variable = new string[1];
string *nameTree_sig;
string *nameTree_bkg;
Config(inFileName_sig, inFileName_bkg, TMVA_outFileName, TMVA_cutsig, TMVA_cutbkg, TMVA_variable , nameTree_sig, nameTree_bkg);



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
TCut mycuts = "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50";
TCut mycutb = "met>100&&nJet25>=1&&nLep_base<=2&&nLep_signal<=2&&mt>50";


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





