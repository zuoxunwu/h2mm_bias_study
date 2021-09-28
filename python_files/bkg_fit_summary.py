import argparse
from ROOT import *
from pdfClass_6bdt import *
import os

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('h_bkg')
    parser.add_argument('title')
    args = parser.parse_args()

    models = ['MKBwz', 'MKPower', 'MKExp', 'MKBernstein', 'MKBwzredux']
    colors = {}
    b_fit = {}
    b_hist = {}
    b_ratio = {}

    colors['MKBwz']       = kBlue
    colors['MKPower']     = kViolet
    #colors['MKLegendre'] = kGreen
    colors['MKExp']       = kRed
    colors['MKBernstein'] = kYellow
    colors['MKBwzredux']  = kOrange
 
    out_file = TFile('OutputFiles/' + 'bkg_' + args.title + '.root', 'RECREATE')

    in_file  = TFile(args.infile)
    bkg_hist = in_file.Get(args.h_bkg)

    x = None
    for model in models:
	ws_name = 'c_01_test'
	ws_path = 'OutputFiles/' + args.title + '/' + ws_name + '_s' + model + '.root'
 	ws_file = TFile(ws_path)
	wspace  = ws_file.Get(ws_name)
	
	x = wspace.var('x')
	b_fit[model] = wspace.pdf('bmodel_c_01_test')
	#b_hist[model] = b_fit[model].generateBinned(RooArgSet(x),1000,True).createHistogram('x', bkg_hist.GetNbinsX())
	b_hist[model] = b_fit[model].createHistogram('x', bkg_hist.GetNbinsX())
   	b_hist[model].SetName('hist_' + model)
	b_ratio[model] = b_hist[model].Clone( 'ratio_' + model )
	b_ratio[model].Divide( bkg_hist )
    	
    out_file.cd()
    for model in models:
	b_hist[model].Write()
	b_ratio[model].Write()

    canv = TCanvas('bkg_' + args.title, 'bkg_' + args.title, 600, 600)

    upper_pad = TPad("upperpad_"+var_name, "upperpad_"+var_name, 0,0.25, 1,1)
    upper_pad.SetBottomMargin(0.04)
    upper_pad.Draw()
    upper_pad.cd()
    legend = TLegend(0.6,0.6,0.9,0.9)
    xframe = x.frame('bkg_' + args.title, 'bkg_' + args.title)
    bkg_hist.plotOn(xframe, RooFit.MarkerStyle(1), RooFit.MarkerColor(kBlack), RooFit.LineColor(kBlack))
    for model in models:
	b_fit[model].plotOn(xframe, RooFit.LineColor(colors[model]), RooFit.Range('FULL'))
	legend.AddEntry(b_fit[model], model)

    xframe.Draw()
    legend.Draw()
    xframe.GetXaxis().SetLabelSize(0)

    canv.cd()
    lower_pad = TPad("lowerpad_"+var_name, "lowerpad_"+var_name, 0, 0, 1,0.25)
    lower_pad.SetTopMargin(0.04)
    lower_pad.SetBottomMargin(0.3)
    lower_pad.SetGridy()
    lower_pad.Draw()
    lower_pad.cd()

    for model in models:
	b_ratio[model].SetLineWidth(2)
	b_ratio[model].SetLineColor(colors[model])
	b_ratio[model].Draw('histsame')

    canv.cd()
    canv.SaveAs('OutputFiles/' + 'bkg_' + args.title + '.png')

if __name__ == '__main__':
    main()
