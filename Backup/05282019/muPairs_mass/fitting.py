import ROOT as r

infilename = 'm1p1.root'
tfile = r.TFile(infilename)
# histogram for data
h_d = tfile.Get('net_histos/Data_2017BCDEF')
x = r.RooRealVar('x','x',0, -1, 1)
x.SetTitle('m_{#mu#mu}')
x.setUnit('GeV')
data = r.RooDataHist('data_obs', 'data_obs', r.RooArgList(x), h_d)

# defining Legendre polynomial
le0 = r.RooLegendre("le0","le0",x,0) 
co0 = r.RooRealVar("co0","co0",5,-10,10)
le1 = r.RooLegendre("le1","le1",x,1) 
co1 = r.RooRealVar("co1","co1",-7,-10,10)
le2 = r.RooLegendre("le2","le2",x,2) 
co2 = r.RooRealVar("co2","co2",5,-10,10)
le3 = r.RooLegendre("le3","le3",x,3) 
co3 = r.RooRealVar("co3","co3",-3,-10,10)

le4 = r.RooLegendre("le4","le4",x,4) 
co4 = r.RooRealVar("co4","co4",2,-10,10)
le5 = r.RooLegendre("le5","le5",x,5)
co5 = r.RooRealVar("co5","co5",-1,-10,10)
le6 = r.RooLegendre("le6","le6",x,6) 
co6 = r.RooRealVar("co6","co6",0.4,-10,10)
le7 = r.RooLegendre("le7","le7",x,7) 
co7 = r.RooRealVar("co7","co7",-0.2,-10,10)

le8 = r.RooLegendre("le8","le8",x,8) 
co8 = r.RooRealVar("co8","co8",0,-10,10)
le9 = r.RooLegendre("le9","le9",x,9) 
co9 = r.RooRealVar("co9","co9",0.1,-10,10)
le10 = r.RooLegendre("le10","le10",x,10) 
co10 = r.RooRealVar("co10","co10",-0.2,-10,10)
#le11 = r.RooLegendre("le11","le11",x,11) 
#co11 = r.RooRealVar("co11","co11",1,-10,10)

#le12 = r.RooLegendre("le12","le12",x,12) 
#co12 = r.RooRealVar("co12","co12",1,-10,10)
#le13 = r.RooLegendre("le13","le13",x,13) 
#co13 = r.RooRealVar("co13","co13",1,-10,10)
#0,1,2,3
leg1 = r.RooFormulaVar("leg1","leg1","@0*@1+@2*@3+@4*@5+@6*@7",r.RooArgList(co2,le2,co1,le1,co4,le4,co3,le3))
#4,5,6,7
leg2 = r.RooFormulaVar("leg2","leg2","@0*@1+@2*@3",r.RooArgList(co6,le6,co5,le5))
#8,9,10,11
leg3 = r.RooFormulaVar("leg3","leg3","@0*@1+@2*@3+@4*@5+@6*@7",r.RooArgList(co7,le7,co8,le8,co9,le9,co10,le10))
#12,13,14,15
#leg4 = r.RooFormulaVar("leg4","leg4","@0*@1+@2*@3",r.RooArgList(co12,le12,co13,le13))
#sum
leg = r.RooGenericPdf("leg","leg","@0+@1+@2",r.RooArgList(leg1,leg2,leg3))

#============
plotname='wide10_2468A'
npar = 10 # 11 for wide l_max+1 -1
#============
#legnll = leg.createNLL(data,r.RooFit.Range(-1.1,1,1)) #-log(likelihood)
leg.fitTo(data)
legnll = leg.createNLL(data,r.RooFit.Range(-1,1)) #-log(likelihood)
xframe = x.frame(r.RooFit.Name("2017data"),r.RooFit.Title("2017data"))
data.plotOn(xframe)
leg.plotOn(xframe)
leg.paramOn(xframe, r.RooFit.Format("NELU", r.RooFit.AutoPrecision(2)), r.RooFit.Layout(0.6, 0.95, 0.92) )
xframe.getAttText().SetLineWidth(1)
xframe.getAttText().SetTextSize(0.03)
chi2 = xframe.chiSquare()
c1 = r.TCanvas("Hello","Hello",720,720)
xframe.Draw()
t = r.TLatex(0.3,1300,"#chi^{2}/ndof = %7.3f" % chi2)
t.SetTextSize(0.03)
#t.SetTextAlign(13)
#t.SetNDC(r.kTRUE)
t.Draw()
t2 = r.TLatex(-1,7500,"\Lambda = -2 \log \^{\mathscr{L}} + 2*n(par) = %7.3f" % (2 * (legnll.getVal()) +2*npar))
t2.SetTextSize(0.03)
t2.Draw()
t3 = r.TLatex(-1,7000,"\Lambda = -2 \log \^{\mathscr{L}} + 0*n(par) = %7.3f" % (2 * (legnll.getVal()) +0*npar))
t3.SetTextSize(0.03)
t3.Draw()
c1.SaveAs(plotname+'.png')

#chi2 = xframe.chiSquare()
#print "chi2    :     %7.3f"               % chi2
