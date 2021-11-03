# CutFlow & Multivariate Analysis

In HEP **data analysis**, we have generally two categories of events (i.e. two different datasets): **signal** *events* which concern the physics we want to study and **background** *events* which have similar characteristics to the ones we are looking for.
**Event selection** rapresents a procedure that loops on all events and decides whether to accept or to discard each of them, according to specific criteria. At the end of the selection we’ll be left with a sample of **candidates**, ideally made mainly of signal events.

This repository explores two different methods for *events selection*: **cutflow** and **multivariate analysis** and the analysis is based on simulated data obtained by the Susymaker Analysis Package in order to inquire SUSY physics (signal dataset) vs Standard Model (background dataset).


## CutFlow
From the point of view of the data analysis, an event is a sequence of physics objects, organized in data structures containing the information we have to rely on.
Among all the physical quantities of each event, cuts are done on those variables (or combination of variables) that are more ”discriminant”, i.e. that ideally let to discard as much background as possible, mantaining just signal events.
What happens is that every event is questioned: the ones with a variable value over a certain **cut** are mantained, while the other are filtered out.

## MVA
A way to improve the capability of event selection is to apply a linear or, even better, a non linear correlation between the discriminating variables (**multivariate analysis**). Some of these methods succesfully developed in the last decades thanks to improvement of computing performances and the most used in HEP analysis are the *Neural Network* and the *Bost Decision Trees* methods. As before, events are filtered according to a combination of variable values. The difference is that the cuts are no more choosen manually but by algorithms specific of the choosen method.


### Repository
The repository contains:
- cutflow.py  
It is a  python class for the cut-based selection. Among its methods, SetCuts() opens the .root dataset and the filtering is applied, while GetCuts() stamps the results on a sheet with the Signal over Background ratio (S/B) to inspect the efficiency of the method. 
- tmva_train.C  
It is a C++ function based on TMVA, a toolkit of ROOT which provides a ROOT-integrated machine learning
environment. Once the datasets are opened and the Neural Network and BDT methods are booked, it trains and tests the methods and stamps the ROC curve in order to inspect the efficiency. 
- config_Demo.py / config_.py  
The file contains a dictionary variable in which all the information given by the user are set, such as the position of the input and output files or the variables for the cutflow and the tmva analysis we are interested in.
The first works with the demo dataset, while the second with the complete one.
- print.py  
It checks if everything is written in the right way in config file and then it runs cutflow .py and / or tmva_train.C
- signal_Demo.root - bkg2_Demo.root  
Dataset of signal and background events. Every tree contains branches and every branch contains events, everyone with specific variables (same for all branches of signal and background).


A more detailed description is inside every file.

### Installation
to install the application clone the repository [SC_project](https://github.com/giacomoubaldi/SC_project.git):

```
git clone https://github.com/giacomoubaldi/SC_project.git
```

### Version

### Run
If you want to run the demo version, in which one branch of signal and one branch of background are considered, type on the terminal opened inside the repository:

```
python print.py config_Demo.py
```



If you want to run the total version, you have to be sure to be inside TIER-3 since the dataset are located there.
Type on the terminal opened inside the repository:

```
python print.py config_All.py
```
The results are generated in the folder "results". In particular:
- cutflow_results_Demo.txt / cutflow_results_All.txt  
contains the results of the cutflow for all the signal and background branches
- TMVA_Output_Demo_name_branch / TMVA_Output_name_branch  
contains the results of the TMVA methods for the choosen signal branch(es)
- dataset_Demo_name_branch / dataset_name_branch  
it is a folder which contains the weights of the variables used by TMVA for the choosen signal branch(es)
- TMVA_ROC_Curve_Demo_name_branch / TMVA_ROC_Curve_name_branch  
contains the ROC curve for the TMVA used methods for the choosen signal branch(es)
