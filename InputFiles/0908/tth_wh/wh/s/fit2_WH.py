import ROOT as r
from ROOT import RooFit as rf

# load input file and histogram
f = r.TFile("StackPlots_WH.root")
choice1 = 3
if choice1 == 1:
    h = f.Get("H_pair_mass_zoomH_Net_Bkg")
elif choice1 == 2:
    h = f.Get("H_pair_mass_BDT_n10_n02_zoomH_Net_Bkg")
elif choice1 == 3:
    h = f.Get("H_pair_mass_BDT_n02_p02_zoomH_Net_Bkg")
elif choice1 == 4:
    h = f.Get("H_pair_mass_BDT_p02_p06_zoomH_Net_Bkg")
elif choice1 == 5:
    h = f.Get("H_pair_mass_BDT_p06_p10_zoomH_Net_Bkg")

# define x variable (dimuon mass); convert histo in x
x = r.RooRealVar("x","x",125,110,160)
x1 = r.RooFormulaVar("x1","x1","(@0-135)/50",r.RooArgList(x))
x2 = r.RooFormulaVar("x2","x2","(@0-105)/20",r.RooArgList(x))
#x2 = r.RooFormulaVar("x2","x2","(@0-110)/50",r.RooArgList(x))
x3 = r.RooFormulaVar("x3","x3","(@0-60)/50",r.RooArgList(x))
# convert TH1 to RooDataHist
dh = r.RooDataHist("dh","dh",r.RooArgList(x),h)

# plot
#r.gStyle.SetOptFit(1011)
frame1 = x.frame(rf.Title("WH background MC"))
dh.plotOn(frame1)


def MKBwz(x):
    model_name = 'MKBwz'
    gc = []
    arglist = r.RooArgList()
    arglist.add(x1)
    gc.append(x1)
    a1 = r.RooRealVar("a1", "a1", -0.87, -10.0, 10.0) #  mass
    a2 = r.RooRealVar("a2", "a2", 0.1, -10.0, 10.0) # width
    a3 = r.RooRealVar("a3", "a3", 0.1, -10.0, 10.0) # exp
    a1.setConstant()
    for e in [a1,a2,a3]:
        gc.append(e)
        arglist.add(e)
    model = r.RooGenericPdf(model_name, model_name, "@2*exp(@3*@0)/(pow(@0-@1,2)+pow(@2,2))", arglist)
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
        coef_power=r.RooRealVar("coef_power%d"%i,"coef_power%d"%i,0.1,-10,10)
        coef=r.RooRealVar("coef%d"%i,"coef%d"%i,1/2**i,-1,1)
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
    model = r.RooGenericPdf("model3","model3",modelStr,arglist)
    gc.append(model)
    return model, gc
def MKExp(x1):
    gc = []
    arglist = r.RooArgList()
    arglist.add(x1)
    gc.append(x1)
    a1 = r.RooRealVar("a1","a1",1.6,0,10) # term coef 
    b1 = r.RooRealVar("b1","b2",0.1,0,10) # exp coef
    a1.setConstant()
    #a1.setConstant()
    for e in [a1,b1]:
        gc.append(e)
        arglist.add(e)
    model = r.RooGenericPdf("model4","model4","1+@1*exp(-1*@2*@0)",arglist)
    gc.append(model)
    return model, gc
def MKBernstein(x2,order=2):
    gc = []
    arglist = r.RooArgList()
    for i in range(order+1):
        coef = r.RooRealVar("coef%d"%i,"coef%d"%i,1.0/2**i,-1.0,1.0) 
        gc.append(coef)
        arglist.add(coef)
    model = r.RooBernstein("model5","model5",x2,arglist)
    gc.append(model)
    return model, gc
# model choice
model1, gc1 = MKBwz(x1)
model2, gc = MKPower(x2,order=1)
model3, gc3 = MKLegendre(x1,order=[1,2,3])
model4, gc4 = MKExp(x1)
model5, gc5 = MKBernstein(x,order=3)

# Canvas
c = r.TCanvas("c", "c",800,800)
pad1 = r.TPad("pad1","pad1",0.0,0.25,1.0,1.0)
pad1.Draw()
pad1.cd()
# fit 
model1.fitTo(dh, rf.Range(110,160))
model1.plotOn(frame1, rf.LineColor(r.kBlue), rf.Name("MKBwz"))
#model1.paramOn(frame1)
model2.fitTo(dh, rf.Range(110,160))
model2.plotOn(frame1, rf.LineColor(r.kMagenta), rf.Name("MKPower"))
#model2.paramOn(frame1)
model3.fitTo(dh, rf.Range(110,160))
model3.plotOn(frame1, rf.LineColor(r.kGreen), rf.Name("MKLegendre"))
model4.fitTo(dh, rf.Range(110,160))
model4.plotOn(frame1,rf.LineColor(r.kRed), rf.Name("MKExp"))
#model4.paramOn(frame1)
model5.fitTo(dh, rf.Range(110,160))
model5.plotOn(frame1,rf.LineColor(r.kYellow), rf.Name("MKBernstein"))
frame1.Draw()
legend = r.TLegend(0.7,0.7,0.9,0.9)
legend.AddEntry(frame1.findObject("MKBwz"),"bwZ")
legend.AddEntry(frame1.findObject("MKPower"),"Power Law")
legend.AddEntry(frame1.findObject("MKLegendre"),"Legendre order 2")
legend.AddEntry(frame1.findObject("MKExp"),"Exponential")
legend.AddEntry(frame1.findObject("MKBernstein"),"Bernstein order 2")
legend.Draw()

# lower pad
c.cd()
pad2 = r.TPad("pad2","pad2",0.0,0.0,1.0,0.25)
pad2.Draw()
pad2.cd()
frame2 = x.frame(rf.Title("ratio"),rf.Range(110,160))
nbin_hm = 1000
ymax_hm = 1.20
ymin_hm = 0.80
hm1 = model1.createHistogram("x",nbin_hm)
hm1_1 = model1.createHistogram("x",nbin_hm)
hm1_1.Divide(hm1_1)
hm1_1.SetMaximum(ymax_hm)
hm1_1.SetMinimum(ymin_hm)
hm1_1.SetLabelSize(0.1,"xy")
hm1_1.SetStats(r.kFALSE)
hm1_1.GetYaxis().SetTitle("model2/model1")
hm1_1.GetYaxis().CenterTitle(r.kTRUE)
hm1_1.GetYaxis().SetTitleOffset(0)
#r.gStyle.SetTitleFontSize(0.1)
hm1_1.GetYaxis().SetTitleFont(42)
hm1_1.GetYaxis().SetTitleSize(0.05)
hm1_1.SetTitle("")
#hm1_1.SetTitleSize(0.1,"y")
hm1_1.Draw()
hm1 = model1.createHistogram("x",nbin_hm)
hm2 = model2.createHistogram("x",nbin_hm)
hm2.Divide(hm1)
hm2.SetMaximum(ymax_hm)
hm2.SetMinimum(ymin_hm)
hm2.SetLineColor(r.kMagenta)
hm2.Draw("SAME")
hm3 = model3.createHistogram("x",nbin_hm)
hm3.Divide(hm1)
hm3.SetMaximum(ymax_hm)
hm3.SetMinimum(ymin_hm)
hm3.SetLineColor(r.kGreen)
hm3.Draw("same")
hm4 = model4.createHistogram("x",nbin_hm)
hm4.Divide(hm1)
hm4.SetMaximum(ymax_hm)
hm4.SetMinimum(ymin_hm)
hm4.SetLineColor(r.kRed)
hm4.Draw("same")
hm5 = model5.createHistogram("x",nbin_hm)
hm5.Divide(hm1)
hm5.SetMaximum(ymax_hm)
hm5.SetMinimum(ymin_hm)
hm5.SetLineColor(r.kYellow)
hm5.SetLabelSize(1)
hm5.Draw("SAME")
c.SaveAs("bkgfit.pdf")

print(frame1.chiSquare())
