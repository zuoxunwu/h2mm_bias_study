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
    category = ''
    signal_hist = 0
    bkg_hist = 0
    net_hist= 0
    data_hist =0
    tfile = 0
    nuisance_params = []

    def __init__(self, infilename, category, model_choice, h_sig, h_bkg, OutDir='../OutputFiles/'):
        self.infilename = infilename
        self.h_sig = h_sig
        self.h_bkg = h_bkg
        self.category = category
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
        self.bkg_hist = self.tfile.Get('net_histos/'+self.category+"_Net_Bkg")
        self.bkg_hist.SetTitle(self.category+"_Net_Bkg")
    
    def setNetSignalHist(self):
    # just use the net signal histogram instead of the different channels for prototyping
        # self.signal_hist = self.tfile.Get('net_histos/'+self.category+"_Net_Signal")
        #self.signal_hist = self.tfile.Get("H_pair_mass_zoomH_Net_Sig")
        self.signal_hist = self.tfile.Get(self.h_sig)

        self.signal_hist.SetTitle(self.category+"_Net_Signal")


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
        x1 = RooFormulaVar("x1","x1","(@0-135)/50",RooArgList(x))
        x2 = RooFormulaVar("x2","x2","(@0-105)/20",RooArgList(x))
		# create binned dataset from histogram
		# needs to be named data_obs for higgs combine limit setting
        data   = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.data_hist)
        
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
        import pdfs_WH
        # for some reason giving name as is not working
        #if self.h_sig == 'asdf': 
        #    if self.model_choice == 'MKBwz':
        #        model1, model1_params = pdfs_WH.MKBwz(x1)
        #    elif self.model_choice == 'MKPower':
        #        model1, model1_params = pdfs_WH.MKPower(x2,order=2)
        #    elif self.model_choice == 'MKLegendre':
        #        model1, model1_params = pdfs_WH.MKLegendre(x1,order=[1,2,3])
        #    elif self.model_choice == 'MKExp':
        #        model1, model1_params = pdfs_WH.MKExp2(x1)
        #    elif self.model_choice == 'MKBernstein':
        #        model1, model1_params = pdfs_WH.MKBernstein(x,order=3)
        if self.model_choice == 'MKBwz':
            model1, model1_params = pdfs_WH.MKBwz(x1)
        elif self.model_choice == 'MKPower':
            model1, model1_params = pdfs_WH.MKPower(x2,order=1)
        elif self.model_choice == 'MKLegendre':
            model1, model1_params = pdfs_WH.MKLegendre(x1,order=[1,2])
        elif self.model_choice == 'MKExp':
            model1, model1_params = pdfs_WH.MKExp(x1)
        elif self.model_choice == 'MKBernstein':
            model1, model1_params = pdfs_WH.MKBernstein(x,order=2)

        model1name = 'bmodel_'+self.category
        model1.SetNameTitle(model1name, model1name)
        bmodel1 = bgsf.fit(hist_data,model1,x,xmin=110, xmax=160)
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

        smodel, sigParamList, sgc = pdfs_WH.MKTripleGauss(x)
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
        f.write('------------\n')
        f.write('bin'.ljust(width)+self.category.ljust(width)+self.category.ljust(width)+'\n')
        f.write('process'.ljust(width)+('smodel_'+self.category).ljust(width)+('bmodel_'+self.category).ljust(width)+'\n')
        f.write('process'.ljust(width)+'0'.ljust(width)+'1'.ljust(width)+'\n')
        f.write('rate'.ljust(width)+signal_rate.ljust(width)+'1'.ljust(width)+'\n')
        f.write('------------\n')
        f.write('lumi_13TeV'+' '+'lnN'+' '+'1.026'+' '+'-'+'\n')
