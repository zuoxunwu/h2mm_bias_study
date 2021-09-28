import ROOT as r
from ROOT import RooFit as rf

COLOR = {}
COLOR["MKBwz"]        = r.kBlue
COLOR["MKBwzBern1"]   = r.kBlue + 2
COLOR["MKBwzBern2"]   = r.kBlue - 7
COLOR["MKBwzredux_p1"] = r.kOrange
COLOR["MKBwzredux_p2"] = r.kOrange - 3
COLOR["MKBwzredux_p3"] = r.kOrange - 5
COLOR["MKBwzredux"]    = r.kOrange + 2
COLOR["MKBwzGamma"]   = r.kBlack
COLOR["MKBwzFix"]     = r.kOrange

COLOR["MKPower1"]     = r.kMagenta
COLOR["MKPower1int"]  = r.kMagenta + 2
COLOR["MKPower2"]     = r.kMagenta - 7
COLOR["MKPower2int"]  = r.kMagenta - 5
COLOR["MKExp1"]       = r.kGreen + 1
COLOR["MKExp2"]	      = r.kGreen + 2
COLOR["MKExp1int"]    = r.kGreen + 3
COLOR["MKExp2int"]    = r.kGreen - 6
COLOR["MKBernstein1"] = r.kYellow + 1
COLOR["MKBernstein2"] = r.kYellow + 2
COLOR["MKBernstein3"] = r.kYellow + 3
COLOR["MKBernstein4"] = r.kYellow - 6

class takecarePlots:
    def __init__(self):
        pass        
    def plot(self, frametitle, x, frame1, dh, models, xmin=110, xmax=150): 
        # Canvas
        c = r.TCanvas("c", "c",800,800)
        pad1 = r.TPad("pad1","pad1",0.0,0.25,1.0,1.0)
        pad1.Draw()
        pad1.cd()
        # fit 

        x.setRange("left", xmin, 120)
        x.setRange("right", 130, xmax)

	chi2 = []
	minNLL = []
	kstest = []
	dhist = dh.createHistogram('data_hist', x)
	for i in range(len(models)):
	  #nll.append( models[i].createNLL(dh, rf.Range(xmin,xmax)).getVal() )
	  #f_result = r.RooFitResult("fit_res", "fit_res")
	  print "DH",dh
	  print "msdel ",models[i]
	  #models[i].Print("V")
	  print "Val",models[i].getVal()
	  f_result = models[i].fitTo(dh, rf.Range("left,right"), rf.Save(r.kTRUE), rf.SumW2Error(r.kFALSE))
	  models[i].plotOn(frame1, rf.LineColor(COLOR[models[i].GetName()]), rf.Name(models[i].GetName()))
	  chi2.append(frame1.chiSquare())
	  f_result.Print()
	  minNLL.append(f_result.minNll())
#	  mhist = models[i].createHistogram("x", 100)
#	  kstest.append( mhist.KolmogorovTest(dhist) )	

        # plot
        frame1.Draw()
        legend = r.TLegend(0.2,0.6,0.9,0.9)
	for i in range(len(models)):
	  base = 0
	  if models[i].GetName() == 'MKBwz' or models[i].GetName() == 'MKBwzredux_p1' or models[i].GetName() == 'MKBernstein1' or models[i].GetName() == 'MKExp1' or models[i].GetName() == 'MKPower1': base = 1
	  if models[i].GetName() == 'MKBwzredux_p1' or models[i].GetName() == 'MKBernstein1' or models[i].GetName() == 'MKExp1': legend.AddEntry(None,'','')
	  legend.AddEntry(frame1.findObject(models[i].GetName()), "%s  #chi^{2}=%.2f, F= %.3f,   minNLL=%.2f, 2#DeltaNLL= %.3f" %(models[i].GetName(), chi2[i], (chi2[i-1+base]-chi2[i])/chi2[i], minNLL[i], 2*(minNLL[i-1+base]-minNLL[i])), 'L')
        legend.Draw()

        # lower pad
        c.cd()
        pad2 = r.TPad("pad2","pad2",0.0,0.0,1.0,0.25)
        pad2.Draw()
        pad2.cd()
        frame2 = x.frame(rf.Title("ratio"),rf.Range(xmin,xmax))

	print dhist.GetNbinsX()
	print dhist.Integral()
        nbin_hm = 1000
        ymax_hm = 1.20
        ymin_hm = 0.80
#        hm1 = model1.createHistogram("x",nbin_hm)
#        hm1_1.SetLabelSize(0.1,"xy")
#        hm1_1.SetStats(r.kFALSE)
#        hm1_1.GetYaxis().SetTitle("model2/model1")
#        hm1_1.GetYaxis().CenterTitle(r.kTRUE)
#        hm1_1.GetYaxis().SetTitleOffset(0)
#        #r.gStyle.SetTitleFontSize(0.1)
#        hm1_1.GetYaxis().SetTitleFont(42)
#        hm1_1.GetYaxis().SetTitleSize(0.05)
#        hm1_1.SetTitle("")
#        #hm1_1.SetTitleSize(0.1,"y")
#        hm1_1.Draw()
        hm1 = models[0].createHistogram("x",nbin_hm)
	print hm1.Integral()

	for i in range(len(models)):
	  hms = models[i].createHistogram("x",nbin_hm)
	  print hms.Integral()
	  hms.Divide(hm1)
	  hms.SetMaximum(ymax_hm)
          hms.SetMinimum(ymin_hm)
	  hms.SetLineWidth(2)
          hms.SetLineColor(COLOR[models[i].GetName()])
	  hms.SetStats(r.kFALSE)
	  hms.SetLabelSize(0.1,"xy")
	  hms.SetTitle("") 
          hms.Draw("SAMEHIST")

        c.SaveAs('Fits/' + frametitle+".png")

	for i in range(len(models)):
	  canv = r.TCanvas("c_%d"%i, "c_%d"%i, 800,800)
	  frame = x.frame(rf.Title(models[i].GetName()), rf.Range(xmin,xmax))
	  dh.plotOn(frame)
	  models[i].plotOn(frame, rf.LineColor(COLOR[models[i].GetName()]), rf.Name(models[i].GetName()))
	  models[i].paramOn(frame)
	  frame.Draw()
	  t = r.TLatex(.6,.6,"#chi^{2}/ndof = %7.3f" % chi2[i])
	  t.SetNDC(r.kTRUE)
	  t.Draw()
	  canv.SaveAs('Fits/' + frametitle + models[i].GetName() + '.png')


