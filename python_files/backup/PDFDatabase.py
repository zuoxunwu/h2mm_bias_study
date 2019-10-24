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
# rescale; [-1,1] to [110,190]
#-------------------------------------------
def rescale(x):
    f = RooFormulaVar("rescalex", "30.5*@0+150.0", RooArgList(x))
    return f


#-------------------------------------------
# rescale [-1,1] to [0,1]
#-------------------------------------------
def rescaleB(x):
    f = RooFormulaVar("rescalex", "0.5*@0+0.5", RooArgList(x))
    return f, [x]


#----------------------------------------
# linear
#----------------------------------------
def linear(x):
    m = RooRealVar("slope", "slope", -0.33, -10, 0)        
    b = RooRealVar("offset", "offset", 15, 2, 1000) 
    
    linear_model = RooGenericPdf("linear_model", "@1*(@0-140)+@2", RooArgList(x, m, b))
    return linear_model, [m, b]

#--------------------------------------------------------
# breit weigner for photons scaled by falling exp
# no breit weigner for the Z
#--------------------------------------------------------
def bwGamma(x):
    expParam = RooRealVar("bwg_expParam","expParam",-1e-03,-1.0,1.0)
    bwmodel = RooGenericPdf("bwg_model","exp(@0*@1)*pow(@0,-2)",RooArgList(x,expParam))

    return bwmodel, [expParam]

#--------------------------------------------------------
# breit weigner Z scaled by falling exp
# no mixture, no photon contribution
#--------------------------------------------------------
def bwZ(x):
    bwWidth =  RooRealVar("bwz_Width","widthZ",2.5,0,30)
    bwmZ =     RooRealVar("bwz_mZ","mZ",91.2,90,92)
    expParam = RooRealVar("bwz_expParam","expParam",-1e-03,-1e-02,1e+02)
    
    bwWidth.setConstant(True);
    bwmZ.setConstant(True);
    
    bwmodel  = RooGenericPdf("bwz_model","exp(@0*@3)*(@2)/(pow(@0-@1,2)+0.25*pow(@2,2))",RooArgList(x,bwmZ,bwWidth,expParam))
    return bwmodel, [bwWidth, bwmZ, expParam]

#--------------------------------------------------------
# breit weigner mixture scaled by falling exp (run1 bg)
#--------------------------------------------------------
def bwZGamma(x, mix_min=0.001):
    bwWidth =  RooRealVar("bwzg_Width","widthZ",2.5,0,30)
    bwmZ =     RooRealVar("bwzg_mZ","mZ",91.2,90,92)
    
    expParam = RooRealVar("bwzg_expParam","expParam",-0.0053,-0.0073,-0.0033)
    mixParam = RooRealVar("bwzg_mixParam","mix",0.379,0.2,1)
    
    bwWidth.setConstant(True);
    bwmZ.setConstant(True);
    
    phoExpMmumu = RooGenericPdf("phoExpMmumu","exp(@0*@1)*pow(@0,-2)",RooArgList(x,expParam))
    bwExpMmumu  = RooGenericPdf("bwExpMmumu","exp(@0*@3)*(@2)/(pow(@0-@1,2)+0.25*pow(@2,2))",RooArgList(x,bwmZ,bwWidth,expParam))
    bwmodel     = RooAddPdf("bwzg_model","bwzg_model", RooArgList(bwExpMmumu,phoExpMmumu),RooArgList(mixParam))

    return bwmodel, [bwWidth, bwmZ, expParam, mixParam, phoExpMmumu, bwExpMmumu]
    
#----------------------------------------
# perturbed exponential times bwz
# with an off power for the breit weigner
#----------------------------------------
def bwZredux(x):
    a1 = RooRealVar("bwz_redux_a1", "a1", 1.39, 0.7, 2.1)
    a2 = RooRealVar("bwz_redux_a2", "a2", 0.46, 0.30, 0.62)
    a3 = RooRealVar("bwz_redux_a3", "a3", -0.26, -0.40, -0.12)

    #a1.setConstant()
    #a2.setConstant()
    #a3.setConstant()
    
    f = RooFormulaVar("bwz_redux_f", "(@1*(@0/100)+@2*(@0/100)^2)", RooArgList(x, a2, a3))
    #expmodel = RooGenericPdf("bwz_redux_model", "exp(@2)*(2.5)/(pow(@0-91.2,@1)+0.25*pow(2.5,@1))", RooArgList(x, a1, f))
    expmodel = RooGenericPdf("bwz_redux_model", "bwz_redux_model", "exp(@2)*(2.5)/(pow(@0-91.2,@1)+pow(2.5/2,@1))", RooArgList(x, a1, f))
    return expmodel, [a1, a2, a3, f]



#----------------------------------------
# perturbed exponential times bwz
# with an off power for the breit weigner
#----------------------------------------
def bwZreduxFixed(x):
    a1 = RooRealVar("bwz_redux_fixed_a1", "a1", 2.0, 0.7, 2.1)
    a2 = RooRealVar("bwz_redux_fixed_a2", "a2", 0.36, 0.0, 50.0)
    a3 = RooRealVar("bwz_redux_fixed_a3", "a3", -0.36, -50.0, 0)
    bwmZ = RooRealVar("bwz_redux_fixed_mZ","mZ",91.2,89,93)
    w = RooRealVar("bwz_redux_fixed_w","w",2.5,0,10)

    a1.setConstant()
    #a2.setConstant()
    #a3.setConstant()
    bwmZ.setConstant()
    w.setConstant()
    
    f = RooFormulaVar("bwz_redux_fixed_f", "(@1*(@0/100)+@2*(@0/100)^2)", RooArgList(x, a2, a3))
    #expmodel = RooGenericPdf("bwz_redux_model", "exp(@2)*(2.5)/(pow(@0-91.2,@1)+0.25*pow(2.5,@1))", RooArgList(x, a1, f))
    expmodel = RooGenericPdf("bwz_redux_fixed_model", "bwz_redux_fixed_model", "exp(@2)*(2.5)/(pow(@0-@3,@1)+pow(@4/2,@1))", RooArgList(x, a1, f, bwmZ, w))
    return expmodel, [a1, a2, a3, f, bwmZ, w]

#----------------------------------------
# hgg falling exponential
#----------------------------------------
def higgsGammaGamma(x):
    a1 = RooRealVar("hgg_a1", "a1", -5, -1000, 1000)          
    a2 = RooRealVar("hgg_a2", "a2", -5, -1000, 1000)           
    one = RooRealVar("hgg_one", "one", 1.0, -10, 10) 
    one.setConstant()
    
    #a1.setConstant(True)

    f = RooFormulaVar("hgg_f", "@1*(@0/100)+@2*(@0/100)^2", RooArgList(x, a1, a2))
    expmodel = RooExponential('hggexp_model', 'hggexp_model', f, one) # exp(1*f(x))

    return expmodel, [a1, a2, one, f]

#----------------------------------------
# chebychev
#----------------------------------------
def chebychev(x, order=7): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)
    #c1 = RooRealVar("c1","c1", 1.0,-1.0,1.0)
    #c2 = RooRealVar("c2","c2", 1.0,-1.0,1.0)

    args = RooArgList()
    params = []
    for i in range(0,order):
        c = RooRealVar("c"+str(i),"c"+str(i), 1.0/2**i,-1.0,1.0)
        args.add(c)
        params.append(c)

    chebychev = RooChebychev("chebychev"+str(order),"chebychev"+str(order), x,args) 
    return chebychev, params

# bernstein
#----------------------------------------
def bernstein(x, order=8): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)
    #c1 = RooRealVar("c1","c1", 1.0,-1.0,1.0)
    #c2 = RooRealVar("c2","c2", 1.0,-1.0,1.0)

    args = RooArgList()
    params = []
    for i in range(0,order):
        c = RooRealVar("c"+str(i),"c"+str(i), 1.0/2**i,-1.0,1.0)
        args.add(c)
        params.append(c)

    bernstein = RooBernstein("bernstein"+str(order),"bernstein"+str(order), x, args) 
    return bernstein, params

# bernstein3
#----------------------------------------
def bernstein3(x): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)
    #c1 = RooRealVar("c1","c1", 1.0,-1.0,1.0)
    #c2 = RooRealVar("c2","c2", 1.0,-1.0,1.0)

    args = RooArgList()
    params = []

    c0 = RooRealVar("c0","c0", 0.6,-1.0,1.0)
    c1 = RooRealVar("c1","c1", 0.298,-1.0,1.0)
    c2 = RooRealVar("c2","c2", 0.260,-1.0,1.0)

    #c0.setConstant()
    #c1.setConstant()
    #c2.setConstant()

    for e in [c0,c1,c2]:
        args.add(e)
        params.append(e)

    bernstein = RooBernstein("bernstein3","bernstein3", x, args) 
    return bernstein, params

# bernstein
#----------------------------------------
def bernstein2(x): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)
    #c1 = RooRealVar("c1","c1", 1.0,-1.0,1.0)
    #c2 = RooRealVar("c2","c2", 1.0,-1.0,1.0)

    args = RooArgList()
    params = []
    c0 = RooRealVar("c0","c0", 0.61,0.61-0.45,0.61+0.45)
    c1 = RooRealVar("c1","c1", -0.0052,-0.0052-0.017,-0.0052+0.017)
    c2 = RooRealVar("c2","c2", 0.33,0.33-0.24+0.33+0.24)
    c3 = RooRealVar("c3","c3", -0.1049,-0.1049-0.079,-0.1049+0.079)
    c4 = RooRealVar("c4","c4", 0.18,0.18-0.13,0.18+0.13)
    c5 = RooRealVar("c5","c5", -0.0003,-0.0003-0.021,-0.0003+0.021)
    c6 = RooRealVar("c6","c6", 0.047,0.047-0.036,0.047+0.036)
    c7 = RooRealVar("c7","c7", 0.027,0.027-0.022,0.027+0.022)

    args.add(c0)
    args.add(c1)
    args.add(c2)
    args.add(c3)
    args.add(c4)
    args.add(c5)
    args.add(c6)
    args.add(c7)

    params.append(c0)
    params.append(c1)
    params.append(c2)
    params.append(c3)
    params.append(c4)
    params.append(c5)
    params.append(c6)
    params.append(c7)

    bernstein = RooBernstein("bernstein","bernstein", x, args) 
    return bernstein, params


#----------------------------------------
# h2mupoly
#----------------------------------------
def h2mupoly(x, order=5): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)

    args = RooArgList()
    args.add(x)
    params = []
    poly_str = ""
    for i in range(0,order):
        c = RooRealVar("c"+str(i),"c"+str(i), 1.0/2**i,-1.0,1.0)
        args.add(c)
        params.append(c)
        if i==0:
            poly_str += '(@%d)^2' % (i+1)
        else:
            poly_str += '+ pow(@%d,2)*((160-@0)/50)^%d' % ((i+1), i)

    print "h2mupoly = "+poly_str

    h2mupoly = RooGenericPdf("h2mupoly%d"%order, "h2mupoly%d"%order, poly_str, args)
    return h2mupoly, params

#----------------------------------------
# h2mupolyf
#----------------------------------------
def h2mupolyf(x, order=10): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)

    args = RooArgList()
    args.add(x)
    params = []
    poly_str = ""
    for i in range(0,order):
        c = RooRealVar("c"+str(i),"c"+str(i), 1.0/2,-1.0,1.0)
        args.add(c)
        params.append(c)
        if i==0:
            poly_str += '(@%d)^2' % (i+1)
        else:
            poly_str += '+ pow(@%d,2)*sqrt(pow((160-@0)/50,%d))' % ((i+1), i)

    print "h2mupolyf = "+poly_str

    h2mupolyf = RooGenericPdf("h2mupolyf%d"%order, "h2mupolyf%d"%order, poly_str, args)
    return h2mupolyf, params

#----------------------------------------
# h2mupolypow
#----------------------------------------
def h2mupolypow(x, order=6): 
    #c0 = RooRealVar("c0","c0", 1.0,-1.0,1.0)

    args = RooArgList()
    args.add(x)
    params = []
    poly_str = ""

    ic = 1
    ib = 2
    for o in range(0,order):
        c = RooRealVar("c"+str(o),"c"+str(o), 1.0/2,-1.0,1.0)
        b = RooRealVar("b"+str(o),"b"+str(o), 1.0/2,-3.14,3.14)
        args.add(c)
        args.add(b)
        params.append(c)
        params.append(b)
        if o==0:
            poly_str += '(@%d)^2' % (ic)
        else:
            poly_str += '+ TMath::Power(@%d,2)*TMath::Power((160-@0)/50,%d+(cos(@%d))^2)' % (ic, o, ib)

        ic+=2
        ib+=2

    print "h2mupolypow = "+poly_str

    h2mupolypow = RooGenericPdf("h2mupolypow%d"%order, "h2mupolypow%d"%order, poly_str, args)
    return h2mupolypow, params

#--------------------------------------------------------
# breit weigner scaled by falling exp, then add a line
# for ttbar
#--------------------------------------------------------
def bwZPlusLinear(x):
    bwWidth =  RooRealVar("bwzl_widthZ","widthZ",2.5,0,30)
    bwmZ =     RooRealVar("bwzl_mZ","mZ",91.2,85,95)
    expParam = RooRealVar("bwzl_expParam","expParam",-1e-03,-1e-01,1e-01)

    bwWidth.setConstant(True);
    bwmZ.setConstant(True);

    slopeParam = RooRealVar("bwzl_slope", "slope", -0.2, -50, 0)          
    offsetParam = RooRealVar("bwzl_offset", "offset", 39, 0, 1000)            
    
    mix1 = RooRealVar("bwzl_mix1","mix1",0.95,0,1)

    linMmumu = RooGenericPdf("bwzl_linMmumu", "@1*@0+@2", RooArgList(x, slopeParam, offsetParam))
    bwExpMmumu  = RooGenericPdf("bwzl_bwExpMmumu","exp(@0*@3)*(@2)/(pow(@0-@1,2)+0.25*pow(@2,2))",RooArgList(x,bwmZ,bwWidth,expParam))
    model     = RooAddPdf("bwzl_model","bwzl_model", RooArgList(bwExpMmumu,linMmumu),RooArgList(mix1))

    return model, [bwWidth, bwmZ, expParam, mix1, slopeParam, offsetParam, bwExpMmumu, linMmumu]

#--------------------------------------------------------------------
# breit weigner mixture (z + photons) scaled by falling exp (run1 bg)
# then add a line for ttbar
#--------------------------------------------------------------------
def bwZGammaPlusLinear(x):
    bwWidth =  RooRealVar("bwzgl_widthZ","widthZ",2.5,0,30)
    bwmZ =     RooRealVar("bwzgl_mZ","mZ",91.2,85,95)
    expParam = RooRealVar("bwzgl_expParam","expParam",-0.0053,-0.0073,-0.0033)

    bwWidth.setConstant(True);
    bwmZ.setConstant(True);

    slopeParam = RooRealVar("bwl_slope", "slope", -0.2, -50, 0)          
    offsetParam = RooRealVar("bwl_offset", "offset", 39, 0, 1000)            
    
    mix1 = RooRealVar("bwzgl_mix1","mix1",0.10,0.01,0.20)
    mix2 = RooRealVar("bwzgl_mix2","mix2",0.39,0.1,1)
  
    expParam.setConstant(True);
    mix1.setConstant(True);
    mix2.setConstant(True);

    linMmumu = RooGenericPdf("bwzgl_linMmumu", "@1*@0+@2", RooArgList(x, slopeParam, offsetParam))
    phoExpMmumu = RooGenericPdf("bwzgl_phoExpMmumu","exp(@0*@1)*pow(@0,-2)",RooArgList(x,expParam))
    bwExpMmumu  = RooGenericPdf("bwzgl_bwExpMmumu","exp(@0*@3)*(@2)/(pow(@0-@1,2)+0.25*pow(@2,2))",RooArgList(x,bwmZ,bwWidth,expParam))
    model     = RooAddPdf("bwzgl_model","bwl_model", RooArgList(linMmumu,bwExpMmumu,phoExpMmumu),RooArgList(mix1, mix2))

    return model, [bwWidth, bwmZ, expParam, mix1, mix2, slopeParam, offsetParam, phoExpMmumu, bwExpMmumu, linMmumu]
   
'''
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
    co0 = RooRealVar("co0","co0",1.,-10.,10.)
    le1 = RooLegendre("le1","le1",x,1) 
    co1 = RooRealVar("co1","co1",1,-10.,10.)
    le2 = RooLegendre("le2","le2",x,2) 
    co2 = RooRealVar("co2","co2",1.,-10.,10.)
    le3 = RooLegendre("le3","le3",x,3) 
    co3 = RooRealVar("co3","co3",-0.02367,-0.02367-0.0019,-0.02367+0.0019)
    le4 = RooLegendre("le4","le4",x,4) 
    co4 = RooRealVar("co4","co4",0.0126,0.0126-0.0011,0.0126+0.0011)
    le5 = RooLegendre("le5","le5",x,5)
    co5 = RooRealVar("co5","co5",-0.006588,-0.006588-0.00067,-0.006588+0.00067)
    le6 = RooLegendre("le6","le6",x,6) 
    co6 = RooRealVar("co6","co6",0.00358,0.00358-0.00052,0.00358+0.00052)
    le7 = RooLegendre("le7","le7",x,7) 
    co7 = RooRealVar("co7","co7",-0.001717,-0.001717-0.00041,-0.001717+0.00041)
    le8 = RooLegendre("le8","le8",x,8) 
    co8 = RooRealVar("co8","co8",eps,-1,1)
    le9 = RooLegendre("le9","le9",x,9) 
    co9 = RooRealVar("co9","co9",0.00086,0.00086-0.00042,0.00086+0.00042)
    le10 = RooLegendre("le10","le10",x,10) 
    co10 = RooRealVar("co10","co10",-0.001475,-0.001475-0.00045*2,-0.001475+0.00045*2)
    for e in [co0,le0,co1,le1,co2,le2]:
        arglist.add(e)
    leg = RooGenericPdf("leg","leg","@0*@1+@2*@3+@4*@5",arglist)
    # need to return all RooObjects used to construct the final model; some memory sake I think.
    # model, parameters, the rest of RooObjets
    return leg, [co0,le0,co1,le1,co2,le2]
'''


#----------------------------------------------------------------
# Legendre Polynomial
#----------------------------------------------------------------
def MKLegendre(x):
    arglist = RooArgList() 
    # constant off set to handle negative pdf values
    # defining Legendre polynomial
    le0 = RooLegendre("le0","le0",x,0) 
    co0 = RooRealVar("co0","co0",1.4,-10.,10.)
    le1 = RooLegendre("le1","le1",x,1) 
    co1 = RooRealVar("co1","co1",-0.6,-1,1)
    le2 = RooLegendre("le2","le2",x,2) 
    co2 = RooRealVar("co2","co2",0.1,-1,1)
    co0.setConstant()
    for e in [co0,le0,co1,le1,co2,le2]:
        arglist.add(e)
    leg = RooGenericPdf("leg","leg","@0*@1+@2*@3+@4*@5",arglist)
    # need to return all RooObjects used to construct the final model; some memory sake I think.
    # model, parameters, the rest of RooObjets
    return leg, [co0,le0,co1,le1,co2,le2]

# Legendre polynomial
# -------------------
# def MKLegendre2(x):
#     gc = [] # this is needed probably C++ and python interface thing. (global containter)
#     modelStr = "(0.1+"
#     arglist = r
    







'''
def sumOfExp(x):
    arglist = RooArgList()
    #x
    a0 = RooRealVar("a0","a0",0.1,-10,10)
    a1 = RooRealVar("a1","a1",0.2,-10,10)
    a2 = RooRealVar("a2","a2",0.3,-10,10)
    a3 = RooRealVar("a3","a3",0.4,-10,10)
    b1 = RooRealVar("b1","b2",0.1,-1,1)
    b2 = RooRealVar("b2","b2",0.2,-1,1)
    b3 = RooRealVar("b3","b3",0.3,-1,1)

    # need to be this way; some bug in ROOT
    for e in [x,a0,a1,b1,a2,b2,a3,b3]:
        arglist.add(e)

    fitfunc = RooGenericPdf("fitfunc","fitfunc","@1+@2*exp(-1*@3*@0)+@4*exp(-1*@5*@0)+@6*exp(-1*@7*@0)",arglist)
    return fitfunc, [a0,a1,b1,a2,b2,a3,b3]
'''

def sumOfExp(x):
    arglist = RooArgList()
    #x
    a0 = RooRealVar("a0","a0",0.00001,-1,1)
    a1 = RooRealVar("a1","a1",0.002,-1,1)
    #a2 = RooRealVar("a2","a2",0.3,-10,10)
    #a3 = RooRealVar("a3","a3",0.4,-10,10)
    b1 = RooRealVar("b1","b2",0.2,-1,1)
    #b2 = RooRealVar("b2","b2",0.2,-1,1)
    #b3 = RooRealVar("b3","b3",0.3,-1,1)
    
    a0.setConstant()

    # need to be this way; some bug in ROOT
    for e in [x,a0,a1,b1]:
        arglist.add(e)

    fitfunc = RooGenericPdf("fitfunc","fitfunc","@1+@2*exp(-1*@3*@0)",arglist)
    return fitfunc, [a0,a1,b1]
