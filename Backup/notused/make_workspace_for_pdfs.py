#============================================
# import
#============================================

import PDFDatabase as pdfs
import BGSFrun
import prettytable
import string
import re
import argparse
from ROOT import *

#============================================
# code
#============================================

class WorkspaceMaker:
# object to make workspace, root files, and datacards needed for analytic shape or template
# limit setting via higgs combine.

    infilename = ''
    category = ''
    signal_hist = 0
    bkg_hist = 0
    net_hist= 0
    data_hist =0
    tfile = 0
    nuisance_params = []

    def __init__(self, infilename, category):
        self.infilename = infilename
        self.category = category
        self.tfile = TFile(infilename)
        self.setDataHist()
        self.setNetBackgroundHist()
        self.setNetSignalHist()
        self.setNetMCHist()
	
    
    # uses the naming convention from categorize.cxx to automatically grab the histograms
    def setNetBackgroundHist(self):
    # grab net bkg MC, use as data for prototyping
        self.bkg_hist = self.tfile.Get('net_histos/'+self.category+"_Net_Bkg")
        self.bkg_hist.SetTitle(self.category+"_Net_Bkg")
    
    def setNetSignalHist(self):
    # just use the net signal histogram instead of the different channels for prototyping
        self.signal_hist = self.tfile.Get('net_histos/'+self.category+"_Net_Signal")
        self.signal_hist.SetTitle(self.category+"_Net_Signal")


    def setDataHist(self):
    # grab net bkg MC, use as data for prototyping
        self.data_hist = self.tfile.Get('net_histos/Data_2017BCDEF')
        self.data_hist.SetTitle(self.category+"_Data")
    
    def setNetMCHist(self):
        # add up the signal and background
        self.net_hist = self.signal_hist.Clone()
        self.net_hist.Add(self.bkg_hist)
        self.net_hist.SetName(self.category+'_Net_MC')
        self.net_hist.SetTitle(self.category+'_Net_MC')
    
    def MakeWorkspaceForPdfs(self):
	# don't display plots; instead saving them as files
	gROOT.SetBatch(kTRUE)
        wspace = RooWorkspace(self.category)
	bgsf = BGSFrun.BGSpectrumFitter(self.infilename, self.category)
	h1 = bgsf.bg_all_hist

	# x1 dimuon mass variable
	x1, massmin, massmax = bgsf.getX(h1)

        getattr(wspace, 'import')(x1, RooCmdArg())
    
        # create binned dataset from histogram
        # needs to be named data_obs for higgs combine limit setting
        data   = RooDataHist('data_obs', 'data_obs', RooArgList(x1), self.net_hist)
        # import is a keyword so we wspace.import() doesn't work in python. have to do this
        getattr(wspace, 'import')(data, RooCmdArg())

        #----------------------------------------
        # create background model
        #----------------------------------------
	# model1
	model1, model1_params = pdfs.bwZreduxFixed(x1)
	model1.SetNameTitle('bmodel1_'+self.category, 'bmodel1_'+self.category)
	bmodel1 = bgsf.fit(h1,model1,x1)
	
        getattr(wspace, 'import')(bmodel1, RooCmdArg())

	# model2
	model2, model2_params = pdfs.bernstein(x1)
	model2.SetNameTitle('bmodel2_'+self.category, 'bmodel2_'+self.category)
	bmodel2 = bgsf.fit(h1,model2,x1)
	
        getattr(wspace, 'import')(bmodel2, RooCmdArg())

        wspace.Print()
        wspace.SaveAs(self.category+'_s.root')
    

print('program is running ...')
wdm = WorkspaceMaker('/afs/cern.ch/user/m/mukim/MKWorkingArea/CMSSW_8_1_0/src/potatoes/Data/muPairs_mass.root', 'c_01_test') 
print wdm.infilename, wdm.category
wdm.MakeWorkspaceForPdfs()
