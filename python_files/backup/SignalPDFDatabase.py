##############################################
# PDFDatabase.py                             #
##############################################

#============================================
# import
#============================================

import prettytable
import string
import re
import argparse
from ROOT import *

import sys
sys.argv.append( '-b-' )

#-------------------------------------------
# rescale
#-------------------------------------------
def rescale(x):
    f = RooFormulaVar("rescalex", "40.0*@0+150.0", RooArgList(x))
    return f

#----------------------------------------
# linear
#----------------------------------------
def linear(x):
    m = RooRealVar("slope", "slope", -0.33, -10, 0)        
    b = RooRealVar("offset", "offset", 15, 2, 1000) 
    
    linear_model = RooGenericPdf("linear_model", "@1*(@0-140)+@2", RooArgList(x, m, b))
    return linear_model, [m, b]

   
#----------------------------------------
# Tripple Gaussian
#----------------------------------------
def TripleGauss(x):
    meanG1 = RooRealVar("MeanG1", "MeanG1", 0.1, -1., 1.)
    meanG2 = RooRealVar("MeanG2", "MeanG2", 0.1, -1., 1.)
    meanG3 = RooRealVar("MeanG3", "MeanG3", 0.1, -1., 1.)
    widthG1 = RooRealVar("WidthG1", "WidthG1", 0.1, 0., 1.)
    widthG2 = RooRealVar("WidthG2", "WidthG2", 0.1, 0., 1.)
    widthG3 = RooRealVar("WidthG3", "WidthG3", 0.1, 0., 1.)
    coefG1 = RooRealVar("coefG1",  "coefG1", 0.5,0.,1.)
    coefG2 = RooRealVar("coefG2",  "coefG2", 0.5,0.,1.)
    gaus1 = RooGaussian("gaus1", "gaus1", x, meanG1, widthG1)
    gaus2 = RooGaussian("gaus2", "gaus2", x, meanG2, widthG2)
    gaus3 = RooGaussian("gaus3", "gaus3", x, meanG3, widthG3)
    triplegauss = RooAddPdf('triplegauss', 'triplegauss', RooArgList(gaus1, gaus2, gaus3), RooArgList(coefG1,coefG2))
    return triplegauss, [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2], [gaus1,gaus2,gaus3]

#----------------------------------------------------------------
# Legendre Polynomial
#----------------------------------------------------------------
def MKLegendre(x):
    eps = 0.0000001 #epsilon
    arglist = RooArgList() 
    # constant off set to handle negative pdf values
    #uni = r.RooUniform("uni","uni",r.RooArgSet(x))
    #data_uni = uni.generate(r.RooArgSet(x),500000)
    #data
    #data = r.RooDataHist('data_obs', 'data_obs', r.RooArgList(x), hist_data)
    #data.add(data_uni)
    # defining Legendre polynomial
    le0 = RooLegendre("le0","le0",x,0) 
    co0 = RooRealVar("co0","co0",eps,-1,1)
    le1 = RooLegendre("le1","le1",x,1) 
    co1 = RooRealVar("co1","co1",eps,-1,1)
    le2 = RooLegendre("le2","le2",x,2) 
    co2 = RooRealVar("co2","co2",eps,-1,1)
    le3 = RooLegendre("le3","le3",x,3) 
    co3 = RooRealVar("co3","co3",eps,-1,1)
    le4 = RooLegendre("le4","le4",x,4) 
    co4 = RooRealVar("co4","co4",eps,-1,1)
    le5 = RooLegendre("le5","le5",x,5)
    co5 = RooRealVar("co5","co5",eps,-1,1)
    le6 = RooLegendre("le6","le6",x,6) 
    co6 = RooRealVar("co6","co6",eps,-1,1)
    le7 = RooLegendre("le7","le7",x,7) 
    co7 = RooRealVar("co7","co7",eps,-1,1)
    le8 = RooLegendre("le8","le8",x,8) 
    co8 = RooRealVar("co8","co8",eps,-1,1)
    le9 = RooLegendre("le9","le9",x,9) 
    co9 = RooRealVar("co9","co9",eps,-1,1)
    le10 = RooLegendre("le10","le10",x,10) 
    co10 = RooRealVar("co10","co10",eps,-1,1)
    arglist.add(co0) #0
    arglist.add(le0)
    arglist.add(co1)
    arglist.add(le1)
    arglist.add(co2)
    arglist.add(le2)
    arglist.add(co3)
    arglist.add(le3)
    arglist.add(co4)
    arglist.add(le4)
    arglist.add(co5)
    arglist.add(le5) #11
    arglist.add(co6)
    arglist.add(le6)
    arglist.add(co7)
    arglist.add(le7) #15
    #arglist.add(co8)
    #arglist.add(le8) # 17
    arglist.add(co9)
    arglist.add(le9) # 19
    arglist.add(co10)
    arglist.add(le10) # 21
    leg = RooGenericPdf("leg","leg","@0*@1+@2*@3+@4*@5+@6*@7+@8*@9+@10*@11+@12*@13+@14*@15+@16*@17+@18*@19",arglist)
    return leg, [le0,co0,le1,co1,le2,co2,le3,co3,le4,co4,le5,co5,le6,co6,le7,co7,le9,co9,le10,co10]
    # @0*@1+@2*@3+@4*@5+@6*@7+@8*@9+@10*@11+@12*@13+@14*@15+@16*@17+@18*@19+@20*@21
