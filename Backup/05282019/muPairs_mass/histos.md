0,1,2,3,4,5,6,7





mk@mk-ThinkPad-E470:~/Codes/novelbias/muPairs_mass$ root -l muPairs_mass.root 
root [0] 
Attaching file muPairs_mass.root as _file0...
(TFile *) 0x55c720138230
root [1] .ls
TFile**		muPairs_mass.root	
 TFile*		muPairs_mass.root	
  KEY: TDirectoryFile	net_histos;1	net_histos
root [2] net_histos->cd()
(bool) true
root [3] .ls
TDirectoryFile*		net_histos	net_histos
 KEY: TH1F	c_01_test_Net_Bkg;1	MC_DY_and_ttbar
 KEY: TH1F	c_01_test_DY_Bkg;1	MC_DY
 KEY: TH1F	c_01_test_ttbar_Bkg;1	MC_ttbar
 KEY: TH1F	c_01_test_Net_Signal;1	MC_Zd150
 KEY: TH1F	Data_2017BCDEF;1	Data_2017BCDEF
root [4] 


