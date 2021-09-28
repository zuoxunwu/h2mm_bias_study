import ROOT as r
from ROOT import RooFit as rf
r.gSystem.Load("/afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/tmp/slc6_amd64_gcc530/src/HiggsAnalysis/CombinedLimit/src/HiggsAnalysisCombinedLimit/libHiggsAnalysisCombinedLimit.so")

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
        self.p["a1"] = ["a1", "mass", 91, -1000.0, 1000.0, True]
        self.p["a2"] = ["a2", "width", 2.5, -100.0, 100.0, True]
        self.p["a3"] = ["a3", "exp", 0.1, -100.0, 100.0, False]
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
        model = r.RooGenericPdf(self.name, self.name, "@2*exp(@3*@0/100)/(pow(@0-@1,2)+pow(@2/2.0,2))", arglist)
        return model, gc

class MKBwzGamma:
    def __init__(self):
       self.name = 'MKBwzGamma'
       self.p = {}
       self.p['pow0'] = ["pow0", "pow0", 2,   -100.0, 100.0, False] # @1
       self.p['f0']   = ["f0",   "f0",   0.1, -10.0,  10.0, False] # @2
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        for e in [self.p["pow0"], self.p["f0"]]:
            temp = r.RooRealVar(*self.p[e[0]][0:5])
            if e[5] == True:
                temp.setConstant()
            gc.append(temp)
            arglist.add(temp)
        model = r.RooGenericPdf(self.name, self.name, "2.5*exp(@1*@0/100)/(pow(@0-91,2)+pow(2.5/2.0,2)) + 1000*@2*@2*exp(@1*@0)/pow(@0,2)", arglist)
        return model, gc

class MKBwzredux_mod:
    def __init__(self):
        self.name = 'MKBwzredux'
        self.p = {}
        self.p['pow'] = ["pow","pow", 2, 0, 10.0, False] # @1
        self.p['ex1'] = ["ex1", "ex1", 0.5, -10, 10, False] # @2
        self.p['ex2'] = ["ex2", "ex2", 0, -10, 10, False] # @3
        self.p['w'] = ["w", "width", 2.5, 1, 20, False] # @4
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        for e in [self.p["pow"], self.p["ex1"], self.p["ex2"], self.p["w"]]:
            temp = r.RooRealVar(*self.p[e[0]][0:5])
            if e[5] == True:
                temp.setConstant()
            gc.append(temp)
            arglist.add(temp)
        model = r.RooGenericPdf(self.name, self.name, "exp(@2*@2*(@0/100)+@3*@3*(@0/100)^2)*(@4)/(pow(@0-91,@1)+pow(@4/2.0,@1))", arglist)
        return model, gc

class MKBwzBern1:
    def __init__(self):
        self.name = "MKBwzBern1"
        self.p = {}
        self.p["mass"]  = ["mass", "mass", 91, -1000.0, 1000.0, True]
        self.p["width"] = ["width", "width", 2.5, -100.0, 100.0, True]
        self.p["exp"]   = ["exp", "exp", 0.1, -100.0, 100.0, False]
	self.p['c0']    = ["c0","c0", 1.0, -10, 10, True]
        self.p['c1']    = ["c1", "c1", 0, -10, 10, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        rrvs = {}
        rrvs["mass"]  = r.RooRealVar(*self.p["mass"][0:5]) #  mass
        rrvs["width"] = r.RooRealVar(*self.p["width"][0:5]) # width
        rrvs["exp"]   = r.RooRealVar(*self.p["exp"][0:5]) # exp
	rrvs["c0"] = r.RooRealVar(*self.p["c0"][0:5])
        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5])
        for e in [self.p["mass"], self.p["width"], self.p["exp"], self.p["c0"], self.p["c1"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
	bern_x = "(@0 -100)/150"
	model_str = "(@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))) * (@4*(1-%s) + (1+@5)*%s)" %(bern_x, bern_x)
        model = r.RooGenericPdf(self.name, self.name, model_str, arglist)
        return model, gc

class MKBwzBern2:
    def __init__(self):
        self.name = "MKBwzBern2"
        self.p = {}
        self.p["mass"]  = ["mass", "mass", 91, -1000.0, 1000.0, True]
        self.p["width"] = ["width", "width", 2.5, -100.0, 100.0, True]
        self.p["exp"]   = ["exp", "exp", 0.1, -100.0, 100.0, False]
        self.p['c0']    = ["c0", "c0", 1.0, -10, 10, True]
        self.p['c1']    = ["c1", "c1", 0, -10, 10, False]
	self.p['c2']    = ["c2", "c2", 0, -10, 10, False]
    def makeModel(self,x):
        gc = [] 
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        rrvs = {}
        rrvs["mass"]  = r.RooRealVar(*self.p["mass"][0:5]) #  mass
        rrvs["width"] = r.RooRealVar(*self.p["width"][0:5]) # width
        rrvs["exp"]   = r.RooRealVar(*self.p["exp"][0:5]) # exp
        rrvs["c0"] = r.RooRealVar(*self.p["c0"][0:5])
        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5])
	rrvs["c2"] = r.RooRealVar(*self.p["c2"][0:5])
        for e in [self.p["mass"], self.p["width"], self.p["exp"], self.p["c0"], self.p["c1"], self.p["c2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
	bern_x = "(@0 -100)/150"
        model_str = "(@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))) * (@4*pow(1-%s,2) + 2*(1+@5)*(1-%s)*%s + (1+@6)*pow(%s,2))" %(bern_x, bern_x, bern_x, bern_x)
        model = r.RooGenericPdf(self.name, self.name, model_str, arglist)
        return model, gc

class MKPower1:
    def __init__(self):
        self.name = 'MKPower1'
        self.p = {}
        self.p['pow0']  = ["pow0", "pow0", 0.0,-10.0,10.0,False]
        self.p['c0']    = ["c0",   "c0",   1.0,-10.0,10.0,True]
        self.p['const'] = ['const', 'const', 0, -10, 10, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        argnum = 0
	rrvs = {}
        rrvs['pow0']  = r.RooRealVar(*self.p['pow0'][0:5])
        rrvs['c0']    = r.RooRealVar(*self.p['c0'][0:5])
        rrvs['const'] = r.RooRealVar(*self.p['const'][0:5])
        for e in [self.p['pow0'], self.p['c0'], self.p['const']]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        modelStr = "pow((@0-100),@1)*@2*@2 + @3"
        model = r.RooGenericPdf(self.name, self.name,modelStr,arglist)
        gc.append(model)
        return model, gc

class MKPower2:
    def __init__(self):
        self.name = 'MKPower2'
        self.p = {}
        self.p['pow0']  = ["pow0","pow0", 0.0,-10.0,10.0,False]
        self.p['c0']    = ["c0",  "c0",   1.0,-10.0,10.0,True]
        self.p['pow1']  = ["pow1","pow1", 1.0,-10.0,10.0,False]
        self.p['c1']    = ["c1",  "c1",   1.0,-10.0,10.0,False]
	self.p['const'] = ['const', 'const', 0, -10, 10, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        argnum = 0
	rrvs = {}
	rrvs['pow0']  = r.RooRealVar(*self.p['pow0'][0:5]) 
	rrvs['c0']    = r.RooRealVar(*self.p['c0'][0:5])
	rrvs['pow1']  = r.RooRealVar(*self.p['pow1'][0:5])
	rrvs['c1']    = r.RooRealVar(*self.p['c1'][0:5])
	rrvs['const'] = r.RooRealVar(*self.p['const'][0:5])
	for e in [self.p['pow0'], self.p['c0'], self.p['pow1'], self.p['c1'], self.p['const']]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        modelStr = "pow((@0-100),@1)*@2*@2 + pow((@0-100),@3)*@4*@4 + @5"
        model = r.RooGenericPdf(self.name, self.name,modelStr,arglist)
        gc.append(model)
        return model, gc

class MKExp:
    def __init__(self, order, intercept):
	self.name = 'MKExp1'
	self.order = order
	self.intercept = intercept
        self.p = {}
	self.p['c0']   = ["c0",   "c0",   0, -10, 10.0, False]
        self.p['c1']   = ["c1",   "c1",   1.6, -100, 100.0, False] # this param not in use
        self.p['exp1'] = ["exp1", "exp1", 0.1, -100, 100.0, False]
        self.p['c2']   = ["c2",   "c2",   0.8, -100, 100.0, False]
        self.p['exp2'] = ["exp2", "exp2", 0.01, -100, 100.0, False]
    def makeModel(self, x):
	gc = []
        arglist = r.RooArgList()
	rrvs = {}
	rrvs['exp1'] = r.RooRealVar(*self.p['exp1'][0:5])	
	f_x = r.RooFormulaVar('f_x', '(@0-100)', r.RooArgList(x))
	gc.append(x)
	gc.append(rrvs['exp1'])
	gc.append(f_x)
	m_1 = r.RooExponential(self.name, self.name, f_x, rrvs['exp1'])
	gc.append(m_1)
	model = m_1
	if self.order == 2:
	  rrvs['exp2'] = r.RooRealVar(*self.p['exp2'][0:5])   
	  rrvs['c2']   = r.RooRealVar(*self.p['c2'][0:5])
	  f_c2 = r.RooFormulaVar('f_c2', '(@0*@0)', r.RooArgList(rrvs['c2']))
	  gc.append(rrvs['exp2'])
	  gc.append(rrvs['c2'])
	  gc.append(f_c2)
	  m_add = r.RooExponential('Exp2', 'Exp2', f_x, rrvs['exp2'])
	  self.name = 'MKExp2'
	  m_2 = r.RooAddPdf(self.name, self.name, model, m_add, f_c2)
	  gc.append(m_add)
	  gc.append(m_2)
	  model = m_2
	if self.intercept == True:
	  rrvs['c0'] = r.RooRealVar(*self.p['c0'][0:5])
	  f_c0 = r.RooFormulaVar('f_c0', '(@0*@0)', r.RooArgList(rrvs['c0']))
	  gc.append(rrvs['c0'])
	  gc.append(f_c0)
	  m_int = r.RooUniform('const', 'const', r.RooArgSet(r.RooArgList(f_x)))
	  self.name += 'int'
	  m_0 = r.RooAddPdf(self.name, self.name, model, m_int, f_c0)
	  gc.append(m_int)
	  gc.append(m_0)
	  model = m_0
	gc.append(model)
	return model, gc

class MKExp1:
    def __init__(self):
        self.name = 'MKExp1'
        self.p = {}
        self.p['const'] = ["const", "const", 0, -10, 10.0, False]
        self.p['c1']    = ["c1", "c1", 1, -10, 10.0, True]
        self.p['exp1']  = ["exp1", "exp1", 0.15, -100, 100.0, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        for e in [self.p['const'], self.p['c1'], self.p['exp1']]:
            temp = r.RooRealVar(*self.p[e[0]][0:5])
            if e[5] == True:
                temp.setConstant()
            gc.append(temp)
            arglist.add(temp)
        model = r.RooGenericPdf(self.name, self.name,"@1 + @2*@2*exp(-1*@3*(@0-100))",arglist)
        gc.append(model)
        return model, gc

# fold
class MKExp2:
    def __init__(self):
        self.name = 'MKExp2'
        self.p = {}
	self.p['const'] = ["const", "const", 0, -10, 10.0, False]
        self.p['c1']    = ["c1", "c1", 1, -100, 100.0, True]
        self.p['exp1']  = ["exp1", "exp1", 0.1, -100, 100.0, False]
        self.p['c2']    = ["c2", "c2", 0.8, -100, 100.0, False]
        self.p['exp2']  = ["exp2", "exp2", 0.01, -100, 100.0, False]
    def makeModel(self,x):
        gc = []
        arglist = r.RooArgList()
        arglist.add(x)
        gc.append(x)
        rrvs = {}
	rrvs["const"] = r.RooRealVar(*self.p["const"][0:5]) 
        rrvs["c1"]    = r.RooRealVar(*self.p["c1"][0:5]) # term c 
        rrvs["exp1"]  = r.RooRealVar(*self.p["exp1"][0:5]) # exp c
        rrvs["c2"]    = r.RooRealVar(*self.p["c2"][0:5]) # term c 
        rrvs["exp2"]  = r.RooRealVar(*self.p["exp2"][0:5]) # exp c
        for e in [self.p["const"],self.p["c1"],self.p["exp1"],self.p["c2"],self.p["exp2"]]:
            if e[5] == True:
                rrvs[e[0]].setConstant()
            gc.append(rrvs[e[0]])
            arglist.add(rrvs[e[0]])
        model = r.RooGenericPdf(self.name, self.name,"@1 + @2*@2*exp(-1*@3*(@0-100)) + @4*@4*exp(-1*@5*(@0-100))",arglist)
        gc.append(model)
        return model, gc


#class MKBernstein1:
#    def __init__(self):
#        self.name = 'MKBernstein1'
#        self.p = {}
#        self.p['c1'] = ["c1", "c1", 1.0/2**1, -10, 10, False]
#    def makeModel(self,x):
#        gc = []
#	coef = {}
#        arglist = r.RooArgList()
#        rrvs = {}
#        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5])
#        for e in [self.p["c1"]]:
#            if e[5] == True:
#                rrvs[e[0]].setConstant()
#	    coef[e[0]] = r.RooFormulaVar( "f_"+e[0], "@0*@0", r.RooArgList(rrvs[e[0]]) )
#            gc.append(coef[e[0]])
#            arglist.add(coef[e[0]])
#        model = r.RooBernsteinFast(1)(self.name, self.name, x, arglist) #RooBernsteinFast maps x to [0,1]
#        gc.append(model)
#        return model, gc
#class MKBernstein2:
#    def __init__(self):
#        self.name = 'MKBernstein2'
#        self.p = {}
#        #self.p['c0'] = ["c0","c0", 1.0/2**0, -10, 10, True]
#        self.p['c1'] = ["c1", "c1", 1.0/2**1, -10, 10, False]
#        self.p['c2'] = ["c2", "c2", 1.0/2**2, -10, 10, False]
#    def makeModel(self,x):
#        gc = []
#	coef = {}
#        arglist = r.RooArgList()
#        rrvs = {}
#        #rrvs["c0"] = r.RooRealVar(*self.p["c0"][0:5]) 
#        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5]) 
#        rrvs["c2"] = r.RooRealVar(*self.p["c2"][0:5])
#        for e in [ self.p["c1"], self.p["c2"]]:
#            if e[5] == True:
#                rrvs[e[0]].setConstant()
#	    coef[e[0]] = r.RooFormulaVar( "f_"+e[0], "@0*@0", r.RooArgList(rrvs[e[0]]) )
#            gc.append(coef[e[0]])
#	    gc.append(rrvs[e[0]])
#            arglist.add(coef[e[0]])
#        model = r.RooBernsteinFast(2)(self.name, self.name, x, arglist) #RooBernstein maps x to [0,1]
#        gc.append(model)
#        return model, gc
#class MKBernstein3:
#    def __init__(self):
#        self.name = 'MKBernstein3'
#        self.p = {}
#        #self.p['c0'] = ["c0", "c0", 1.0/2**0, -10, 10, True]
#        self.p['c1'] = ["c1", "c1", 1.0/2**1, -10, 10, False]
#        self.p['c2'] = ["c2", "c2", 1.0/2**2, -10, 10, False]
#        self.p['c3'] = ["c3", "c3", 1.0/2**3, -10, 10, False]
#    def makeModel(self,x):
#        gc = []
#	coef = {}
#        arglist = r.RooArgList()
#        rrvs = {}
#        #rrvs["c0"] = r.RooRealVar(*self.p["c0"][0:5]) 
#        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5]) 
#        rrvs["c2"] = r.RooRealVar(*self.p["c2"][0:5])
#        rrvs["c3"] = r.RooRealVar(*self.p["c3"][0:5])
#        for e in [ self.p["c1"], self.p["c2"], self.p["c3"]]:
#            if e[5] == True:
#                rrvs[e[0]].setConstant()
#	    coef[e[0]] = r.RooFormulaVar( "f_"+e[0], "@0*@0", r.RooArgList(rrvs[e[0]]) )
#            gc.append(coef[e[0]])
#            arglist.add(coef[e[0]])
#        model = r.RooBernsteinFast(3)(self.name, self.name, x, arglist)
#        gc.append(model)
#        return model, gc
class MKBernsteinFast:
    def __init__(self, order):  # order = 1,2,3,4
        self.name = 'MKBernstein%d' %order
	self.order = order
        self.p = {}
        self.p['c1'] = ["c1", "c1", 1.0/2**1, -10, 10, False]
        self.p['c2'] = ["c2", "c2", 1.0/2**2, -10, 10, False]
        self.p['c3'] = ["c3", "c3", 1.0/2**3, -10, 10, False]
	self.p['c4'] = ["c4", "c4", 1.0/2**4, -10, 10, False]
    def makeModel(self,x):
        gc = []
	coef = {}
        arglist = r.RooArgList()
        rrvs = {}
        rrvs["c1"] = r.RooRealVar(*self.p["c1"][0:5])
        rrvs["c2"] = r.RooRealVar(*self.p["c2"][0:5])
        rrvs["c3"] = r.RooRealVar(*self.p["c3"][0:5])
	rrvs["c4"] = r.RooRealVar(*self.p["c4"][0:5])
        for i in range(self.order):
            if self.p['c%d' %(i+1)][5] == True:
                rrvs['c%d'%(i+1)].setConstant()
	    coef['c%d'%(i+1)] = r.RooFormulaVar( "f_c%d"%(i+1), "@0*@0", r.RooArgList(rrvs['c%d'%(i+1)]) )
    	    gc.append(coef['c%d'%(i+1)])
            gc.append(rrvs['c%d'%(i+1)])
            arglist.add(coef['c%d'%(i+1)])
        model = r.RooBernsteinFast(self.order)(self.name, self.name, x, arglist)
        gc.append(model)
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
