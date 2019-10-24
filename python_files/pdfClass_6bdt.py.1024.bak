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
        self.name = "MKBwz"
        self.p = {}
        self.p["a1"] = ["a1", "mass", -0.87, -10.0, 10.0, True]
        self.p["a2"] = ["a2", "width", 0.1, -10.0, 10.0, False]
        self.p["a3"] = ["a3", "exp", 0.1, -10.0, 10.0, False]
    def makeModel(self,x):
        model_name = 'MKBwz'
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        rrvs = {}
        rrvs["a1"] = r.RooRealVar(*self.p["a1"][0:5]) #  mass
        rrvs["a2"] = r.RooRealVar(*self.p["a2"][0:5]) # width
        rrvs["a3"] = r.RooRealVar(*self.p["a3"][0:5]) # exp
        #a1.setConstant()
        for e in [self.p["a1"], self.p["a2"], self.p["a3"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooGenericPdf(self.name, self.name, "@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))", arglist)
        return model, gc
# fold
class MKPower:
    def __init__(self):
        self.name = 'MKPower'
        self.p = {}
        self.p['pow0'] = ["pow","pow",1.0, -10.0, 10.0, False]
        self.p['c0'] = ["c0", "c0", 1.0, -10.0, 10.0, False]
    def makeModel(self,x1,order=1):
        gc = []
        modelStr = "("
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        argnum = 0
        for i in range(order):
            coef_power=r.RooRealVar(*self.p["pow%d"%i][0:5])
            if self.p["pow%d"%i][5] == True:
                coef_power.setConstant()
            coef=r.RooRealVar(*self.p["c%d"%i][0:5])
            if self.p["c%d"%i][5] == True:
                coef.setConstant()
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
        model = r.RooGenericPdf(self.name, self.name,modelStr,arglist)
        gc.append(model)
        return model, gc
# fold
class MKPower_inc:
    def __init__(self):
        self.name = 'MKPower'
        self.p = {}
        self.p['pow0'] = ["pow0","pow0",0.0,-10.0,10.0,False]
        self.p['c0'] = ["c0","c0",1.0,-10.0,10.0,False]
        self.p['pow1'] = ["pow1","pow1",1.0,-10.0,10.0,False]
        self.p['c1'] = ["c1","c1",1.0/2,-10.0,10.0, False]
    def makeModel(self,x1,order=1):
        gc = []
        modelStr = "(1+"
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        argnum = 0
        for i in range(order):
            coef_power=r.RooRealVar(*self.p["pow%d"%i][0:5])
            if self.p["pow%d"%i][5] == True:
                coef_power.setConstant()
            coef=r.RooRealVar(*self.p["c%d"%i][0:5])
            if self.p["c%d"%i][5] == True:
                coef.setConstant()
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
        model = r.RooGenericPdf(self.name, self.name,modelStr,arglist)
        gc.append(model)
        return model, gc
# fold
class MKLegendre:
    def __init__(self):
        self.name = "MKLegendre"
        self.p = {}
        self.p['coef1'] = ["coef1","coef1",1/2**1,-10.0,10.0,False]
        self.p['coef2'] = ["coef2","coef2",1/2**2, -10.0, 10.0, False]
        self.p['coef3'] = ["coef3", "coef3", 1/2**3, -10.0, 10.0, False]
    def makeModel(self,x1,order=[1,2]):
        gc = []
        modelStr = "(1+"
        arglist = r.RooArgList()
        argnum = -1
        for i in order:
            leg = r.RooLegendre("leg%d"%i, "leg%d"%i, x1 ,i)
            coef=r.RooRealVar(*self.p["coef%d"%i][0:5])
            if self.p["coef%d"%i][5] == True:
                coef.setConstant()
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
        model = r.RooGenericPdf(self.name, self.name, modelStr,arglist)
        gc.append(model)
        return model, gc

class MKExp:
    def __init__(self):
        self.name = 'MKExp'
        self.p = {}
        self.p['a1'] = ["a1", "a1", 1.6, 0.0, 10.0, False]
        self.p['b1'] = ["b1", "b1", 0.1, 0.0, 10.0, False]
    def makeModel(self,x1):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        rrvs = {}
        rrvs['a1'] = r.RooRealVar(*self.p["a1"][0:5]) # term coef 
        rrvs['b1'] = r.RooRealVar(*self.p["b1"][0:5]) # exp coef
        for e in [self.p['a1'], self.p['b1']]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooGenericPdf(self.name, self.name,"@1*exp(-1*@2*@0)",arglist)
        gc.append(model)
        return model, gc
# fold
class MKExp2:
    def __init__(self):
        self.name = 'MKExp2'
        self.p = {}
        self.p['a1'] = ["a1", "a1", 1.6, 0.0, 10.0, False]
        self.p['b1'] = ["b1", "b1", 0.1, 0.0, 10.0, False]
        self.p['a2'] = ["a2", "a2", 0.8, 0.0, 10.0, False]
        self.p['b2'] = ["b2", "b2", 0.01, 0.0, 10.0, False]
    def makeModel(self,x1):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x1)
        gc.append(x1)
        rrvs = {}
        rrvs["a1"] = r.RooRealVar(*self.p["a1"][0:5]) # term coef 
        rrvs["b1"] = r.RooRealVar(*self.p["b1"][0:5]) # exp coef
        rrvs["a2"] = r.RooRealVar(*self.p["a2"][0:5]) # term coef 
        rrvs["b2"] = r.RooRealVar(*self.p["b2"][0:5]) # exp coef
        #a1.setConstant()
        for e in [self.p["a1"],self.p["b1"],self.p["a2"],self.p["b2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooGenericPdf(self.name, self.name,"1+@1*exp(-1*@2*@0)+@3*exp(-1*@4*@0)",arglist)
        gc.append(model)
        return model, gc
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
        self.name = 'MKBernstein'
        self.par = {}
        self.p['coef0'] = ["coef0","coef0", 1.0/2**0, -1.0, 1.0, True]
        self.p['coef1'] = ["coef1", "coef1", 1.0/2**1, -1.0, 1.0, False]
        self.p['coef2'] = ["coef2", "coef2", 1.0/2**2, -1.0, 1.0, False]
        self.p['coef3'] = ["coef3", "coef3", 1.0/2**3, -1.0, 1.0, False]
    def makeModel(self,x2):
        gc = []
        arglist = r.RooArgList()
        rrvs = {}
        rrvs["coef0"] = r.RooRealVar(*self.p["coef0"][0:5]) 
        rrvs["coef1"] = r.RooRealVar(*self.p["coef1"][0:5]) 
        rrvs["coef2"] = r.RooRealVar(*self.p["coef2"][0:5])
        rrvs["coef3"] = r.RooRealVar(*self.p["coef3"][0:5])
        #rrvs["coef4"] = r.RooRealVar(*self.p["coef4"][0:5])
        #rrvs["coef0"].setConstant()
        for e in [self.p["coef0"], self.p["coef1"], self.p["coef2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooBernstein(self.name, self.name, x2, arglist)
        gc.append(model)
        return model, gc
class MKBernstein3:
    def __init__(self):
        self.name = 'MKBernstein'
        self.p = {}
        self.p['coef0'] = ["coef0","coef0", 1.0/2**0, -1.0, 1.0, True]
        self.p['coef1'] = ["coef1", "coef1", 1.0/2**1, -1.0, 1.0, False]
        self.p['coef2'] = ["coef2", "coef2", 1.0/2**2, -1.0, 1.0, False]
        self.p['coef3'] = ["coef3", "coef3", 1.0/2**3, -1.0, 1.0, False]
    def makeModel(self,x2):
        gc = []
        arglist = r.RooArgList()
        rrvs = {}
        rrvs["coef0"] = r.RooRealVar(*self.p["coef0"][0:5]) 
        rrvs["coef1"] = r.RooRealVar(*self.p["coef1"][0:5]) 
        rrvs["coef2"] = r.RooRealVar(*self.p["coef2"][0:5])
        rrvs["coef3"] = r.RooRealVar(*self.p["coef3"][0:5])
        #rrvs["coef4"] = r.RooRealVar(*self.p["coef4"][0:5])
        #rrvs["coef0"].setConstant()
        for e in [self.p["coef0"], self.p["coef1"], self.p["coef2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooBernstein(self.name, self.name, x2, arglist)
        gc.append(model)
        return model, gc
# fold
class MKBernstein2_inc:
    def __init__(self):
        self.name = 'MKBernstein'
        self.p = {}
        self.p['coef0'] = ["coef0","coef0", 0.7, 0.7-3*1.0, 0.7+3*1.0, False]
        self.p['coef1'] = ["coef1", "coef1", 0.13, 0.13-3*0.26, 0.13+3*0.26, False]
        self.p['coef2'] = ["coef2", "coef2", 0.31, 0.31-3*0.49, 0.31+3*0.49, False]
        self.p['coef3'] = ["coef3", "coef3", 0.12, 0.12-3*0.22, 0.12+3*0.22, False]
        self.p['coef4'] = ["coef4", "coef4", 0.14, 0.14-3*0.21, 0.14+3*0.21, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        rrvs = {}
        rrvs["coef0"] = r.RooRealVar(*self.p['coef0'][0:5]) 
        rrvs["coef1"] = r.RooRealVar(*self.p['coef1'][0:5]) 
        rrvs["coef2"] = r.RooRealVar(*self.p['coef2'][0:5])
        rrvs["coef3"] = r.RooRealVar(*self.p['coef3'][0:5])
        rrvs["coef4"] = r.RooRealVar(*self.p['coef4'][0:5])
        for e in [self.p["coef0"], self.p["coef1"], self.p["coef2"], self.p["coef3"], self.p["coef4"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooBernstein(self.name, self.name, x, arglist)
        gc.append(model)
        return model, gc
# fold
class MKBwzredux:
    def __init__(self):
        self.name = 'MKBwzredux'
        self.p = {}
        self.p['pow'] = ["pow","pow", 1.544, -10.0, 10.0, True]
        self.p['ex1'] = ["ex1", "ex1", 2.3, -100.0, 100.0, False]
        self.p['ex2'] = ["ex2", "ex2", -0.59, -100.0, 100.0, False]
    def makeModel(self,x):
        gc = []
        rrvs = {}
        rrvs["pow"] = r.RooRealVar(*self.p['pow'][0:5]) #a1
        rrvs["ex1"] = r.RooRealVar(*self.p['ex1'][0:5]) #a2
        rrvs["ex2"] = r.RooRealVar(*self.p['ex2'][0:5]) #a3
        for e in [self.p["pow"], self.p["ex1"], self.p["ex2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            #arglist.add(rrvs[e[0]])
        f = r.RooFormulaVar("f", "(@1*(@0/100)+@2*(@0/100)^2)", r.RooArgList(x, rrvs["ex1"], rrvs["ex2"]))
        gc.append(f)
        model = r.RooGenericPdf(self.name, self.name, "exp(@2)*(2.5)/(pow(@0-91.2,@1)+pow(2.5/2,@1))", r.RooArgList(x, rrvs["pow"], f))
        return model, gc
class MKBwzredux2:
    def __init__(self):
        self.name = 'MKBwzredux'
        self.p = {}
        self.p['pow'] = ["pow","pow", 1.544, -10.0, 10.0, True]
        self.p['ex1'] = ["ex1", "ex1", 2.3, -100.0, 100.0, False]
        self.p['ex2'] = ["ex2", "ex2", -0.59, -100.0, 100.0, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        rrvs = {}
        rrvs["pow"] = r.RooRealVar(*self.p['pow'][0:5]) #a1
        rrvs["ex1"] = r.RooRealVar(*self.p['ex1'][0:5]) #a2
        rrvs["ex2"] = r.RooRealVar(*self.p['ex2'][0:5]) #a3
        for e in [self.p["pow"], self.p["ex1"], self.p["ex2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooGenericPdf(self.name, self.name, "exp(@2*(@0/100)+@3*(@0/100)^2)*(2.5)/(pow(@0-91.2,@1)+pow(2.5/2,@1))", arglist)
        return model, gc


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
