# Fitting using Legendre
import ROOT as r
r.gROOT.SetBatch(r.kTRUE)

infilename = 'm1p1.root'
tfile = r.TFile(infilename)

# histogram for data
hist_data = tfile.Get('net_histos/Data_2017BCDEF')
x1 = r.RooRealVar('x','x',-1.0, 1.0)
x1.SetTitle('m_{#mu#mu}')
x1.setUnit('GeV')


data = r.RooDataHist('data_obs', 'data_obs', r.RooArgList(x1), hist_data)

def MKLegendre(x):
    eps = 0.0000001 #epsilon
    arglist = r.RooArgList() 
    # constant off set to handle negative pdf values
    #uni = r.RooUniform("uni","uni",r.RooArgSet(x))
    #data_uni = uni.generate(r.RooArgSet(x),500000)
    #data
    #data = r.RooDataHist('data_obs', 'data_obs', r.RooArgList(x), hist_data)
    #data.add(data_uni)
    # defining Legendre polynomial
    le0 = r.RooLegendre("le0","le0",x,0) 
    co0 = r.RooRealVar("co0","co0",eps,-1,1)
    le1 = r.RooLegendre("le1","le1",x,1) 
    co1 = r.RooRealVar("co1","co1",eps,-1,1)
    le2 = r.RooLegendre("le2","le2",x,2) 
    co2 = r.RooRealVar("co2","co2",eps,-1,1)
    le3 = r.RooLegendre("le3","le3",x,3) 
    co3 = r.RooRealVar("co3","co3",eps,-1,1)
    le4 = r.RooLegendre("le4","le4",x,4) 
    co4 = r.RooRealVar("co4","co4",eps,-1,1)
    le5 = r.RooLegendre("le5","le5",x,5)
    co5 = r.RooRealVar("co5","co5",eps,-1,1)
    le6 = r.RooLegendre("le6","le6",x,6) 
    co6 = r.RooRealVar("co6","co6",eps,-1,1)
    le7 = r.RooLegendre("le7","le7",x,7) 
    co7 = r.RooRealVar("co7","co7",eps,-1,1)
    le8 = r.RooLegendre("le8","le8",x,8) 
    co8 = r.RooRealVar("co8","co8",eps,-1,1)
    le9 = r.RooLegendre("le9","le9",x,9) 
    co9 = r.RooRealVar("co9","co9",eps,-1,1)
    le10 = r.RooLegendre("le10","le10",x,10) 
    co10 = r.RooRealVar("co10","co10",eps,-1,1)
    arglist.add(co0) #0
    arglist.add(le0)
    arglist.add(co1)
    arglist.add(le1)
    arglist.add(co2)
    arglist.add(le2)
    arglist.add(co3)
    arglist.add(le3)
    arglist.add(co4)
    arglist.add(le4)
    arglist.add(co5)
    arglist.add(le5) #11
    arglist.add(co6)
    arglist.add(le6)
    arglist.add(co7)
    arglist.add(le7) #15
    arglist.add(co8)
    arglist.add(le8) # 17
    arglist.add(co9)
    arglist.add(le9) # 19
    arglist.add(co10)
    arglist.add(le10) # 21
    leg = r.RooGenericPdf("leg","leg","@0*@1+@2*@3+@4*@5+@6*@7+@8*@9+@10*@11+@12*@13+@14*@15+@16*@17+@18*@19+@20*@21",arglist)
    return leg, [le0,co0,le1,co1,le2,co2,le3,co3,le4,co4,le5,co5,le6,co6,le7,co7,le8,co8,le9,co9,le10,co10]
    # @0*@1+@2*@3+@4*@5+@6*@7+@8*@9+@10*@11+@12*@13+@14*@15+@16*@17+@18*@19+@20*@21

def linear(x):
    le1 = r.RooLegendre("le1","le1",x,1,0)
    #lele = r.RooLegendre(le1)
    m = r.RooRealVar("slope", "slope", -0.33, -10, 0)        
    b = r.RooRealVar("offset", "offset", 15, 2, 1000) 
    #fle1 = r.RooFormulaVar("f","@0",r.RooArgList(le1))    
    linear_model = r.RooGenericPdf("linear_model", "@1*(@0-140)+@2", r.RooArgList(le1, m, b))
    return linear_model, [le1,m,b]

leg,_= MKLegendre(x1)

#============
plotname='test'
npar = 10 # 11 for wide l_max+1 -1
#============

#legnll = leg.createNLL(data,r.RooFit.Range(-1.1,1,1)) #-log(likelihood)
leg.fitTo(data)

# plotting
legnll = leg.createNLL(data,r.RooFit.Range(-1,1)) #-log(likelihood)
x1frame = x1.frame(r.RooFit.Name("2017data"),r.RooFit.Title("2017data"))
data.plotOn(x1frame)
leg.plotOn(x1frame)
leg.paramOn(x1frame, r.RooFit.Format("NELU", r.RooFit.AutoPrecision(2)), r.RooFit.Layout(0.6, 0.95, 0.92) )
x1frame.getAttText().SetLineWidth(1)
x1frame.getAttText().SetTextSize(0.03)
chi2 = x1frame.chiSquare()
c1 = r.TCanvas("Hello","Hello",720,720)
x1frame.Draw()
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

