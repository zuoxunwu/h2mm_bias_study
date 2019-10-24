import ROOT as r

# define custon pdfs (models)


# Legendre
# --------

def MKLegendre_o(x):
    gc = []
    modelStr = "(0.1+"
    arglist = r.RooArgList()
    argnum = -1
    for i in [1,2,3,5,7,9]:
        leg = r.RooLegendre("leg%d"%i, "leg%d"%i, x ,i)
        coef=r.RooRealVar("coef%d"%i,"coef%d"%i,0,-10,10)
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


def bwZreduxFixed(x):
    a1 = r.RooRealVar("bwz_redux_a1", "a1", 0, -10, 10) # power in denominater
    a2 = r.RooRealVar("bwz_redux_a2", "a2", 0, -10, 10) # x
    a3 = r.RooRealVar("bwz_redux_a3", "a3", 0, -10, 10) # x^2

    #a1.setConstant()
    #a2.setConstant()
    #a3.setConstant()

    f = r.RooFormulaVar("bwz_redux_f", "(@1*((30*@0+150)/100)+@2*((30*@0+150)/100)^2)", r.RooArgList(x, a2, a3))
    #expmodel = RooGenericPdf("bwz_redux_model", "exp(@2)*(2.5)/(pow(@0-91.2,@1)+0.25*pow(2.5,@1))", RooArgList(x, a1,     f))
    expmodel = r.RooGenericPdf("bwz_redux_model", "bwz_redux_model", "exp(@2)*(2.5)/(pow((30*@0+150)-91.2,@1)+pow(2.5/    2,@1))", r.RooArgList(x, a1, f))
    return expmodel, [a1, a2, a3, f]
 
