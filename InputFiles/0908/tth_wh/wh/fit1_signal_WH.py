import ROOT as r
from ROOT import RooFit as rf

# load input file and histogram
f = r.TFile("StackPlots_WH.root")
choice1 = 2
if choice1 == 1:# 1.092
    h = f.Get("H_pair_mass_zoomH_Net_Sig")
elif choice1 == 2: # 0.097
    h = f.Get("H_pair_mass_BDT_n10_n02_zoomH_Net_Sig")
elif choice1 == 3: # 0.568
    h = f.Get("H_pair_mass_BDT_n02_p02_zoomH_Net_Sig")
elif choice1 == 4: # 0.446
    h = f.Get("H_pair_mass_BDT_p02_p06_zoomH_Net_Sig")
elif choice1 == 5: # 1.28
    h = f.Get("H_pair_mass_BDT_p06_p10_zoomH_Net_Sig")
# define x variable (dimuon mass); convert histo in x
x = r.RooRealVar("x","x",125,110,160)
x1 = r.RooFormulaVar("x1","x1","(@0-135)/50",r.RooArgList(x))
x2 = r.RooFormulaVar("x2","x2","(@0-110)/50",r.RooArgList(x))

# convert TH1 to RooDataHist
dh = r.RooDataHist("dh","dh",r.RooArgList(x),h)

# plot
frame1 = x.frame(rf.Title("frame1"))
dh.plotOn(frame1)

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
    return model, gc 


model, gc = MKTripleGauss(x)

c = r.TCanvas("test", "test", 800, 800)
# fit 
model.fitTo(dh, rf.Range(110,160))
model.plotOn(frame1)

# disply plots
print(frame1.chiSquare())
frame1.Draw()
c.SaveAs("signal.png")
