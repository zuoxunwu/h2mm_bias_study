import ROOT as r

nx = 2 # months
ny = 3 # people  
month = ['January','February']
people = ['Alex','Barry','Caleb']

c1 = r.TCanvas("c1","demo",10,10,600,600)
c1.SetGrid()
c1.SetLeftMargin(0.15)
c1.SetBottomMargin(0.15)
h = r.TH2F("h","test",3,0,3,2,0,2)
h.SetStats(0)
r.gRandom.SetSeed()
for i in range(0,100):
    rx = int(r.gRandom.Rndm()*nx)
    ry = int(r.gRandom.Rndm()*ny)
    # print(rx, ry)
    h.Fill(people[ry],month[rx],0.1)
h.LabelsDeflate("X")
h.LabelsDeflate("Y")
h.LabelsOption("Y")
h.Draw("colz")

