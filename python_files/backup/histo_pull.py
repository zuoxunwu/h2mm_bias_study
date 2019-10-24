import argparse
from ROOT import *
import os
import sys

def main1():
    # parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('toy_model')
    parser.add_argument('fit_model')
    parser.add_argument('signal_strength')
    parser.add_argument('title')
    args = parser.parse_args()
    
    gROOT.SetBatch(kTRUE)
    path1 = os.path.join(os.getcwd(), 'OutputFiles', 'nbyn'+args.toy_model+args.fit_model+args.signal_strength, 'fitDiagnostics.root')
    print(path1)
    tfile = TFile(path1)
    fit_tree = tfile.Get('tree_fit_sb')
    c = TCanvas("pull", "pull", 400, 400)
    draw_str = "(r-"+args.signal_strength+")/rErr>>h(40,-4,4)"
    fit_tree.Draw(draw_str,"fit_status==0") # "(r-1)/rErr>>h(20,-4,4)"
    h.Fit("gaus")
    c.SaveAs("OutputFiles/pull_"+args.title+"_"+args.toy_model+"_"+args.fit_model+"_"+args.signal_strength+".png")
    g11 = h.GetListOfFunctions().FindObject("gaus")
    print("Mean", g11.GetParameter(1))
    path2 = os.path.join(os.getcwd(), 'OutputFiles', 'pulls_'+args.title+args.signal_strength+'.txt')
    with open(path2,'a+') as file1:
        file1.write("pull"+","+args.toy_model+","+args.fit_model+","+str(g11.GetParameter(1))+"\n")

# arg1, arg2 = toy_model, fit_model
if __name__ == '__main__':
    main1()
