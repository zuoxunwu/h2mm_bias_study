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
    def __init__(self, infilename, category, model_choice, h_sig, h_bkg, title, runmode, OutDir='../OutputFiles/', InDir="/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct"):
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
        self.outdir = os.path.join('/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/',self.title)
	
    
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
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 8, 8, 8, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", 0.0231, 0.0231,0.0231, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['c0'] = ["c0","c0", 4, 4, 4,True]
                mkpower.p['c1'] = ["c1","c1", -0.52, -0.52, -0.52, True]
                mkpower.p['pow0'] = ["pow0","pow0", -10.0, -10.0, -10.0,True]
                mkpower.p['pow1'] = ["pow1","pow1", 0.0, 0.0, 0.0,True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1",-0.7443,-0.7443, -0.7443,True]
                mklegendre.p['c2'] = ["c2","c2", 0.38, 0.38, 0.38, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.171, -0.171, -0.171, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp_mod()
                mkexp.p['a1'] = ["a1", "a1", 2, 2, 2, True]
                mkexp.p['b0'] = ["b0", "b0", 0.00004, 0.00004, 0.00004, True]
                mkexp.p['b1'] = ["b1", "b1", 0.090, 0.090, 0.090, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3_mod()
                mkbernstein.p['c1'] = ["c1", "c1", 0.20, 0.20, 0.20, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.40, 0.40, 0.40, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.25, 0.25, 0.25, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 2, 2, 2, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", 0, 0, 0, True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        ################
        # cat2: WH_BDT_n02_p02
        ################
        elif self.title == "WH_BDT_n02_p02":
            smodel, sigParamList, sgc = MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 5, 5, 5, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", 0.0199, 0.0199, 0.0199, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['c0'] = ["c0","c0", 4, 4, 4,True]
                mkpower.p['c1'] = ["c1","c1", -0.51, -0.51, -0.51, True]
                mkpower.p['pow0'] = ["pow0","pow0", -7.8, -7.8, -7.8,True]
                mkpower.p['pow1'] = ["pow1","pow1", 0.5, 0.5, 0.5,True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1", "c1", -0.800, -0.800, -0.800,True]
                mklegendre.p['c2'] = ["c2", "c2", 0.39, 0.39, 0.39, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.126, -0.126, -0.126, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp_mod()
                mkexp.p['a1'] = ["a1", "a1", 10, 10, 10, True]
                mkexp.p['b0'] = ["b0", "b0", 0.002, 0.002, 0.002, True]
                mkexp.p['b1'] = ["b1", "b1", 0.065, 0.065, 0.065, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3_mod()
                mkbernstein.p['c1'] = ["c1", "c1", 0.31, 0.31, 0.31, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.35, 0.35, 0.35, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.23, 0.23, 0.23, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 10, 10, 10, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -3.22, -3.22, -3.22, True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        ################
        # cat3: WH_BDT_p02_p06
        ################
        elif self.title == "WH_BDT_p02_p06":
            smodel, sigParamList, sgc = MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 6, 6, 6, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", 0.0179, 0.0179, 0.0179, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['c0'] = ["c0","c0", 1.1, 1.1, 1.1,True]
                mkpower.p['c1'] = ["c1","c1", -1.478, -1.478, -1.478, True]
                mkpower.p['pow0'] = ["pow0","pow0", -4.52, -4.52, -4.52,True]
                mkpower.p['pow1'] = ["pow1","pow1", -0.743, -0.743, -0.743,True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.892, -0.892, -0.892,True]
                mklegendre.p['c2'] = ["c2","c2", 0.44, 0.44, 0.44, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.158, -0.158, -0.158, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp_mod()
                mkexp.p['a1'] = ["a1", "a1", 4, 4, 4, True]
                mkexp.p['b0'] = ["b0", "b0", 0.0001, 0.0001, 0.0001, True]
                mkexp.p['b1'] = ["b1", "b1", 0.083, 0.083, 0.083, True]
                model1, model1_params = mkexp.makeModel(x)

            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 0.7, 0.7, 0.7, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.2, 0.2, 0.2, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.2, 0.2, 0.2 , True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.2, 0.2, 0.2, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 3,3 ,3 , True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -0.35, -0.35 ,-0.35 , True]
                mkbwzredux.p['pow'] = ["pow","pow", 2.0, 2.0, 2.0, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        ################
        # cat4: WH_BDT_p060_p068
        ################
        elif self.title == "WH_BDT_p060_p068":
            smodel, sigParamList, sgc = MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 16, 16, 16, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", 0.019, 0.019, 0.019, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_scale()
                mkpower.p['c0'] = ["c0","c0", 0.6, 0.6, 0.6 ,True]
                mkpower.p['c1'] = ["c1","c1",-0.54, -0.54, -0.54 , True]
                mkpower.p['pow0'] = ["pow0","pow0",0.1, 0.1, 0.1 ,True]
                mkpower.p['pow1'] = ["pow1","pow1",0.2, 0.2, 0.2,True]
                model1, model1_params = mkpower.makeModel(x)

            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.760, -0.760, -0.760,True]
                mklegendre.p['c2'] = ["c2","c2", 0.38, 0.38, 0.38, True]
                mklegendre.p['c3'] = ["c3", "c3", 0.01, 0.01, 0.01, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp_mod()
                mkexp.p['a1'] = ["a1", "a1", 2, 2, 2, True]
                mkexp.p['b0'] = ["b0", "b0", -0.0005, -0.0005, -0.0005, True]
                mkexp.p['b1'] = ["b1", "b1", 0.04, 0.04, 0.04, True]
                model1, model1_params = mkexp.makeModel(x)

            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 0.7, 0.7, 0.7, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.2, 0.2, 0.2, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.4, 0.4, 0.4, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.1, 0.1, 0.1, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 23, 23, 23, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -8.3, -8.3, -8.3, True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        ################
        # cat5: WH_BDT_p068_p076
        ################
        elif self.title == "WH_BDT_p068_p076":
            smodel, sigParamList, sgc = MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 1, 1, 1, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", -0.0012, -0.0012, -0.0012, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_scale()
                mkpower.p['c0'] = ["c0","c0", 0.58, 0.58, 0.58,True]
                mkpower.p['c1'] = ["c1","c1",-0.567, -0.567, -0.567, True]
                mkpower.p['pow0'] = ["pow0","pow0", -0.374, -0.374, -0.374,True]
                mkpower.p['pow1'] = ["pow1","pow1", -0.351, -0.374, -0.374,True]
                model1, model1_params = mkpower.makeModel(x)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -2.2, -10, 10, True]
                mklegendre.p['c2'] = ["c2","c2", -0.08, -10, 10, True]
                mklegendre.p['c3'] = ["c3", "c3", -1.00, -10, 10, True]
                model1, model1_params = mklegendre.makeModel(x11)
            elif self.model_choice == 'MKExp':
                mkexp = MKExp2()
                mkexp.p['a1'] = ["a1", "a1", 1, 1, 1, True]
                mkexp.p['b1'] = ["b1", "b1", 2, 2, 2, True]
                mkexp.p['a2'] = ["a2", "a2", 2.0, 2.0, 2.0, True]
                mkexp.p['b2'] = ["b2", "b2", 0.061, 0.061, 0.061, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3_mod()
                mkbernstein.p['c1'] = ["c1", "c1", -0.01099,-0.01099,-0.01099, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.459, 0.459, 0.459, True]
                mkbernstein.p['c3'] = ["c3", "c3", -0.0, -0.0, -0.0, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 9, 9, 9, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -3.6, -3.6, -3.6, True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        ################
        # cat6: WH_BDT_p076_p10
        ################
        elif self.title == "WH_BDT_p076_p10":
            smodel, sigParamList, sgc = MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                mkbwz.p["a1"] = ["a1", "mass", 91.2, 91.2, 91.2, True]
                #mkbwz.p["a2"] = ["a2", "width", 1, 1, 1, True]
                mkbwz.p["a2"] = ["a2", "width", 2.5, 2.5, 2.5, True]
                mkbwz.p["a3"] = ["a3", "exp", 0.034, 0.034, 0.034, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['c0'] = ["c0","c0",4.7, 4.7, 4.7,True]
                mkpower.p['pow0'] = ["pow0","pow0",-10.0, -10.0, -10.0,True]
                model1, model1_params = mkpower.makeModel(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.555, -0.555, -0.555, True]
                mklegendre.p['c2'] = ["c2","c2", 0.39, 0.39, 0.39, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.211, -0.211, -0.211, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp_mod()
                mkexp.p['a1'] = ["a1", "a1", 8, 8, 8, True]
                mkexp.p['b0'] = ["b0", "b0", 0.00, 0.00, 0.00, True]
                mkexp.p['b1'] = ["b1", "b1", 0.06, 0.06, 0.06, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 0.4,0.4,0.4 , True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.3, 0.3, 0.3, True]
                mkbernstein.p['c2'] = ["c2", "c2", -0.06, -0.06, -0.06, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.3, 0.3, 0.3, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", -14.8,-14.8 ,-14.8 , True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", 7,7 ,7 , True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        #
        # end; function parameter configs
        ###################################################################################

        model1name = 'bmodel_'+self.category
        model1.SetNameTitle(model1name, model1name)
        bmodel1 = bgsf.fit(hist_data,model1,x, self.model_choice, self.title, xmin=xmin, xmax=xmax, blinded=False, roodata=data, runmode=self.runmode)
        getattr(wspace, 'import')(bmodel1, RooCmdArg())
        norm = RooRealVar(model1name+"_norm","Number of background events",data.sumEntries())
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
