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
    def __init__(self, infilename, category, model_choice, h_sig, h_bkg, title, runmode, OutDir='../OutputFiles/'):
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
        x = RooRealVar("x","x",125,110,160)
        #x.setRange("left", 110, 120)
        #x.setRange("right", 130, 160)
        x1 = RooFormulaVar("x1","x1","(@0-135)/25",RooArgList(x))
        x2 = RooFormulaVar("x2","x2","(@0-105)/20",RooArgList(x))
        x21 = RooFormulaVar("x21","x21","@0/100",RooArgList(x))
		# create binned dataset from histogram
		# needs to be named data_obs for higgs combine limit setting
        if self.runmode == "toyqdataq":
            if self.title == "WH_inclusive":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat0/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_n10_n02":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat1/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_n02_p02":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat2/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p02_p06":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat3/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p06_p10":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat4/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p060_p068":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat4/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p068_p076":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat5/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p076_p10":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance_oct/OutputFiles/cat6/toy_MKBernstein0.root") 
            td1 = infile_toydata.Get("toys/toy_1000") 
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
                mkbwz.p["a3"] = ["a3", "exp", 0.0188, 0.0188, 0.0188, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['pow0'] = ["pow0","pow0",-10.0,-10.0,-10.0,True]
                mkpower.p['c0'] = ["c0","c0",7.3,7.3,7.3,True]
                mkpower.p['pow1'] = ["pow1","pow1",9,9,9,True]
                mkpower.p['c1'] = ["c1","c1",-0.0050,-0.0050,-0.0050, True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1",-0.7443,-0.7443, -0.7443,True]
                mklegendre.p['c2'] = ["c2","c2", 0.38, 0.38, 0.38, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.171, -0.171, -0.171, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp2()
                mkexp.p['a1'] = ["a1", "a1", 8, 8, 8, True]
                mkexp.p['b1'] = ["b1", "b1", 0.159, 0.159, 0.159, True]
                mkexp.p['a2'] = ["a2", "a2", 0.0000018, 0.0000018, 0.0000018, True]
                mkexp.p['b2'] = ["b2", "b2", 0.0195, 0.0195, 0.0195, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0","c0", 0.8, 0.8 , 0.8, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.1, 0.1, 0.1, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.3, 0.3, 0.3, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.2, 0.2, 0.2, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 5.7, 5.7, 5.7, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -1.34, -1.34, -1.34, True]
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
                mkbwz.p["a3"] = ["a3", "exp", 0.018, 0.018, 0.018, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['pow0'] = ["pow0","pow0", -7.5, -7.5, -7.5, True]
                mkpower.p['c0'] = ["c0","c0", 4, 4, 4,True]
                mkpower.p['pow1'] = ["pow1","pow1", 0.2, 0.2, 0.2, True]
                mkpower.p['c1'] = ["c1","c1", -0.53, -0.53, -0.53, True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1", "c1", -0.800, -0.800, -0.800,True]
                mklegendre.p['c2'] = ["c2", "c2", 0.39, 0.39, 0.39, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.126, -0.126, -0.126, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp2()
                mkexp.p['a1'] = ["a1", "a1", 0.4, 0.4, 0.4, True]
                mkexp.p['b1'] = ["b1", "b1", 0.08, 0.08, 0.08, True]
                mkexp.p['a2'] = ["a2", "a2", 0.00010, 0.00010, 0.00010, True]
                mkexp.p['b2'] = ["b2", "b2", 0.009, 0.009, 0.009, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein2_inc()
                mkbernstein.p['c0'] = ["c0", "c0", 0.5, 0.5, 0.5, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.16, 0.16,0.16, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.18, 0.18, 0.18, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.11, 0.11, 0.11, True]
                mkbernstein.p['c4'] = ["c4", "c4", 0.11, 0.11, 0.11,  True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 7, 7, 7, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -1.94, -1.94, -1.94, True]
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
                mkbwz.p["a3"] = ["a3", "exp", 0.014, 0.014, 0.014, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['pow0'] = ["pow0","pow0",-9.9, -9.9, -9.9,True]
                mkpower.p['c0'] = ["c0","c0",6,6, 6,True]
                mkpower.p['pow1'] = ["pow1","pow1",3, 3, 3, True]
                mkpower.p['c1'] = ["c1","c1",-0.13, -0.13, -0.13, True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.892, -0.892, -0.892,True]
                mklegendre.p['c2'] = ["c2","c2", 0.44, 0.44, 0.44, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.158, -0.158, -0.158, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp2()
                mkexp.p['a1'] = ["a1", "a1", 1.3, 1.3, 1.3, True]
                mkexp.p['b1'] = ["b1", "b1", 0.142, 0.142, 0.142, True]
                mkexp.p['a2'] = ["a2", "a2", 0.000004, 0.000004, 0.000004, True]
                mkexp.p['b2'] = ["b2", "b2", 0.026, 0.026, 0.026, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 1.0, 1.0, 1.0, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.15, 0.15, 0.15, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.30, 0.30, 0.30, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.16, 0.16, 0.16, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 6, 6, 6, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -1.9, -1.9, -1.9, True]
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
                mkbwz.p["a3"] = ["a3", "exp", 0.012, 0.012, 0.012, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower()
                mkpower.p['pow0'] = ["pow0","pow0", -4.19, -4.19 , -4.19, True]
                mkpower.p['c0'] = ["c0","c0", 4, 4, 4,True]
                model1, model1_params = mkpower.makeModel(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.760, -0.760, -0.760,True]
                mklegendre.p['c2'] = ["c2","c2", 0.38, 0.38, 0.38, True]
                mklegendre.p['c3'] = ["c3", "c3", 0.01, 0.01, 0.01, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp()
                mkexp.p['a1'] = ["a1", "a1", 5.7, 5.7, 5.7, True]
                mkexp.p['b1'] = ["b1", "b1", 0.032, 0.032, 0.032, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 0.7, 0.7, 0.7, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.3, 0.3, 0.3, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.1, 0.1, 0.1, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.2, 0.2, 0.2, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 7, 7, 7, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -1.8, -1.8, -1.8, True]
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
                mkbwz.p["a3"] = ["a3", "exp", 0.009, 0.009, 0.009, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['c0'] = ["c0","c0", 2, 2 ,2,True]
                mkpower.p['c1'] = ["c0","c0", -1.68, -1.68, -1.68,True]
                mkpower.p['pow0'] = ["pow0","pow0", -5.7, -5.7, -5.7, True]
                mkpower.p['pow1'] = ["pow0","pow0", -1.03, -1.03, -1.03,True]
                model1, model1_params = mkpower.makeModel(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -1.040, -10, 10, True]
                mklegendre.p['c2'] = ["c2","c2", 0.73, -10, 10, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.025, -10, 10, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp()
                mkexp.p['a1'] = ["a1", "a1", 5.7, 0, 100, True]
                mkexp.p['b1'] = ["b1", "b1", 0.045, 0.0, 100, True]
                #mkexp.p['a2'] = ["a2", "a2", 0.00000000011, 0.00000000011, 0.00000000011, True]
                #mkexp.p['b2'] = ["b2", "b2", 0.026, 0.026, 0.026, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 1.0, 1.0, 1.0, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.18, 0.18, 0.18, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.0, 0.0, 0.0, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.2, 0.2, 0.2, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", -14.5, -14.5, -14.5, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", 6, 6, 6, True]
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
                mkbwz.p["a3"] = ["a3", "exp", 0.029, 0.029, 0.029, True]
                model1, model1_params = mkbwz.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower_inc()
                mkpower.p['pow0'] = ["pow0","pow0",-9.8, -9.8, -9.8,True]
                mkpower.p['c0'] = ["c0","c0",6,6,6,True]
                model1, model1_params = mkpower.makeModel(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                mklegendre.p['c1'] = ["c1","c1", -0.555, -0.555, -0.555, True]
                mklegendre.p['c2'] = ["c2","c2", 0.39, 0.39, 0.39, True]
                mklegendre.p['c3'] = ["c3", "c3", -0.211, -0.211, -0.211, True]
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp()
                mkexp.p['a1'] = ["a1", "a1", 5.7, 0, 100, True]
                mkexp.p['b1'] = ["b1", "b1", 0.022, 0.0, 10.0, True]
                #mkexp.p['a2'] = ["a2", "a2", 0.0002, 0.0002, 0.0002, True]
                #mkexp.p['b2'] = ["b2", "b2", -0.0050, -0.0050, -0.0050, True]
                model1, model1_params = mkexp.makeModel(x)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.p['c0'] = ["c0", "c0", 0.5, 0.5, 0.5, True]
                mkbernstein.p['c1'] = ["c1", "c1", 0.0, 0.0, 0.0, True]
                mkbernstein.p['c2'] = ["c2", "c2", 0.3, 0.3, 0.3, True]
                mkbernstein.p['c3'] = ["c3", "c3", 0.1, 0.1, 0.1, True]
                model1, model1_params = mkbernstein.makeModel(x)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux2()
                mkbwzredux.p['ex1'] = ["ex1", "ex1", 3, 3, 3, True]
                mkbwzredux.p['ex2'] = ["ex2", "ex2", -0.2, -0.2, -0.2, True]
                mkbwzredux.p['pow'] = ["pow","pow", 2, 2, 2, True]
                model1, model1_params = mkbwzredux.makeModel(x)
        #
        # end; function parameter configs
        ###################################################################################

        model1name = 'bmodel_'+self.category
        model1.SetNameTitle(model1name, model1name)
        bmodel1 = bgsf.fit(hist_data,model1,x, self.model_choice, self.title, xmin=110, xmax=160, blinded=False, roodata=data)
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
        c1.SaveAs(os.path.join(self.outdir, 'signal_fit.png'))

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
