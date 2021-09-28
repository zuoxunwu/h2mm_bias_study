############################################
# Workspace And Datacard Maker               
# Makes .root file and datacard needed for   
# shape limit setting.                       
# output .root and .txt files to be used     
# with higgs combine.                        
############################################

import BGSFrun
from ROOT import *
from pdfClass_6bdt import *
import os

DoBlind = True

class WorkspaceAndDatacardMaker:
    # fold
    infilename = '' # path for bkg, sig histos
    h_sig = ''
    h_bkg = ''
    title = ''
    category = ''
    signal_hist = 0
    bkg_hist = 0
    net_hist= 0
    data_hist =0
    tfile = 0
    nuisance_params = []
    runmode=''

    # parsed from config.txt
    # infilename: histo root file, category: category, model_choice: bkg_model
    # h_sig: signal histogram name, h_bkg: background histogram name, runmode:runmode 
    def __init__(self, infilename, category, model_choice, h_sig, h_bkg, title, runmode, OutDir='../OutputFiles/', InDir="/afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/src/bias_study"):
        self.basepath = InDir
        self.infilename = infilename
        self.h_sig = h_sig
        self.h_bkg = h_bkg
        self.category = category
        self.title = title
        self.runmode = runmode
        print(infilename)
        print(h_sig)
        print(h_bkg)
        self.tfile = TFile(infilename) #we loaded our root-file
        self.setDataHist()
        self.setNetSignalHist()
        self.model_choice = model_choice # string for choosing model (function)
        self.outdir = os.path.join('/afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/src/bias_study/OutputFiles/',self.title)
	
    
    # uses the naming convention from categorize.cxx to automatically grab the histograms
    def setNetBackgroundHist(self):
        # grab net bkg MC, use as data for prototyping
        self.bkg_hist = self.tfile.Get(self.h_bkg)
        #self.bkg_hist.SetTitle(self.h_bkg)
    
    def setNetSignalHist(self):
        # just use the net signal histogram instead of the different channels for prototyping
        self.signal_hist = self.tfile.Get(self.h_sig)
        #self.signal_hist.SetTitle(self.h_sig)


    def setDataHist(self):
        # grab net bkg MC, use as data for prototyping
        #self.data_hist = self.tfile.Get('net_histos/Data_2017BCDEF')
        #self.data_hist = self.tfile.Get("H_pair_mass_zoomH_Net_Bkg")
        self.data_hist = self.tfile.Get(self.h_bkg)
        self.data_hist.SetTitle(self.category+"_Data")
    
    def setNetMCHist(self):
        # add up the signal and background
        self.net_hist = self.signal_hist.Clone()
        self.net_hist.Add(self.bkg_hist)
        self.net_hist.SetName(self.category+'_Net_MC')
        self.net_hist.SetTitle(self.category+'_Net_MC')

    # make workspace for signal and backgroudn fitting function
    def makeShapeWorkspace(self):
        # don't display plots; instead saving them as files
        gROOT.SetBatch(kTRUE)
        wspace = RooWorkspace(self.category)
        bgsf = BGSFrun.BGSpectrumFitter(self.infilename, self.category)
        hist_data = self.data_hist
        xmin = 110
        xmax = 150
        x = RooRealVar("x","x",125,xmin,xmax)
        #x.setRange("left", 110, 120)
        #x.setRange("right", 130, 160)
        
        x1 = RooFormulaVar("x1","x1","(@0-%f)/%f"%((xmin+xmax)/2.0, (xmax-xmin)/2.0),RooArgList(x))
        #x11 = RooFormulaVar("x1","x1","(@0-135)/25", RooArgList(x))
        #x11 = RooFormulaVar("x11","x11","(@0-135)/20", RooArgList(x))
        x2 = RooFormulaVar("x2","x2","(@0-105)/20",RooArgList(x))
        x21 = RooFormulaVar("x21","x21","@0/100",RooArgList(x))
        # fold
		# create binned dataset from histogram
		# needs to be named data_obs for higgs combine limit setting
        if self.runmode == "toyqdataq":
            toyqdataq_model = "toy_MKBwz0_seed10.root"
            infile_toydata = TFile(os.path.join(self.basepath, "OutputFiles", self.title, toyqdataq_model)) 
            td1 = infile_toydata.Get("toys/toy_10") 
            data = td1.binnedClone("data_obs","data_obs") # RooDataHist
            #data   = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.data_hist)
        elif self.runmode == "mc_to_toys":
            self.setNetBackgroundHist()
            data = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.bkg_hist)
          
		# import is a keyword so we wspace.import() doesn't work in python. have to do this
        getattr(wspace, 'import')(data, RooCmdArg())

		# need to set the signal model to something concrete, so we will fit it to the expected SM histogram
        shist  = RooDataHist('sig', 'sig', RooArgList(x), self.signal_hist)
    
		#-------------------------------------------------------------------------
		# create background model(from PDFDatabase.py)

		# A. bwZreduxFixed(x1)
		# B. bernstein2(x1)
		# C. bwZredux(x1)
		# D. higgsGammaGamma(x1)
		# E. bwZ(x1)
        # F. sumOfExp(x1)

        ############################################################################
        # start; function parameter configs
        #

        ################
        # cat1: WH_BDT_n10_n02
        ################
        if self.title == "WH_BDT_n10_n02":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0249
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

	    elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
		mkbwzredux_fix.name = 'MKBwzredux_fix'
		mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 4
                  mkbwzredux_fix.p['ex2'][2] = -0.62
                  mkbwzredux_fix.p['w'][2]   = 1
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
	    elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 3.6
                  mkbwzredux.p['ex2'][2] = -0.37
                  mkbwzredux.p['w'][2]   = 1
                  mkbwzredux.p['pow'][2] = 2
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
	    elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.807
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
	    elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -1.076
		  mkpower1int.p['const'][2]  = 0.011
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
	    # exps
	    elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0316
                model1, model1_params = mkexp1.makeModel(x)
	    elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
		mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.1
		  mkexp1int.p['const'][2] = 0.2
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.2
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
		if self.runmode == 'toyqdataq':
		  mkbernstein3.p['c0'][2] = 0.6
		  mkbernstein3.p['c1'][2] = 0.1
		  mkbernstein3.p['c2'][2] = 0.3
		  mkbernstein3.p['c3'][2] = 0.1
		  mkbernstein3.p['c0'][5] = True
		  mkbernstein3.p['c1'][5] = True
		  mkbernstein3.p['c2'][5] = True
		  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)
	    elif self.model_choice == 'MKBernstein4':
                mkbernstein4 = MKBernstein4()
                if self.runmode == 'toyqdataq':
                  mkbernstein4.p['c0'][2] = 0.4
                  mkbernstein4.p['c1'][2] = 0.09
                  mkbernstein4.p['c2'][2] = 0.23
                  mkbernstein4.p['c3'][2] = 0.12
		  mkbernstein4.p['c4'][2] = 0.12
                  mkbernstein4.p['c0'][5] = True
                  mkbernstein4.p['c1'][5] = True
                  mkbernstein4.p['c2'][5] = True
                  mkbernstein4.p['c3'][5] = True
		  mkbernstein4.p['c4'][5] = True
                model1, model1_params = mkbernstein4.makeModel(x)

        ################
        # cat2: WH_BDT_n02_p02
        ################
        elif self.title == "WH_BDT_n02_p02":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0196
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.46
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 2.6
                  mkbwzredux.p['ex2'][2] = -0.50
                  mkbwzredux.p['w'][2]   = 20
                  mkbwzredux.p['pow'][2] = 1.9
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.925
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.648
                  mkpower1int.p['const'][2]  = -0.038
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0375
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.068
                  mkexp1int.p['const'][2] = 0.119
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.2
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = 0
                  mkbernstein3.p['c2'][2] = 0
                  mkbernstein3.p['c3'][2] = 0.2
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)
            elif self.model_choice == 'MKBernstein4':
                mkbernstein4 = MKBernstein4()
                if self.runmode == 'toyqdataq':
                  mkbernstein4.p['c0'][2] = 0.4
                  mkbernstein4.p['c1'][2] = 0.19
                  mkbernstein4.p['c2'][2] = 0.19
                  mkbernstein4.p['c3'][2] = 0.09
                  mkbernstein4.p['c4'][2] = 0.12
                  mkbernstein4.p['c0'][5] = True
                  mkbernstein4.p['c1'][5] = True
                  mkbernstein4.p['c2'][5] = True
                  mkbernstein4.p['c3'][5] = True
                  mkbernstein4.p['c4'][5] = True
                model1, model1_params = mkbernstein4.makeModel(x)

        ################
        # cat3: WH_BDT_p02_p06
        ################
        elif self.title == "WH_BDT_p02_p06":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0209
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 0
                  mkbwzredux_fix.p['ex2'][2] = 0.7
                  mkbwzredux_fix.p['w'][2]   = 18
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 3.0
                  mkbwzredux.p['ex2'][2] = -0.22
                  mkbwzredux.p['w'][2]   = 19
                  mkbwzredux.p['pow'][2] = 2.2
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.90
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.888
                  mkpower1int.p['const'][2]  = -0.0009
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.036
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.079
                  mkexp1int.p['const'][2] = 0.133
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.2
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = 0.2
                  mkbernstein3.p['c2'][2] = 0.2
                  mkbernstein3.p['c3'][2] = 0.2
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)
            elif self.model_choice == 'MKBernstein4':
                mkbernstein4 = MKBernstein4()
                if self.runmode == 'toyqdataq':
                  mkbernstein4.p['c0'][2] = 0.5
                  mkbernstein4.p['c1'][2] = 0.14
                  mkbernstein4.p['c2'][2] = 0.24
                  mkbernstein4.p['c3'][2] = 0.09
                  mkbernstein4.p['c4'][2] = 0.13
                  mkbernstein4.p['c0'][5] = True
                  mkbernstein4.p['c1'][5] = True
                  mkbernstein4.p['c2'][5] = True
                  mkbernstein4.p['c3'][5] = True
                  mkbernstein4.p['c4'][5] = True
                model1, model1_params = mkbernstein4.makeModel(x)

        ################
        # cat4: WH_BDT_p060_p068
        ################
        elif self.title == "WH_BDT_p060_p068":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.017
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.5
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 4
                  mkbwzredux.p['ex2'][2] = -1
                  mkbwzredux.p['w'][2]   = 5
                  mkbwzredux.p['pow'][2] = 2.0
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.995
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.89
                  mkpower1int.p['const'][2]  = 0
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0402
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.082
                  mkexp1int.p['const'][2] = 0.108
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.2
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.3
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = -0.06
                  mkbernstein3.p['c2'][2] = 0.5
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)

        ################
        # cat5: WH_BDT_p068_p076
        ################
        elif self.title == "WH_BDT_p068_p076":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0011
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 20
                  mkbwzredux_fix.p['ex2'][2] = -7.8
                  mkbwzredux_fix.p['w'][2]   = 2
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 81
                  mkbwzredux.p['ex2'][2] = -26.6
                  mkbwzredux.p['w'][2]   = 11
                  mkbwzredux.p['pow'][2] = 6.5
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -1.339
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.581
                  mkpower1int.p['const'][2]  = -0.088
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0576
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.058
                  mkexp1int.p['const'][2] = 0.001
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
            elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.1
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.2
                  mkbernstein2.p['c2'][2] = 0.1
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = 0
                  mkbernstein3.p['c2'][2] = 0.2
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)

        ################
        # cat6: WH_BDT_p076_p10
        ################
        elif self.title == "WH_BDT_p076_p10":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.035
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)
	    elif self.model_choice == 'MKBwzredux_p2':
                mkbwzredux_p2 = MKBwzredux_mod()
                mkbwzredux_p2.name = 'MKBwzredux_p2'
                mkbwzredux_p2.p['pow'][5] = True
		mkbwzredux_p2.p['w'][5] = True
                #if self.runmode == 'toyqdataq':
                #  mkbwzredux_p2.p['ex1'][2] = 0
		#  mkbwzredux_p2.p['ex2'][2] = 0
                #  mkbwzredux_p2.p['ex1'][5] = True
		#  mkbwzredux_p2.p['ex2'][5] = True
                model1, model1_params = mkbwzredux_p2.makeModel(x)
	    elif self.model_choice == 'MKBwzredux_p3':
                mkbwzredux_p3 = MKBwzredux_mod()
                mkbwzredux_p3.name = 'MKBwzredux_p3'
                mkbwzredux_p3.p['pow'][5] = True
                #if self.runmode == 'toyqdataq':
                #  mkbwzredux_p2.p['ex1'][2] = 0
                #  mkbwzredux_p2.p['ex2'][2] = 0
                #  mkbwzredux_p2.p['ex1'][5] = True
                #  mkbwzredux_p2.p['ex2'][5] = True
                model1, model1_params = mkbwzredux_p3.makeModel(x)

            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 1
                  mkbwzredux.p['ex2'][2] = 1.4
                  mkbwzredux.p['w'][2]   = 20
                  mkbwzredux.p['pow'][2] = 2.4
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.552
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.7
                  mkpower1int.p['const'][2]  = 0
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.021
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.28
                  mkexp1int.p['const'][2] = 0.083
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
            elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 0.3
                  mkbernstein3.p['c1'][2] = 0.4
                  mkbernstein3.p['c2'][2] = -0.12
                  mkbernstein3.p['c3'][2] = 0.3
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)


        ################
        # WH new cat1: WH_BDT_n10_n01
        ################
        elif self.title == "WH_BDT_n10_n01":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0286
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.5
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 0.8
                  mkbwzredux.p['ex2'][2] = -0.3
                  mkbwzredux.p['w'][2]   = 2.5
                  mkbwzredux.p['pow'][2] = 1.3
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux.makeModel(x)
            elif self.model_choice == 'MKBwzGamma':
                mkbwzgamma = MKBwzGamma()
                if self.runmode == 'toyqdataq':
                  mkbwzgamma.p['pow0'][2] = 0.003
                  mkbwzgamma.p['f0'][2]  = 0.25
                model1, model1_params = mkbwzgamma.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -0.704
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.663
                  mkpower1int.p['const'][2]  = -0.007
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0277
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.069
                  mkexp1int.p['const'][2] = 0.218
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.2
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.3
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = -0.06
                  mkbernstein3.p['c2'][2] = 0.5
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)


        ################
        # WH new cat2: WH_BDT_n01_p03
        ################
        elif self.title == "WH_BDT_n01_p03":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.0163
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.5
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 4
                  mkbwzredux.p['ex2'][2] = -1
                  mkbwzredux.p['w'][2]   = 5
                  mkbwzredux.p['pow'][2] = 2.0
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -1.009
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.812
                  mkpower1int.p['const'][2]  = -0.0147
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.0411
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.076
                  mkexp1int.p['const'][2] = 0.101
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.2
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.3
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = -0.06
                  mkbernstein3.p['c2'][2] = 0.5
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)



        ################
        # WH new cat3: WH_BDT_p03_p10
        ################
        elif self.title == "WH_BDT_p03_p10":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 0.012
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.5
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 4
                  mkbwzredux.p['ex2'][2] = -1
                  mkbwzredux.p['w'][2]   = 5
                  mkbwzredux.p['pow'][2] = 2.0
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -1.11
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.736
                  mkpower1int.p['const'][2]  = -0.0319
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.046
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.074
                  mkexp1int.p['const'][2] = 0.078
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.2
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.3
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = -0.06
                  mkbernstein3.p['c2'][2] = 0.5
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)


        ################
        # cat456: WH_BDT_p06_p10 , and ZH
        ################
        elif self.title == "WH_BDT_p06_p10" or self.title == "WH_BDT_n10_n01" or self.title == "ZH_BDT_n10_p04" or self.title == "ZH_BDT_p04_p10" or self.title == "ZH_BDT_n10_n01" or self.title == "ZH_BDT_n01_p10" or self.title == "ZH_BDT_n10_p10":
            smodel, sigParamList, sgc = MKTripleGauss(x)
	    # bwzs
	    if self.model_choice == 'MKBwz_fix':
                mkbwz_fix = MKBwz()
                mkbwz_fix.name = 'MKBwz_fix'
		mkbwz_fix.p['a2'][2] = 2.5
                mkbwz_fix.p['a3'][2] = 1.5
                mkbwz_fix.p['a2'][5] = True
                mkbwz_fix.p['a3'][5] = True
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz_fix.makeModel(x)
            elif self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwz.makeModel(x)
	    elif self.model_choice == 'MKBwzBern1':
		mkbwzbern1 = MKBwzBern1()
		#if self.runmode == 'toyqdataq':
		model1, model1_params = mkbwzbern1.makeModel(x)
	    elif self.model_choice == 'MKBwzBern2':
                mkbwzbern2 = MKBwzBern2()
                #if self.runmode == 'toyqdataq':
                model1, model1_params = mkbwzbern2.makeModel(x)

            elif self.model_choice == 'MKBwzredux_fix':
                mkbwzredux_fix = MKBwzredux_mod()
                mkbwzredux_fix.name = 'MKBwzredux_fix'
                mkbwzredux_fix.p['pow'][5] = True
                if self.runmode == 'toyqdataq':
                  mkbwzredux_fix.p['ex1'][2] = 3
                  mkbwzredux_fix.p['ex2'][2] = -0.5
                  mkbwzredux_fix.p['w'][2]   = 20
                  mkbwzredux_fix.p['ex1'][5] = True
                  mkbwzredux_fix.p['ex2'][5] = True
                  mkbwzredux_fix.p['w'][5]   = True
                model1, model1_params = mkbwzredux_fix.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux_mod()
                if self.runmode == 'toyqdataq':
                  mkbwzredux.p['ex1'][2] = 4
                  mkbwzredux.p['ex2'][2] = -1
                  mkbwzredux.p['w'][2]   = 5
                  mkbwzredux.p['pow'][2] = 2.0
                  mkbwzredux.p['ex1'][5] = True
                  mkbwzredux.p['ex2'][5] = True
                  mkbwzredux.p['w'][5]   = True
                  mkbwzredux.p['pow'][5] = True
                model1, model1_params = mkbwzredux.makeModel(x)
	    # power laws
            elif self.model_choice == 'MKPower1':
                mkpower1 = MKPower1()
                mkpower1.name = "MKPower1"
                mkpower1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkpower1.p['pow0'][2]   = -1.016
                  #mkpower1.p['pow0'][5] = True
                model1, model1_params = mkpower1.makeModel(x)
            elif self.model_choice == 'MKPower1int':
                mkpower1int = MKPower1()
                mkpower1int.name = "MKPower1int"
                if self.runmode == 'toyqdataq':
                  mkpower1int.p['pow0'][2]   = -0.81
                  mkpower1int.p['const'][2]  = -0.016
                  #mkpower1int.p['pow0'][5] = True
                model1, model1_params = mkpower1int.makeModel(x)
            # exps
            elif self.model_choice == 'MKExp1':
                mkexp1 = MKExp1()
                mkexp1.p['const'][5] = True
                if self.runmode == 'toyqdataq':
                  mkexp1.p['exp1'][2] = 0.041
                model1, model1_params = mkexp1.makeModel(x)
            elif self.model_choice == 'MKExp1int':
                mkexp1int = MKExp1()
                mkexp1int.name = "MKExp1int"
                if self.runmode == 'toyqdataq':
                  mkexp1int.p['exp1'][2]  = 0.075
                  mkexp1int.p['const'][2] = 0.099
                model1, model1_params = mkexp1int.makeModel(x)
	    # berns
	    elif self.model_choice == 'MKBernstein1':
                mkbernstein1 = MKBernstein1()
                if self.runmode == 'toyqdataq':
                  mkbernstein1.p['c0'][2] = 1
                  mkbernstein1.p['c1'][2] = 0.2
                  mkbernstein1.p['c0'][5] = True
                  mkbernstein1.p['c1'][5] = True
                model1, model1_params = mkbernstein1.makeModel(x)
            elif self.model_choice == 'MKBernstein2':
                mkbernstein2 = MKBernstein2()
                if self.runmode == 'toyqdataq':
                  mkbernstein2.p['c0'][2] = 1
                  mkbernstein2.p['c1'][2] = 0.3
                  mkbernstein2.p['c2'][2] = 0.3
                  mkbernstein2.p['c0'][5] = True
                  mkbernstein2.p['c1'][5] = True
                  mkbernstein2.p['c2'][5] = True
                model1, model1_params = mkbernstein2.makeModel(x)
            elif self.model_choice == 'MKBernstein3':
                mkbernstein3 = MKBernstein3()
                if self.runmode == 'toyqdataq':
                  mkbernstein3.p['c0'][2] = 1
                  mkbernstein3.p['c1'][2] = -0.06
                  mkbernstein3.p['c2'][2] = 0.5
                  mkbernstein3.p['c3'][2] = 0.1
                  mkbernstein3.p['c0'][5] = True
                  mkbernstein3.p['c1'][5] = True
                  mkbernstein3.p['c2'][5] = True
                  mkbernstein3.p['c3'][5] = True
                model1, model1_params = mkbernstein3.makeModel(x)
        #
        # end; function parameter configs
        ###################################################################################

        model1name = 'bmodel_'+self.category
        model1.SetNameTitle(model1name, model1name)
        bmodel1 = bgsf.fit(hist_data,model1,x, self.model_choice, self.title, xmin=xmin, xmax=xmax, blinded=DoBlind, roodata=data, runmode=self.runmode)
        getattr(wspace, 'import')(bmodel1, RooCmdArg())
        norm = RooRealVar(model1name+"_norm","Number of background events",data.sumEntries(), 0, 2*data.sumEntries() )
        norm.setConstant(False)
        getattr(wspace,'import')(norm)

        #######################################
        # create signal model(triple gaussian)

        smodelname = 'smodel_'+self.category
        smodel.SetNameTitle(smodelname, smodelname)
        smodel.fitTo(shist)
        # after fitting, we nail the parameters down so that higgs combine 
        # knows what the SM signal shape is
        for i in sigParamList:
            i.setConstant(True)
        getattr(wspace, 'import')(smodel, RooCmdArg())
        
        # fold
        ########################################
		# plotting
        xframe = x.frame()
        shist.plotOn(xframe) 
        smodel.plotOn(xframe)
        smodel.paramOn(xframe)
        chi2 = xframe.chiSquare()
        print "signal"
        print chi2
        c1 = TCanvas('fig_signal_fit', 'fit', 10, 10, 500, 500)
        xframe.Draw()
        t = TLatex(.6,.2,"#chi^{2}/ndof = %7.3f" % chi2);  
        t.SetNDC(kTRUE);
        t.Draw();
        #c1.SaveAs(os.path.join('.root'))
        c1.SaveAs(os.path.join(self.basepath,self.title+'_signal_fit.png'))

		#########################################
		# saving workspace to rootfile
        # wspace.SaveAs('OutputFiles/'+self.category+'_s'+self.model_choice+'.root')
        wspath = os.path.join('OutputFiles', self.title, self.category+'_s'+self.model_choice+'.root')
        wspace.SaveAs(wspath)
        wspace.Print()
        print(os.path.join('OutputFiles', self.title, self.category+'_s'+self.model_choice+'.root'))

        signal_rate = str(shist.sumEntries())
        print("model_choice", self.model_choice)
        print("shist.sumEntries()", shist.sumEntries())
        print("data.sumEntries()", data.sumEntries())

        ################
        # Write Datacard
        ################

		# analytic shape fit datacard
        # figure out the size of the column
        width = max(len('smodel_'+self.category), len('process'))
        width+=4
        #f = open(self.outdir+self.category+'_s'+self.model_choice+'.txt', 'w') 
        f = open(os.path.join(self.outdir, self.category+'_s'+self.model_choice+'.txt'), 'w')
        f.write('imax *\n')
        f.write('jmax *\n')
        f.write('kmax *\n')
        f.write('------------\n')
        # this should match worksapce saveas path
        f.write('shapes * * '+ os.path.join(self.outdir, self.category+'_s'+self.model_choice+'.root') + ' ' + self.category+':$PROCESS\n')
        f.write('------------\n')
        f.write('bin            '+self.category+'\n')
        f.write('observation    -1\n')
        # rates
        f.write('------------\n')
        f.write('bin'.ljust(width)+self.category.ljust(width)+self.category.ljust(width)+'\n')
        f.write('process'.ljust(width)+('smodel_'+self.category).ljust(width)+('bmodel_'+self.category).ljust(width)+'\n')
        f.write('process'.ljust(width)+'0'.ljust(width)+'1'.ljust(width)+'\n')
        f.write('rate'.ljust(width)+signal_rate.ljust(width)+'1'.ljust(width)+'\n')
        # nusance parameters
        f.write('------------\n')
        f.write('lumi_13TeV'+' '+'lnN'+' '+'1.026'+' '+'-'+'\n')
