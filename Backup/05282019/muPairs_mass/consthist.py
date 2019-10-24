import ROOT as rt
x = rt.RooRealVar("x", "x", -1, 1)
uni = rt.RooUniform("uni","uni",rt.RooArgSet(x))
hist_uni = uni.generate(rt.RooArgSet(x),1000000)
xframe = x.frame(rt.RooFit.Title("uni"))
hist_uni.plotOn(xframe)
c = rt.TCanvas("c","c",800,400)
xframe.Draw()
c.SaveAs("uni.png")
