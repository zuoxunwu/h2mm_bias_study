1) Make work space and datacard for combine

2) Generate Toys

3) FitDiagnotics





root -l fitDiagnostics.root
tree_fit_sb->Draw("(r-1)/rErr>>h(20,-4,4)")
h->Fit("gaus")



root -l /afs/cern.ch/user/m/mukim/MKWorkingArea/CMSSW_8_1_0/src/potatoes/Data/muPairs_mass.root

higgs combine github -> manual -> multipdf
hello
root file is for barrel
