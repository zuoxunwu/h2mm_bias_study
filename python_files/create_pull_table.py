import os
import csv
import numpy as np
import ROOT as r
r.gROOT.SetBatch(r.kTRUE)
r.gStyle.SetPaintTextFormat("2.0f%%")
def create_pull_table(infile):
    filefront = os.path.splitext(infile)[0] 
    # plot
    c1 = r.TCanvas("c1","demo",10,10,600,600)
    c1.SetGrid()
    c1.SetLeftMargin(0.18)
    c1.SetRightMargin(0.13)
    c1.SetBottomMargin(0.07)
    h_name = filefront[:-1]+"_signal_strength_"+filefront[-1]
    h = r.TH2F("h",'',3,0,3,2,0,2)
    h.SetStats(0)
    r.gRandom.SetSeed()
    # read txt/csv file
    csv_file = open(infile)
    csv_reader = list(csv.reader(csv_file, delimiter=','))
    for row in csv_reader:
        if row[1] == 'MKExp1': continue
        if row[2] == 'MKExp1': continue
        h.Fill(row[1].replace('MK',''), row[2].replace('MK',''), round(100*float(row[3]),2))
    h.GetYaxis().SetTitle("Fit Model")
    h.GetYaxis().SetTitleOffset(2.2)
    h.GetXaxis().SetTitle("Toy Model")
    h.LabelsDeflate("X")
    h.LabelsDeflate("Y")
    h.LabelsOption("a","X")
    h.LabelsOption("a","Y")
    h.SetContour(12)
    h.SetMarkerSize(2)
    hc = h.Clone()
    hc.Reset()
    for row in csv_reader:
        if row[1] == 'MKExp1': continue
        if row[2] == 'MKExp1': continue
        pull_val = round(100*float(row[3]),2)
        if abs(pull_val) <= 40.0:
            hc.Fill(row[1].replace('MK',''), row[2].replace('MK',''), pull_val)
        elif pull_val >= 40:
            hc.Fill(row[1].replace('MK',''), row[2].replace('MK',''), 40.0)
        elif pull_val <= -40:
            hc.Fill(row[1].replace('MK',''), row[2].replace('MK',''), -40.0)
    hc.SetMaximum(40)
    hc.SetMinimum(-40)
    hc.Draw("colztext")
    #h.Draw("text")
    cms_latex = r.TLatex()
    cms_latex.SetTextAlign(11)
    cms_latex.SetTextSize(0.03)
    cms_latex.DrawLatexNDC(0.18, 0.92, '#scale[1.5]{CMS #bf{#it{Preliminary Simulation}}}')

    c1.Update()
    c1.SaveAs(h_name+"_table.pdf")
# list files from current directory
print(os.curdir)
#files = os.listdir(os.path.join(os.curdir,'OutputFiles'))
outdir = os.path.join(os.curdir,'OutputFiles')
files_txt = [f for f in os.listdir(outdir) if (f.startswith("pulls") and f.endswith(".txt"))]
for ftxt in files_txt:
    fpathu = outdir+"/"+ftxt
    create_pull_table(fpathu)
