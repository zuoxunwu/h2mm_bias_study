##############################################
# WorkspaceAndDatacardMaker.py               #
##############################################
# Makes .root file and datacard needed for   #
# shape and template limit setting.          #
# output .root and .txt files to be used     #
# with higgs combine.                        #
##############################################

# prototype with no systematics or automatic interpolation


#============================================
# import
#============================================

import prettytable
import string
import re
import argparse
from ROOT import *

#============================================
# code
#============================================

class WorkspaceAndDatacardMaker:
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
    
    def makeShapeWorkspace(self):
    # make workspace with signal model and background model for analytic shape fit.
    # save it to a root file.
        # suppress all messages except those that matter
        RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
        print "="*78
        wspace = RooWorkspace(self.category)
    
        # Get the dimu mass histogram to use for limit setting
        nbins   = self.net_hist.GetNbinsX()
        massmin = self.net_hist.GetBinLowEdge(1)
        massmax = massmin + nbins*self.net_hist.GetBinWidth(1)
    
        #----------------------------------------
        # create di-muon mass variable
        # syntax:
        # <name>[initial-val, min-val, max-val]
        #----------------------------------------
        x = RooRealVar('x','x',150, massmin, massmax)
        x.SetTitle('m_{#mu#mu}')
        x.setUnit('GeV')
    
        # create binned dataset from histogram
        # needs to be named data_obs for higgs combine limit setting
        data   = RooDataHist('data_obs', 'data_obs', RooArgList(x), self.net_hist)
        # import is a keyword so we wspace.import() doesn't work in python. have to do this
        getattr(wspace, 'import')(data, RooCmdArg())

        # need to set the signal model to something concrete, so we will fit it to the expected SM histogram

        bhist  = RooDataHist('bkg', 'bkg', RooArgList(x), self.net_hist)
        shist  = RooDataHist('sig', 'sig', RooArgList(x), self.signal_hist)
    
        #----------------------------------------
        # create background model
        #----------------------------------------
        alpha = RooRealVar("alpha","alpha",1.0,0.5,1.5)
	getattr(wspace, 'import')(alpha, RooCmdArg())	

	mean_BW = RooRealVar("mean_BW", "mean_BW", 91,80,100)          # nuisance parameter1 for the background fit
        width_BW = RooRealVar("width_BW", "width_BW", 4,0.1,10)         # nuisance parameter2 for the background fit
    
        #func_BW = RooBreitWigner("func_BW","func_BW", x, mean_BW, width_BW)
        bmodel = RooBreitWigner('bmodel_'+self.category, 'bmodel_'+self.category, x, mean_BW, width_BW)

 
        bkgParamList = [mean_BW, width_BW]
        #getattr(wspace, 'import')(bmodel, RooCmdArg())
    
        #----------------------------------------
        # create signal model, double gaussian
        #----------------------------------------

        # define the parameters for the two gaussians
        meanG1 = RooRealVar("MeanG1", "MeanG1", 150, massmin, massmax)
        meanG2 = RooRealVar("MeanG2", "MeanG2", 150, massmin, massmax)
        meanG3 = RooRealVar("MeanG3", "MeanG3", 150, massmin, massmax)

        widthG1 = RooRealVar("WidthG1", "WidthG1", 5.0, 0.1, 20.0)
        widthG2 = RooRealVar("WidthG2", "WidthG2", 5.0, 0.1, 20.0)
        widthG3 = RooRealVar("WidthG3", "WidthG3", 5.0, 0.1, 20.0)
        
        # mixing parameters for the two gaussians
        coefG1 = RooRealVar("coefG1",  "coefG2", 0.5,0.,1.)
        coefG2 = RooRealVar("coefG2",  "coefG2", 0.5,0.,1.)

        # define the two gaussians
        gaus1 = RooGaussian("gaus1", "gaus1", x, meanG1, widthG1)
        gaus2 = RooGaussian("gaus2", "gaus2", x, meanG2, widthG2)
        gaus3 = RooGaussian("gaus3", "gaus3", x, meanG3, widthG3)

        # double gaussian
        smodel = RooAddPdf('smodel_'+self.category, 'smodel_'+self.category, RooArgList(gaus1, gaus2, gaus3), RooArgList(coefG1,coefG2))

        sigParamList = [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2]

        #----------------------------------------
        # save data and signal & bg models for use
        # with higgs combine
        #----------------------------------------
   
	smodel.fitTo(shist)
        xframe = x.frame()
        shist.plotOn(xframe) #b->s
        smodel.plotOn(xframe) #
        smodel.paramOn(xframe)
	print("below is chi2")
	i=0
	while i<10:
		print(xframe.chiSquare('smodel_'+self.category,'bkg',i)) 
		i+=1
        c1 = TCanvas('fig_signal_fit', 'fit', 10, 10, 500, 500)
        xframe.Draw()
        c1.SaveAs('.root')
        c1.SaveAs('.png')


	bmodel.fitTo(bhist)
        x2frame = x.frame()
        bhist.plotOn(x2frame) #b->s
        bmodel.plotOn(x2frame) #
        bmodel.paramOn(x2frame) #
        c2 = TCanvas('fig_bkg_fit','fit', 10, 10, 500, 500)
        x2frame.Draw()
        c2.SaveAs('.root')
        c2.SaveAs('.png')
     
        # after fitting, we nail the parameters down so that higgs combine 
        # knows what the SM signal shape is
        for i in sigParamList:
            i.setConstant(True)

        getattr(wspace, 'import')(smodel, RooCmdArg())

	# similar thing for background 
        #for i in bkgParamList:
        #    i.setConstant(True)

        getattr(wspace, 'import')(bmodel, RooCmdArg())

        wspace.Print()
        wspace.SaveAs(self.category+'_s.root')

    def makeShapeDatacard(self):
    # analytic shape fit datacard
        # figure out the size of the column
        width = max(len('smodel_'+self.category), len('process'))
        width+=4

        f = open(self.category+'_s.txt', 'w') 
        f.write('imax *\n')
        f.write('jmax *\n')
        f.write('kmax *\n')
        f.write('----------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('shapes * * '+self.category+'_s.root '+self.category+':$PROCESS\n')
        f.write('----------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('bin            '+self.category+'\n')
        f.write('observation    -1.0\n')
        f.write('----------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('bin'.ljust(width)+self.category.ljust(width)+self.category.ljust(width)+'\n')
        f.write('process'.ljust(width)+('smodel_'+self.category).ljust(width)+('bmodel_'+self.category).ljust(width)+'\n')
        f.write('process'.ljust(width)+'0'.ljust(width)+'1'.ljust(width)+'\n')
        f.write('rate'.ljust(width)+'1'.ljust(width)+'1'.ljust(width)+'\n')
        f.write('----------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('alpha'.ljust(width)+'rateParam'.ljust(width)+self.category.ljust(width)+('bmodel_'+self.category).ljust(width)+'1'.ljust(width)+'[0.9,1.1]'.ljust(width)+'\n')
        f.write('lumi'.ljust(width)+'lnN'.ljust(width)+'1.05'.ljust(width)+'1.05'.ljust(width)+'\n')
      
        # get maximum length of the strings to figure out the width of the columns for the systematics section 
        pwidth = len('param')
        for n in self.nuisance_params:
            if len(n) > pwidth: pwdith = len(n)
        pwidth+=4
      
        # write the systematics section
        for n in self.nuisance_params:
            f.write(n.ljust(pwidth)+'param'.ljust(pwidth)+'0.0'.ljust(pwidth)+'0.1'.ljust(pwidth)+'\n')


print('program is running ...')
# Needs the file with the dimu_mass plots created by categorize.cxx
# also needs to know the category you want to make the root file and datacard for
wdm = WorkspaceAndDatacardMaker('/afs/cern.ch/user/m/mukim/potatoes/Data/muPairs_mass.root', 'c_01_test') 
print wdm.infilename, wdm.category
wdm.makeShapeWorkspace()
wdm.makeShapeDatacard()
# use higgs combine to combine the categories for the net limit, p-value, whatever
