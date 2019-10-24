import ROOT as r
from ROOT import RooFit as rf
# -----------------------------
# | PDFs for background model |
# -----------------------------
def MKBwz(x):
    # -1, 1 x range
    gc = []
    arglist = r.RooArgList()
    arglist.add(x)
    gc.append(x)
    a1 = r.RooRealVar("a1", "a1", -0.87, -10.0, 10.0) #  mass
    a2 = r.RooRealVar("a2", "a2", 0.1, -10.0, 10.0) # width
    a3 = r.RooRealVar("a3", "a3", 0.1, -10.0, 10.0) # exp
    a1.setConstant()
    for e in [a1,a2,a3]:
        gc.append(e)
        arglist.add(e)
    model = r.RooGenericPdf("model", "model", "@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))", arglist)
    return model, gc
# define function: Legendre polynomial
def MKPower(x1,order=1):
    gc = []
    modelStr = "(1+"
    arglist = r.RooArgList()
    arglist.add(x1)
    gc.append(x1)
    argnum = 0
    for i in range(order):
        coef_power=r.RooRealVar("coef_power%d"%i,"coef_power%d"%i,0.1,-1,1)
        coef=r.RooRealVar("coef%d"%i,"coef%d"%i,0.1,-1,1)
        gc.append(coef_power)
        arglist.add(coef_power)
        argnum += 1
        gc.append(coef)
        arglist.add(coef)
        argnum += 1
        modelStr += "@%d*pow(@0,@%d)+"%(argnum,argnum-1)
    modelStr = modelStr[:-1] 
    modelStr += ")"
    print(modelStr)
    model = r.RooGenericPdf("model","model",modelStr,arglist)
    gc.append(model)
    return model, gc
def MKLegendre(x1,order=[1,2]):
    gc = []
    modelStr = "(1+"
    arglist = r.RooArgList()
    argnum = -1
    for i in order:
        leg = r.RooLegendre("leg%d"%i, "leg%d"%i, x1 ,i)
        coef=r.RooRealVar("coef%d"%i,"coef%d"%i,0.1,-1,1)
        gc.append(leg)
        arglist.add(leg)
        argnum += 1
        gc.append(coef)
        arglist.add(coef)
        argnum += 1
        modelStr += "@%d*@%d+"%(argnum-1,argnum)
    modelStr = modelStr[:-1] 
    modelStr += ")"
    print(modelStr)
    model = r.RooGenericPdf("model","model",modelStr,arglist)
    gc.append(model)
    return model, gc
def MKExp(x1):
    gc = []
    arglist = r.RooArgList()
    arglist.add(x1)
    gc.append(x1)
    a1 = r.RooRealVar("a1","a1",1.6,0,10)
    b1 = r.RooRealVar("b1","b2",0.1,0,10)
    a1.setConstant()
    for e in [a1,b1]:
        gc.append(e)
        arglist.add(e)
    model = r.RooGenericPdf("model","model","1+@1*exp(-1*@2*@0)",arglist)
    gc.append(model)
    return model, gc
def MKBernstein(x2,order=2):
    gc = []
    arglist = r.RooArgList()
    for i in range(order+1):
        coef = r.RooRealVar("coef%d"%i,"coef%d"%i,1.0/2**i,-1.0,1.0) 
        gc.append(coef)
        arglist.add(coef)
    model = r.RooBernstein("model","model",x2,arglist)
    gc.append(model)
    return model, gc
# --------------------------
# | PDFs for signal models |
# --------------------------
def MKTripleGauss(x):
    gc = []
    arglist = r.RooArgList()
    meanG1 = r.RooRealVar("MeanG1", "MeanG1", 125, 122, 128)
    meanG2 = r.RooRealVar("MeanG2", "MeanG2", 125, 110, 160)
    meanG3 = r.RooRealVar("MeanG3", "MeanG3", 120, 0, 300)
    widthG1 = r.RooRealVar("WidthG1", "WidthG1", 1, 0, 5.)
    widthG2 = r.RooRealVar("WidthG2", "WidthG2", 10, 0., 10000.)
    widthG3 = r.RooRealVar("WidthG3", "WidthG3", 10, 0., 10000.)
    coefG1 = r.RooRealVar("coefG1",  "coefG1", 0.8,0.,1.)
    coefG2 = r.RooRealVar("coefG2",  "coefG2", 0.1,0.,1.)
    gaus1 = r.RooGaussian("gaus1", "gaus1", x, meanG1, widthG1)
    gaus2 = r.RooGaussian("gaus2", "gaus2", x, meanG2, widthG2)
    gaus3 = r.RooGaussian("gaus3", "gaus3", x, meanG3, widthG3)
    for e in [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2, gaus1, gaus2, gaus3]:
        gc.append(e)
    model = r.RooAddPdf('model', 'model', r.RooArgList(gaus1, gaus2, gaus3), r.RooArgList(coefG1,coefG2))
    return model, [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2], gc 
