import ROOT as r
from ROOT import RooFit as rf

# ---------------------
# | Background Models |
# ---------------------
# Bwz
# Power
# Legendre
# Exp
# Exp2
# Bernstein
# Bernstein2
# Bwzredux

class MKBwz:
    def __init__(self):
        self.d_par = {}
        self.d_par['a1_i'] = -0.87 # i: initial
        self.d_par['a1_n'] = -10.0 # n: min
        self.d_par['a1_x'] = 10.0 # x: max
        self.d_par['a2_i'] = 0.1 
        self.d_par['a2_n'] = -10.0
        self.d_par['a2_x'] = 10.0
        self.d_par['a3_i'] = 0.1
        self.d_par['a3_n'] = -10.0
        self.d_par['a3_x'] = 10.0
    def makeModel(self,x):
        model_name = 'MKBwz'
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        a1 = r.RooRealVar("a1", "a1", self.d_par['a1_i'], self.d_par['a1_n'], self.d_par['a1_x']) #  mass
        a2 = r.RooRealVar("a2", "a2", self.d_par['a2_i'], self.d_par['a2_n'], self.d_par['a2_x']) # width
        a3 = r.RooRealVar("a3", "a3", self.d_par['a3_i'], self.d_par['a3_n'], self.d_par['a3_x']) # exp
        a1.setConstant()
        for e in [a1,a2,a3]:
            gc.append(e)
            arglist.add(e)
        model = r.RooGenericPdf(model_name, model_name, "@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))", arglist)
        return model, gc
    def setParam(self,parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

class MKPower:
    def __init__(self):
        self.d_par = {}
        self.d_par['pow0_i'] = 0.0
        self.d_par['pow0_n'] = -10.0
        self.d_par['pow0_x'] = 10.0
        self.d_par['c0_i'] = 1.0 
        self.d_par['c0_n'] = -10.0
        self.d_par['c0_x'] = 10.0
        #self.d_par['a3_i'] = 0.1
        #self.d_par['a3_n'] = -10.0
        #self.d_par['a3_x'] = 10.0
    def makeModel(self,x1,order=1):
        model_name = 'MKPower'
        gc = []
        modelStr = "("
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        argnum = 0
        for i in range(order):
            coef_power=r.RooRealVar("pow%d"%i,"pow%d"%i,self.d_par['pow%d_i'%i],self.d_par['pow%d_n'%i],self.d_par['pow%d_x'%i])
            coef=r.RooRealVar("c%d"%i,"c%d"%i,self.d_par['c%d_i'%i],self.d_par['c%d_n'%i],self.d_par['c%d_x'%i])
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
        model = r.RooGenericPdf(model_name, model_name,modelStr,arglist)
        gc.append(model)
        return model, gc
    def setParam(self,parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

class MKLegendre:
    def __init__(self):
        self.d_par = {}
        self.d_par['coef1_i'] = 1/2**1 
        self.d_par['coef1_n'] = -10.0
        self.d_par['coef1_x'] = 10.0
        self.d_par['coef2_i'] = 1/2**2
        self.d_par['coef2_n'] = -10.0
        self.d_par['coef2_x'] = 10.0
        self.d_par['coef3_i'] = 1/2**3
        self.d_par['coef3_n'] = -10.0
        self.d_par['coef3_x'] = 10.0
    def makeModel(self,x1,order=[1,2]):
        model_name = 'MKLegendre'
        gc = []
        modelStr = "(1+"
        arglist = r.RooArgList()
        argnum = -1
        for i in order:
            leg = r.RooLegendre("leg%d"%i, "leg%d"%i, x1 ,i)
            coef=r.RooRealVar("coef%d"%i,"coef%d"%i, self.d_par['coef%d_i'%i], self.d_par['coef%d_n'%i], self.d_par['coef%d_x'%i])
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
        model = r.RooGenericPdf(model_name, model_name, modelStr,arglist)
        gc.append(model)
        return model, gc
    def setParam(self,parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

class MKExp:
    def __init__(self):
        self.d_par = {}
        self.d_par['a1_i'] = 1.6
        self.d_par['a1_n'] = 0.0
        self.d_par['a1_x'] = 10.0
        self.d_par['b1_i'] = 0.1 
        self.d_par['b1_n'] = 0.0
        self.d_par['b1_x'] = 10.0
        self.setconst = []
    def makeModel(self,x1):
        model_name = 'MKExp'
        gc = []
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        dyvar = {}
        dyvar['a1'] = r.RooRealVar("a1","a1",self.d_par['a1_i'],self.d_par['a1_n'],self.d_par['a1_x']) # term coef 
        dyvar['b1'] = r.RooRealVar("b1","b1",self.d_par['b1_i'],self.d_par['b1_n'],self.d_par['b1_x']) # exp coef
        for e in ['a1', 'b1']:
            if e in self.setconst:
                dyvar[e].setConstant()
            gc.append(dyvar[e])
            arglist.add(dyvar[e])
        model = r.RooGenericPdf(model_name, model_name,"1+@1*exp(-1*@2*@0)",arglist)
        gc.append(model)
        return model, gc
    def setParam(self,parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax
    def setConst(self,parname):
        self.setconst.append(parname)

class MKExp2:
    def __init__(self):
        self.d_par = {}
        self.d_par['a1_i'] = 1.6 
        self.d_par['a1_n'] = 0.0
        self.d_par['a1_x'] = 10.0
        self.d_par['b1_i'] = 0.1 
        self.d_par['b1_n'] = 0.0
        self.d_par['b1_x'] = 10.0
        self.d_par['a2_i'] = 0.8
        self.d_par['a2_n'] = 0.0
        self.d_par['a2_x'] = 10.0
        self.d_par['b2_i'] = 0.01
        self.d_par['b2_n'] = 0.0
        self.d_par['b2_x'] = 10.0
    def makeModel(self,x1):
        model_name = 'MKExp2'
        gc = []
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        a1 = r.RooRealVar("a1","a1",self.d_par['a1_i'],self.d_par['a1_n'],self.d_par['a1_x']) # term coef 
        b1 = r.RooRealVar("b1","b1",self.d_par['b1_i'],self.d_par['b1_n'],self.d_par['b1_x']) # exp coef
        a2 = r.RooRealVar("a2","a2",self.d_par['a2_i'],self.d_par['a2_n'],self.d_par['a2_x']) # term coef 
        b2 = r.RooRealVar("b2","b2",self.d_par['b2_i'],self.d_par['b2_n'],self.d_par['b2_x']) # exp coef
        #a1.setConstant()
        for e in [a1,b1,a2,b2]:
            gc.append(e)
            arglist.add(e)
        model = r.RooGenericPdf(model_name, model_name,"1+@1*exp(-1*@2*@0)+@3*exp(-1*@4*@0)",arglist)
        gc.append(model)
        return model, gc
    def setParam(self, parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

class MKBernstein:
    def __init__(self):
        self.d_par = {}
        self.d_par['coef0_i'] = 1.0/2**0
        self.d_par['coef0_n'] = -1.0
        self.d_par['coef0_x'] = 1.0
        self.d_par['coef1_i'] = 1.0/2**1
        self.d_par['coef1_n'] = -1.0
        self.d_par['coef1_x'] = 1.0
        self.d_par['coef2_i'] = 1.0/2**2
        self.d_par['coef2_n'] = -1.0
        self.d_par['coef2_x'] = 1.0
        self.d_par['coef3_i'] = 1.0/2**3
        self.d_par['coef3_n'] = -1.0
        self.d_par['coef3_x'] = 1.0
    def makeModel(self,x2,order=2):
        model_name = 'MKBernstein'
        gc = []
        arglist = r.RooArgList()
        for i in range(order+1):
            coef = r.RooRealVar("coef%d"%i,"coef%d"%i,1.0/2**i,-1.0,1.0) 
            gc.append(coef)
            arglist.add(coef)
        model = r.RooBernstein(model_name, model_name, x2,arglist)
        gc.append(model)
        return model, gc
    def setParam(self, parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

class MKBernstein2:
    def __init__(self):
        self.d_par = {}
        self.d_par['coef0_i'] = 1.0/2**0
        self.d_par['coef0_n'] = -1.0
        self.d_par['coef0_x'] = 1.0
        self.d_par['coef1_i'] = 1.0/2**1
        self.d_par['coef1_n'] = -1.0
        self.d_par['coef1_x'] = 1.0
        self.d_par['coef2_i'] = 1.0/2**2
        self.d_par['coef2_n'] = -1.0
        self.d_par['coef2_x'] = 1.0
        self.d_par['coef3_i'] = 1.0/2**3
        self.d_par['coef3_n'] = -1.0
        self.d_par['coef3_x'] = 1.0
    def makeModel(self,x2):
        model_name = 'MKBernstein'
        gc = []
        arglist = r.RooArgList()
        coef0 = r.RooRealVar("coef0","coef0",1.0/2**0,1.0,1.0) 
        coef1 = r.RooRealVar("coef1","coef1",1.0/2**1,-1.0,1.0) 
        coef2 = r.RooRealVar("coef2","coef2",1.0/2**2,-1.0,1.0)
        coef0.setConstant()
        for e in [coef0, coef1, coef2]:
            gc.append(e)
            arglist.add(e)
        model = r.RooBernstein(model_name, model_name, x2, arglist)
        gc.append(model)
        return model, gc
    def setParam(self, parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax
class MKBernstein3:
    def __init__(self):
        self.d_par = {}
        self.d_par['c0_i'] = 1.0/2**0
        self.d_par['c0_n'] = -1.0
        self.d_par['c0_x'] = 1.0
        self.d_par['c1_i'] = 1.0/2**1
        self.d_par['c1_n'] = -1.0
        self.d_par['c1_x'] = 1.0
        self.d_par['c2_i'] = 1.0/2**2
        self.d_par['c2_n'] = -1.0
        self.d_par['c2_x'] = 1.0
        self.d_par['c3_i'] = 1.0/2**3
        self.d_par['c3_n'] = -1.0
        self.d_par['c3_x'] = 1.0
        self.setconst=[]
    def makeModel(self,x2,orders=["c0","c1","c2","c3"]):
        model_name = 'MKBernstein'
        gc = []
        arglist = r.RooArgList()
        cvars = {}
        for e in orders:
            cvars[e] = r.RooRealVar(e, e, self.d_par[e+'_i'], self.d_par[e+'_n'], self.d_par[e+'_x'])
            if e in self.setconst:
                cvars[e].setConstant()
            gc.append(cvars[e])
            arglist.add(cvars[e])
        model = r.RooBernstein(model_name, model_name, x2, arglist)
        gc.append(model)
        return model, gc
    def setParam(self, parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax
    def setConst(self,parname):
        self.setconst.append(parname)

class MKBwzredux:
    def __init__(self):
        self.d_par = {}
        self.d_par['pow_i'] = 1.544 
        self.d_par['pow_n'] = 0 
        self.d_par['pow_x'] = 10.0
        self.d_par['ex1_i'] = 2.3
        self.d_par['ex1_n'] = -100.0
        self.d_par['ex1_x'] = 100.0
        self.d_par['ex2_i'] = -0.59
        self.d_par['ex2_n'] = -100.0
        self.d_par['ex2_x'] = 100.0
    def makeModel(self,x):
        model_name = 'MKBwzredux'
        gc = []
        a1 = r.RooRealVar("pow", "pow", self.d_par['pow_i'], self.d_par['pow_n'], self.d_par['pow_x'])
        a2 = r.RooRealVar("ex1", "ex1", self.d_par['ex1_i'], self.d_par['ex1_n'], self.d_par['ex1_x'])
        a3 = r.RooRealVar("ex2", "ex2", self.d_par['ex2_i'], self.d_par['ex2_n'], self.d_par['ex2_x'])
        for e in [a1,a2,a3]:
            gc.append(e)
            # arglist.add(e)
        #a1.setConstant()
        #a2.setConstant()
        #a3.setConstant()
        f = r.RooFormulaVar("f", "(@1*(@0/100)+@2*(@0/100)^2)", r.RooArgList(x, a2, a3))
        gc.append(f)
        model = r.RooGenericPdf(model_name, model_name, "exp(@2)*(2.5)/(pow(@0-91.2,@1)+pow(2.5/2,@1))", r.RooArgList(x, a1, f))
        return model, gc
    def setParam(self, parname, pini, pmin, pmax):
        self.d_par[parname+"_i"] = pini
        self.d_par[parname+"_n"] = pmin
        self.d_par[parname+"_x"] = pmax

# ----------------
# | Signal Model |
# ----------------
def MKTripleGauss(x):
    gc = []
    arglist = r.RooArgList()
    meanG1 = r.RooRealVar("MeanG1", "MeanG1", 125, 122, 128)
    meanG2 = r.RooRealVar("MeanG2", "MeanG2", 160, 110, 160)
    meanG3 = r.RooRealVar("MeanG3", "MeanG3", 110, 0, 110)
    widthG1 = r.RooRealVar("WidthG1", "WidthG1", 1, 0, 10.)
    widthG2 = r.RooRealVar("WidthG2", "WidthG2", 10, 0., 100.)
    widthG3 = r.RooRealVar("WidthG3", "WidthG3", 100, 0., 1000.)
    coefG1 = r.RooRealVar("coefG1",  "coefG1", 0.5,0.5,1.0)
    coefG2 = r.RooRealVar("coefG2",  "coefG2", 0.25,0.,0.5)
    gaus1 = r.RooGaussian("gaus1", "gaus1", x, meanG1, widthG1)
    gaus2 = r.RooGaussian("gaus2", "gaus2", x, meanG2, widthG2)
    gaus3 = r.RooGaussian("gaus3", "gaus3", x, meanG3, widthG3)
    for e in [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2, gaus1, gaus2, gaus3]:
        gc.append(e)
    model = r.RooAddPdf('model', 'model', r.RooArgList(gaus1, gaus2, gaus3), r.RooArgList(coefG1,coefG2))
    return model, [meanG1, meanG2, meanG3, widthG1, widthG2, widthG3, coefG1, coefG2], gc 
