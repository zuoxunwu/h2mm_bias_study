#######################
# fit_spectrum
# fit dimuon invariant mass spectrum of background of WH channel of Higgs to mumu search
#######################
# zf: import modules
import os
import ROOT as r
from ROOT import RooFit as rf
from pdfClass_6bdt import * 
from takecarePlots import takecarePlots
r.gROOT.SetBatch(r.kTRUE)
################################
# load input file and histogram
# Arguments:
#   string filepath
################################
xmin = 110
xmax = 150
def fit_mass_spectrum(cat):
    isToy = False
    # zf
    dic_cats = {
        'cat0':"H_pair_mass_zoomH_Net_Bkg",
        'cat1':"H_pair_mass_BDT_n10_n02_zoomH_Net_Bkg",
        'cat2':"H_pair_mass_BDT_n02_p02_zoomH_Net_Bkg",
        'cat3':"H_pair_mass_BDT_p02_p06_zoomH_Net_Bkg",
        'cat4':"H_pair_mass_BDT_p060_p068_zoomH_Net_Bkg",
        'cat5':"H_pair_mass_BDT_p068_p076_zoomH_Net_Bkg",
        'cat6':"H_pair_mass_BDT_p076_p10_zoomH_Net_Bkg",
	'cat456': "H_pair_mass_BDT_p06_p10_zoomH_Net_Bkg",

        'Wcat1new': "H_pair_mass_BDT_final_n10_n01_zoomH_Net_Bkg",
        'Wcat2new': "H_pair_mass_BDT_final_n01_p03_zoomH_Net_Bkg",
        'Wcat3new': "H_pair_mass_BDT_final_p03_p10_zoomH_Net_Bkg",

	'Zcat1': "dimu_mass_BDT_n10_p04_Net_Bkg",
	'Zcat2': "dimu_mass_BDT_p04_p10_Net_Bkg",
	'Zcat1new': "dimu_mass_BDT_n10_n01_Net_Data",
        'Zcat2new': "dimu_mass_BDT_n01_p10_Net_Bkg",
	'Zcatall': 'dimu_mass_BDT_n10_p10_Net_Bkg',
        }
    dirpath = "InputFiles/"
    if isToy == True:
      if 'Z' in cat:
	fname = "OutputFiles/" + dic_cats[cat].replace('dimu_mass_', 'ZH_').replace('_Net_Bkg', '') + "/toy_MKBwz0_seed1.root"
      else:
        fname = "OutputFiles/" + dic_cats[cat].replace('H_pair_mass_', 'WH_').replace('_final', '').replace('_zoomH_Net_Bkg', '') + "/toy_MKBwz0_seed1.root"
      f = r.TFile(fname)
      itoy = 10
      ds = f.Get("toys/toy_"+str(itoy)) #RooDataSet
    else:
      if 'Z' in cat:
	#fname = "mass_hists_lepMVAn4.root"
	fname = "mass_hists_lepMVAp04.root"
      else:
        fname = "StackPlots_run2_WH.root"
      fullpath = os.path.join(dirpath, fname)
      print("histogram root file path: %s"%fullpath)
      f = r.TFile(fullpath)
      h = f.Get(dic_cats[cat])
      if h.GetNbinsX() == 800: h.Rebin(20)
    frametitle="WH_"+cat
    if 'Z' in cat: frametitle="ZH_"+cat
    # define x variable (dimuon mass); convert histo in x
    # histo x = [110,160] (GeV); 135 is middle point
    x = r.RooRealVar("x","x",125,xmin,xmax)
    middle = (xmin+xmax)/2.0
    half_interval = (xmax-xmin)/2.0
    #middle = 135
    #half_interval = 25 
    #x = r.RooRealVar("x","x",125,110,160)
    # for [110, 160] -> [-1,1]
    x1 = r.RooFormulaVar("x1","x1","(@0-%f)/%f"%(middle, half_interval), r.RooArgList(x))
    x11 = r.RooFormulaVar("x1","x1","(@0-135)/25", r.RooArgList(x))
    x2 = r.RooFormulaVar("x2","x2","(@0-105)/20",r.RooArgList(x))
    x3 = r.RooFormulaVar("x3","x3","(@0-135)",r.RooArgList(x))

    # for power law
    x21 = r.RooFormulaVar("x2","x2","@0/100",r.RooArgList(x)) 
    if isToy == True:
        dh = ds.binnedClone("data_obs","data_obs") # RooDataHist
    else:
        # convert TH1 to RooDataHist
        dh = r.RooDataHist("data_obs","data_obs",r.RooArgList(x),h)

    # plot
    #r.gStyle.SetOptFit(1011)
    frame1 = x.frame(rf.Title(frametitle))
    dh.plotOn(frame1)

    #########################
    #  model parameter tuning 
    #########################
    models = []
    # fold: cat1
    if cat == "cat1":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat2
    if cat == "cat2":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat3
    if cat == "cat3":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat4
    if cat == "cat4":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat5
    if cat == "cat5":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat6
    if cat == "cat6":
        # model 10
#        mkbwz = MKBwz()
#        model10, gc10 = mkbwz.makeModel(x)
#	models.append(model10)
#	# model 11
#        mkbwzbern1 = MKBwzBern1()
#        model11, gc11 = mkbwzbern1.makeModel(x)
#        models.append(model11)
#        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
#	# model 16
#        mkbwzredux = MKBwzredux_mod()
#        model16, gc16 = mkbwzredux.makeModel(x)
#        models.append(model16)
#	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
        mkpower2 = MKPower2()
	mkpower2.p['const'][5] = True
        model22, gc22 = mkpower2.makeModel(x)
        models.append(model22)
        # model 23
        mkpower2int = MKPower2()
	mkpower2int.name = "MKPower2int"
        model23, gc23 = mkpower2int.makeModel(x)
	models.append(model23)
	# model 40
#	mkexp = MKExp(1, False) # order = 1,2, intercept = True,False
#	model40, gc40 = mkexp.makeModel(x)
#	models.append(model40)
#	# model 41
#        mkexp = MKExp(1, True) # order = 1,2, intercept = True,False
#        model41, gc41 = mkexp.makeModel(x)
#        models.append(model41)
#	# model 42
#        mkexp = MKExp(2, False) # order = 1,2, intercept = True,False
#        model42, gc42 = mkexp.makeModel(x)
#        models.append(model42)
#	# model 43
#        mkexp = MKExp(2, True) # order = 1,2, intercept = True,False
#        model43, gc43 = mkexp.makeModel(x)
#        models.append(model43)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
        mkexp2 = MKExp2()
        mkexp2.p['const'][5] = True
        model42, gc42 = mkexp2.makeModel(x)
        models.append(model42)
	# model 43
	mkexp2int = MKExp2()
	mkexp2int.name = "MKExp2int"
        model43, gc43 = mkexp2int.makeModel(x)
        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)
    # fold: cat456
    if cat == "cat456" or cat == "Zcat1" or cat == "Zcat2" or cat == "Zcat1new" or cat == "Zcat2new" or cat == "Zcatall" or cat == "Wcat1new" or cat == "Wcat2new" or cat == "Wcat3new":
        # model 10
        mkbwz = MKBwz()
        model10, gc10 = mkbwz.makeModel(x)
	models.append(model10)
	# model 11
        mkbwzbern1 = MKBwzBern1()
        model11, gc11 = mkbwzbern1.makeModel(x)
        models.append(model11)
        # model 12
#        mkbwzbern2 = MKBwzBern2()
#        model12, gc12 = mkbwzbern2.makeModel(x)
#        models.append(model12)
#	# model 13
#        mkbwzredux_p1 = MKBwzredux_mod()
#        mkbwzredux_p1.name = "MKBwzredux_p1"
#        mkbwzredux_p1.p['pow'][5] = True
#	mkbwzredux_p1.p['w'][5] = True
#	mkbwzredux_p1.p['ex2'][5] = True
#        model13, gc13 = mkbwzredux_p1.makeModel(x)
#        models.append(model13)
#	# model 14
#        mkbwzredux_p2 = MKBwzredux_mod()
#        mkbwzredux_p2.name = "MKBwzredux_p2"
#        mkbwzredux_p2.p['pow'][5] = True
#        mkbwzredux_p2.p['w'][5] = True
#        model14, gc14 = mkbwzredux_p2.makeModel(x)
#        models.append(model14)
#	# model 15
#        mkbwzredux_p3 = MKBwzredux_mod()
#        mkbwzredux_p3.name = "MKBwzredux_p3"
#        mkbwzredux_p3.p['pow'][5] = True
#        model15, gc15 = mkbwzredux_p3.makeModel(x)
#        models.append(model15)
	# model 16
        mkbwzredux = MKBwzredux_mod()
        mkbwzredux.p['w'][5] = True
        model16, gc16 = mkbwzredux.makeModel(x)
        models.append(model16)
        # model 17
        mkbwzgamma = MKBwzGamma()
        model17, gc17 = mkbwzgamma.makeModel(x)
        models.append(model17)
        # model 18
        mkbwzfix = MKBwz()
        mkbwzfix.name = "MKBwzFix"
        mkbwzfix.p['a3'][2] = 1.5
        mkbwzfix.p['a3'][5] = True
        model18, gc18 = mkbwzfix.makeModel(x)
        models.append(model18)
	# model 20
        mkpower1 = MKPower1()
	mkpower1.p['const'][5] = True
        model20, gc20 = mkpower1.makeModel(x)
        models.append(model20)
	# model 21
	mkpower1int = MKPower1()
        mkpower1int.name = "MKPower1int"
        model21, gc21 = mkpower1int.makeModel(x)
        models.append(model21)
	# model 22
#        mkpower2 = MKPower2()
#	mkpower2.p['const'][5] = True
#        model22, gc22 = mkpower2.makeModel(x)
#        models.append(model22)
#        # model 23
#        mkpower2int = MKPower2()
#	mkpower2int.name = "MKPower2int"
#        model23, gc23 = mkpower2int.makeModel(x)
#	models.append(model23)
        # model 40
        mkexp1 = MKExp1()
	mkexp1.p['const'][5] = True
        model40, gc40 = mkexp1.makeModel(x)
	models.append(model40)
	# model 41
        mkexp1int = MKExp1()
        mkexp1int.name = "MKExp1int"
        model41, gc41 = mkexp1int.makeModel(x)
        models.append(model41)
	# model 42
#        mkexp2 = MKExp2()
#        mkexp2.p['const'][5] = True
#        model42, gc42 = mkexp2.makeModel(x)
#        models.append(model42)
#	# model 43
#	mkexp2int = MKExp2()
#	mkexp2int.name = "MKExp2int"
#        model43, gc43 = mkexp2int.makeModel(x)
#        models.append(model43)
	# model 50
        mkbernstein1 = MKBernsteinFast(1)
        model50, gc50 = mkbernstein1.makeModel(x)
        models.append(model50)
        # model 51
        mkbernstein2 = MKBernsteinFast(2)
        model51, gc51 = mkbernstein2.makeModel(x)
	models.append(model51)
	# model 52
	mkbernstein3 = MKBernsteinFast(3)
        model52, gc52 = mkbernstein3.makeModel(x)
        models.append(model52)

    ########
    # plot #
    ########
    takecareplots = takecarePlots()
    takecareplots.plot(frametitle, x, frame1, dh, models, xmin=xmin,xmax=xmax)

#cat="cat5"
#for e in ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6"]:
#for e in ["cat456"]:
for e in ["Zcat1new"]:
#for e in ["Wcat1new"]:
    fit_mass_spectrum(e)
 
