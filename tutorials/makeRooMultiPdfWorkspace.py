# turing c++ code to python
# I haven't found ROOT in python documentation, so I'm doing thing using analogy
# routine things; -> to .
# remove ; 

#============================================
# import
#============================================

#import PDFDatabase as pdfs
#import prettytable
#import string
#import re
#import argparse
#import math as math
#import numpy as np
from ROOT import *

#import sys
#sys.argv.append( '-b-' )

#

#Load the combine Library 
gSystem.Load("libHiggsAnalysisCombinedLimit.so")

# Open the dummy H->gg workspace 
infilename = "toyhgg_in.root"
tfile = TFile(infilename)
w_hgg = tfile.Get("multipdf") # workspace that contain multiple pdfs

# The observable (CMS_hgg_mass in the workspace)
mass =  w_hgg.var("CMS_hgg_mass")

# Get three of the functions inside, exponential, linear polynomial, power law
pdf_exp = w_hgg.pdf("env_pdf_1_8TeV_exp1")
pdf_pol = w_hgg.pdf("env_pdf_1_8TeV_bern2")
pdf_pow = w_hgg.pdf("env_pdf_1_8TeV_pow1")


# Fit the functions to the data to set the "prefit" state (note this can and should be redone with combine when doing bias studies as one typically throws toys from the "best-fit"
data = w_hgg.data("roohist_data_mass_cat1_toy1_cutrange__CMS_hgg_mass")
pdf_exp.fitTo(data)  # index 0
pdf_pow.fitTo(data) # index 1 
pdf_pol.fitTo(data)   # index 2

# Make a plot (data is a toy dataset)
plot = mass.frame()
data.plotOn(plot)
pdf_exp.plotOn(plot,RooFit.LineColor(kGreen))
pdf_pol.plotOn(plot,RooFit.LineColor(kBlue))
pdf_pow.plotOn(plot,RooFit.LineColor(kRed))
plot.SetTitle("PDF fits to toy data")
plot.Draw()

# Make a RooCategory object. This will control which of the pdfs is "active"
cat = RooCategory("pdf_index","Index of Pdf which is active")

# Make a RooMultiPdf object. The order of the pdfs will be the order of their index, ie for below 
# 0 == exponential
# 1 == linear function
# 2 == powerlaw
mypdfs = RooArgList()
mypdfs.add(pdf_exp)
mypdfs.add(pdf_pol)
mypdfs.add(pdf_pow)

multipdf = RooMultiPdf("roomultipdf","All Pdfs",cat,mypdfs)
   
# As usual make an extended term for the background with _norm for freely floating yield
norm = RooRealVar("roomultipdf_norm","Number of background events",0,10000)
   
# Save to a new workspace
fout = TFile("background_pdfs.root","RECREATE")
wout = RooWorkspace("backgrounds","backgrounds")
getattr(wout,'import')(cat,RooCmdArg())
getattr(wout,'import')(norm,RooCmdArg())
getattr(wout,'import')(multipdf,RooCmdArg())
wout.Print()
wout.Write()
