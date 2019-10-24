import ROOT as r
import os

# create workspace
w_dp = r.RooWorkspace("w_dp","w_dp")

# load file
tfile = r.TFile(os.path.join(os.getcwd(), "InputFiles", "muPairs_mass135_165_nb31.root"))
h = tfile.Get("net_histos/c_01_test_Net_Signal")

# define x variable



# load data



# load models






# save to workspace
