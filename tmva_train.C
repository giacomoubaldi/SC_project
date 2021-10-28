#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>


using namespace std;



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
,string *& TMVA_variable ,string *& nameTree_sig, string *& nameTree_bkg, int& length_TMVA_variable,int& length_nameTree_sig,int& length_nameTree_bkg
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

    // inizialization of the map vector csv_contents which takes all the keys of my config file
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


   	// inizialitazion of the config variables I will use on TMVA function
    
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
     	//cout << csv_contents[7].size()<<endl;
     	TMVA_variable[i-1] = csv_contents[7][i];
     	//cout << TMVA_variable[i-1] << endl;
     	}
     	length_TMVA_variable= (csv_contents[7].size()-1);
     	     	
     	
     	nameTree_sig = new string [csv_contents[1].size()-1];
     	for (int i=1; i< (csv_contents[1].size()); i++) {
     	
     	nameTree_sig[i-1] = csv_contents[1][i];
     	}
     	length_nameTree_sig= (csv_contents[1].size()-1);
     	
     	
     	nameTree_bkg = new string [csv_contents[3].size()-1];
     	for (int i=1; i< (csv_contents[3].size()); i++) {
     	nameTree_bkg[i-1] = csv_contents[3][i];
     	}
   	length_nameTree_bkg = (csv_contents[3].size()-1);
    	
    }







//DELETE ARRAY!
// remember the check of keys in config_demo if wants even tmva 



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
string *nameTree_sig = new string[1];
string *nameTree_bkg = new string[1];
int length_TMVA_variable = 0;
int length_nameTree_sig = 0;
int length_nameTree_bkg = 0;




Config(inFileName_sig, inFileName_bkg, TMVA_outFileName, TMVA_cutsig, TMVA_cutbkg, TMVA_variable , nameTree_sig, nameTree_bkg,length_TMVA_variable, length_nameTree_sig, length_nameTree_bkg );

//cout << length_TMVA_variable << " "<< length_nameTree_sig << " " << length_nameTree_bkg << endl;



//-------------------
//declare Factory

auto inputFile_signal = TFile::Open(inFileName_sig.c_str()); // .c_str() stands for the conversion of the variable from std::string to object of type const char *
auto inputFile_bkg = TFile::Open(inFileName_bkg.c_str());

auto outputFile = TFile::Open(TMVA_outFileName.c_str(), "RECREATE");

TMVA::Factory factory("TMVAClassification", outputFile,
"!V:ROC:!Correlations:!Silent:Color:"
"!DrawProgressBar:AnalysisType=Classification");





//-------------------
//declare DataLoader



TMVA::DataLoader loader("dataset");
//cout << length_TMVA_variable<< endl;
for (int i =0; i< length_TMVA_variable; i++) {
//cout<<TMVA_variable[i]<< endl;
loader.AddVariable(TMVA_variable[i].c_str());
}

//exit(EXIT_SUCCESS);

/*

loader.AddVariable("nLep_base");
loader.AddVariable("nLep_signal");
loader.AddVariable("lep1Pt");
loader.AddVariable("nJet30");
loader.AddVariable("nBJet30_DL1");
loader.AddVariable("met");
loader.AddVariable("met_Phi");
loader.AddVariable("nFatjets");
loader.AddVariable("mt");
*/

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
TCut mycuts = TMVA_cutsig.c_str();
TCut mycutb = TMVA_cutbkg.c_str();


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





