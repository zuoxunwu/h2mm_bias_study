# Workspace And Datacard Maker               
# Makes .root file and datacard needed for   
# shape limit setting.                       
# output .root and .txt files to be used     
# with higgs combine.                        

import BGSFrun
from ROOT import *

class WorkspaceAndDatacardMaker:
# object to make workspace, root files, and datacards needed for analytic shape or template
# limit setting via higgs combine.
    infilename = '' # [path, bkg, sig histo]
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

    def __init__(self, infilename, category, model_choice, h_sig, h_bkg, title, runmode, OutDir='../OutputFiles/'):
        self.infilename = infilename
        self.h_sig = h_sig
        self.h_bkg = h_bkg
        self.category = category
        self.title = title
        print(infilename)
        print(h_sig)
        print(h_bkg)
        self.tfile = TFile(infilename) #we loaded our root-file
        self.setDataHist()
        #self.setNetBackgroundHist()
        self.setNetSignalHist()
        #self.setNetMCHist()
        self.model_choice = model_choice # string for choosing model (function)
        self.outdir = '/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/'
	
    
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
        x1 = RooFormulaVar("x1","x1","(@0-135)/50",RooArgList(x))
        x2 = RooFormulaVar("x2","x2","(@0-105)/20",RooArgList(x))
        x21 = RooFormulaVar("x21","x21","@0/100",RooArgList(x))
		# create binned dataset from histogram
		# needs to be named data_obs for higgs combine limit setting
        if self.runmode == "toyqdataq":
            if self.title == "WH_inclusive":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/cat0/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_n10_n02":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/cat1/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_n02_p02":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/cat2/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p02_p06":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/cat3/toy_MKBernstein0.root") 
            if self.title == "WH_BDT_p06_p10":
                infile_toydata = TFile("/home/pq8556/WorkingArea/CMSSW_8_1_0/src/novel_bias_variance/OutputFiles/cat4/toy_MKBernstein0.root") 
            td1 = infile_toydata.Get("toys/toy_1000") 
            data = td1.binnedClone("data_obs","data_obs") # RooDataHist
            #data   = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.data_hist)
        elif self.runmode == "mc_to_toys":
            self.setNetBackgroundHist()
            data   = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.bkg_hist)
          
        #self.setNetBackgroundHist()
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

        # pdfs_ttH or pdfs_WH

        ############################################
        # Set paramters for models for each category
        # Arguments:
        #   category string, models, parameters
        # Produce:
        #   differnt prefit for each category 
        ############################################
        if self.title == "WH_inclusive":
            import pdfs_WH_inc_redux
            smodel, sigParamList, sgc = pdfs_WH_inc_redux.MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                model1, model1_params = pdfs_WH_inc_redux.MKBwz(x1)
            elif self.model_choice == 'MKBwzredux':
                model1, model1_params = pdfs_WH_inc_redux.MKBwzredux(x)
            elif self.model_choice == 'MKPower':
                model1, model1_params = pdfs_WH_inc_redux.MKPower(x21,order=2)
            elif self.model_choice == 'MKLegendre':
                model1, model1_params = pdfs_WH_inc_redux.MKLegendre(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                model1, model1_params = pdfs_WH_inc_redux.MKExp2(x1)
            elif self.model_choice == 'MKBernstein':
                model1, model1_params = pdfs_WH_inc_redux.MKBernstein2(x)

        ##########################
        # Category: WH_BDT_n02_p02
        ##########################
        elif self.title == "WH_BDT_n02_p02":
            from pdfClass import MKBwz, MKPower, MKLegendre, MKExp, MKExp2, MKBernstein, MKBernstein2, MKBernstein3, MKBwzredux
            import pdfClass
            smodel, sigParamList, sgc = pdfClass.MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                model1, model1_params = mkbwz.makeModel(x1)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux()
                #mkbwzredux.setParam("pow",0,0.0,10.0) # setConstant()
                mkbwzredux.setParam("ex1",-16.6,-16.6-10*3,-16.6+10*3)
                mkbwzredux.setParam("ex2",5,5-3.9*3,5+3.9*3)
                model1, model1_params = mkbwzredux.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower()
                mkpower.setParam("pow0", 1.0, -10.0, 10.0)
                mkpower.setParam("c0", 1.0, -10.0, 10.0)
                model1, model1_params = mkpower.makeModel(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp()
                mkexp.setParam("a1", 1, -10, 10) # co
                #mkexp.setConst("a1")
                mkexp.setParam("b1", 4, 0, 10) # exp
                model1, model1_params = mkexp.makeModel(x1)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.setParam("c0",1, 1, 1)
                mkbernstein.setConst("c0")
                #c3v=0.5
                #c2 = 0
                #mkbernstein.setParam("c2",0, -0.2, 0.2)
                #mkbernstein.setParam("c4",1/2**4, -1, 1)
                #mkbernstein.setConst("c0")
                #c2 =0.0
                #mkbernstein.setParam("c2",c2,c2,c2)
                #mkbernstein.setConst("c2")
                model1, model1_params = mkbernstein.makeModel(x, orders=["c0","c1","c2"])

        ################
        # WH_BDT_p02_p06
        ################
        elif self.title == "WH_BDT_p02_p06":
            from pdfClass import MKBwz, MKPower, MKLegendre, MKExp, MKExp2, MKBernstein, MKBernstein2, MKBernstein3, MKBwzredux
            import pdfClass
            smodel, sigParamList, sgc = pdfClass.MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                mkbwz = MKBwz()
                model1, model1_params = mkbwz.makeModel(x1)
            elif self.model_choice == 'MKBwzredux':
                mkbwzredux = MKBwzredux()
                #mkbwzredux.setParam("pow",0,0.0,10.0) # setConstant()
                mkbwzredux.setParam("ex1",-16.6,-16.6-10*3,-16.6+10*3)
                mkbwzredux.setParam("ex2",5,5-3.9*3,5+3.9*3)
                model1, model1_params = mkbwzredux.makeModel(x)
            elif self.model_choice == 'MKPower':
                mkpower = MKPower()
                mkpower.setParam("pow0", 1.0, -10.0, 10.0)
                mkpower.setParam("c0", 1.0, -10.0, 10.0)
                model1, model1_params = mkpower.makeModel(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                mklegendre = MKLegendre()
                model1, model1_params = mklegendre.makeModel(x1,order=[1,2,3])
            elif self.model_choice == 'MKExp':
                mkexp = MKExp()
                mkexp.setParam("a1", 1, -10, 10) # co
                #mkexp.setConst("a1")
                mkexp.setParam("b1", 4, 0, 10) # exp
                model1, model1_params = mkexp.makeModel(x1)
            elif self.model_choice == 'MKBernstein':
                mkbernstein = MKBernstein3()
                mkbernstein.setParam("c0",1, 1, 1)
                mkbernstein.setConst("c0")
                #c3v=0.5
                #c2 = 0
                #mkbernstein.setParam("c2",0, -0.2, 0.2)
                #mkbernstein.setParam("c4",1/2**4, -1, 1)
                #mkbernstein.setConst("c0")
                #c2 =0.0
                #mkbernstein.setParam("c2",c2,c2,c2)
                #mkbernstein.setConst("c2")
                model1, model1_params = mkbernstein.makeModel(x, orders=["c0","c1","c2"])

        else:
            import pdfs_WH
            smodel, sigParamList, sgc = pdfs_WH.MKTripleGauss(x)
            if self.model_choice == 'MKBwz':
                model1, model1_params = pdfs_WH.MKBwz(x1)
            elif self.model_choice == 'MKBwzredux':
                model1, model1_params = pdfs_WH.MKBwzredux(x)
            elif self.model_choice == 'MKPower':
                model1, model1_params = pdfs_WH.MKPower(x21,order=1)
            elif self.model_choice == 'MKLegendre':
                model1, model1_params = pdfs_WH.MKLegendre(x1,order=[1,2])
            elif self.model_choice == 'MKExp':
                model1, model1_params = pdfs_WH.MKExp(x1)
            elif self.model_choice == 'MKBernstein':
                model1, model1_params = pdfs_WH.MKBernstein(x,order=2)
        # elif title == 2:
        #     import pdfs_WH_inc
        #     if self.model_choice == 'MKBwz':
        #         model1, model1_params = pdfs_WH_inc.MKBwz(x1)
        #     elif self.model_choice == 'MKPower':
        #         model1, model1_params = pdfs_WH_inc.MKPower(x2,order=2)
        #     elif self.model_choice == 'MKLegendre':
        #         model1, model1_params = pdfs_WH_inc.MKLegendre(x1,order=[1,2,3])
        #     elif self.model_choice == 'MKExp':
        #         model1, model1_params = pdfs_WH_inc.MKExp2(x1)
        #     elif self.model_choice == 'MKBernstein':
        #         model1, model1_params = pdfs_WH_inc.MKBernstein(x,order=3)

        model1name = 'bmodel_'+self.category
        model1.SetNameTitle(model1name, model1name)
        bmodel1 = bgsf.fit(hist_data,model1,x,xmin=110, xmax=160, blinded=False, roodata=data)
        #x1frame0 = x1.frame()
        #bmodel1.plotOn(x1frame0)
        #c0 = TCanvas('bkg_fit','bkg_fit',10,10,500,500)	
        #x1frame0.Draw()
        getattr(wspace, 'import')(bmodel1, RooCmdArg())
        norm = RooRealVar(model1name+"_norm","Number of background events",data.sumEntries())
        norm.setConstant(False)
        getattr(wspace,'import')(norm)

        #-------------------------------------------------------------------------
        # create signal model(triple gaussian)

        #smodel, sigParamList, sgc = pdfs_WH_inc_redux.MKTripleGauss(x)
        smodelname = 'smodel_'+self.category
        smodel.SetNameTitle(smodelname, smodelname)
        smodel.fitTo(shist)
        # after fitting, we nail the parameters down so that higgs combine 
        # knows what the SM signal shape is
        for i in sigParamList:
            i.setConstant(True)

        getattr(wspace, 'import')(smodel, RooCmdArg())

        #--------------------------------------------------------------------------
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
        c1.SaveAs('.root')
        c1.SaveAs('.png')

		#-------------------------------------------------------------------
		# saving workspace to rootfile
        wspace.SaveAs('OutputFiles/'+self.category+'_s'+self.model_choice+'.root')
        wspace.Print()
        print(self.outdir+self.category+'_s'+self.model_choice +'.root')

        signal_rate = str(shist.sumEntries())
        print("model_choice", self.model_choice)
        print("shist.sumEntries()", shist.sumEntries())
        print("data.sumEntries()", data.sumEntries())

#    def makeShapeDatacard(self):
		# analytic shape fit datacard
        # figure out the size of the column
        width = max(len('smodel_'+self.category), len('process'))
        width+=4
        f = open(self.outdir+self.category+'_s'+self.model_choice+'.txt', 'w') 
        f.write('imax *\n')
        f.write('jmax *\n')
        f.write('kmax *\n')
        f.write('------------\n')
        f.write('shapes * * '+self.category+'_s'+self.model_choice+'.root '+self.category+':$PROCESS\n')
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
