//This program creates histograms for dimuon mass spectrum. to be used for modeling singal/background 

void run(){	
	//==========================
	string varToPlot = "muPairs.mass_Roch";
	// mass range for histograms
	// symmetric range around 150GeV dark photon mass
	// Z peak 90GeV width 2GeV
	int xmin=110;
	int xmax=190;
	int bins=80; //1GeV bins
	//Should logscale be off for limit-setting? Probably yes?
	//choose different MC/data selection
	
	// choose eta region
	//string selection_eta = "(muons[0].eta > -2.4 && muons[0].eta < 2.4 && muons[1].eta > -2.4 && muons[1].eta < 2.4)";
	//Barrel region
	string selection_eta = "(abs(muons[muPairs.iMu1].eta) < 0.9 && abs(muons[muPairs.iMu2].eta) < 0.9)";
	//string selection_eta = "((abs(muons[muPairs.iMu1].eta) > 0.9 && abs(muons[muPairs.iMu1].eta) < 1.7) ||( abs(muons[muPairs.iMu2].eta) > 0.9 && abs(muons[muPairs.iMu2].eta) < 1.7))";
	//string selection_eta = "(abs(muons[muPairs.iMu1].eta) > 1.7 || abs(muons[muPairs.iMu2].eta) > 1.7)";
	//==========================

	// Loading ROOT files for data and MC for signal/background
	TFile* MyFileMC_DY = new TFile("/home/pq8556/.paths/mukim/66/dytestall.root","READ"); //1921.8*3pb,126068800
	TFile* MyFileMC_ttbar = new TFile("/home/pq8556/.paths/mukim/ttbar2017.root","READ"); //831.76pb, 57342000
	TFile* MyFileB = new TFile("/home/pq8556/.paths/mukim/0906/testB.root","READ"); //4823 pb^-1
	TFile* MyFileC = new TFile("/home/pq8556/.paths/mukim/0906/testC.root","READ"); //9664 pb^-1
	TFile* MyFileD = new TFile("/home/pq8556/.paths/mukim/0906/testD.root","READ"); //4252 pb^-1
	TFile* MyFileE = new TFile("/home/pq8556/.paths/mukim/0906/testE.root","READ"); //9278 pb^-1
	TFile* MyFileF = new TFile("/home/pq8556/.paths/mukim/0906/testF.root","READ"); //13540 pb^-1
	TFile* MyFileSignal = new TFile("/home/pq8556/muffin_data/tuple_total_Zd150.root","READ");

	//the integrated luminosity of data(the LHC)
	double lumiB = 4823, lumiC = 9664, lumiD = 4252, lumiE = 9278, lumiF = 13540;
	double luminosity = lumiB + lumiC + lumiD + lumiE + lumiF; // pb^-1
	
	//cross-sections for processes
	double xsec_DY = 1921.8*3; // pb
	double xsec_ttbar = 831.76; // pb
	double xsec_Zd150 = 0.2029; //pb; cross-section*(branching ratio) at Z_D mass 150GeV

	// sumEventWeights ( metadata in ntuple)
	double total_sEW_DY = 126068800;
	double total_sEW_ttbar = 57342000; 
	double total_sEW_Zd150 = 255420; 
	// total luminosity of data samples : 41557

	// scale factor = lumi * xsec / total sumEventWeights
	double scaleFactor_DY = luminosity * xsec_DY / total_sEW_DY;
	double scaleFactor_ttbar = luminosity * xsec_ttbar / total_sEW_ttbar; 
	double scaleFactor_Zd150 = luminosity * xsec_Zd150 / total_sEW_Zd150;
 
	cout << "The total integrated luminosity of the data : " << luminosity << "pb^-1" << endl;
	cout << "scale factors for MC" << endl;
	cout << "DY : " << scaleFactor_DY << endl;
	cout << "ttbar :" << scaleFactor_ttbar << endl;
	cout << "Zd150 :" << scaleFactor_Zd150 << endl;

	// load TTrees
	TTree* MyTreeMC_DY = (TTree*) (*MyFileMC_DY).Get("dimuons/tree");
	TTree* MyTreeMC_ttbar = (TTree*) (*MyFileMC_ttbar).Get("dimuons/tree");
	TTree* MyTreeB = (TTree*) (*MyFileB).Get("dimuons/tree");
	TTree* MyTreeC = (TTree*) (*MyFileC).Get("dimuons/tree");
	TTree* MyTreeD = (TTree*) (*MyFileD).Get("dimuons/tree");
	TTree* MyTreeE = (TTree*) (*MyFileE).Get("dimuons/tree");
	TTree* MyTreeF = (TTree*) (*MyFileF).Get("dimuons/tree");
	TTree* MyTreeSignal = (TTree*) (*MyFileSignal).Get("dimuons/tree");

	// initialize histos to fill
	TH1F* MyHistoMC_DY = new TH1F("MyHistoMC_DY","MyHistoMC_DY",bins,xmin,xmax);
	TH1F* MyHistoMC_ttbar = new TH1F("MyHistoMC_ttbar","MyHistoMC_ttbar",bins,xmin,xmax);
	TH1F* MyHistoB = new TH1F("MyHistoB","MyHistoB",bins,xmin,xmax);
	TH1F* MyHistoC = new TH1F("MyHistoC","MyHistoC",bins,xmin,xmax);
	TH1F* MyHistoD = new TH1F("MyHistoD","MyHistoD",bins,xmin,xmax);
	TH1F* MyHistoE = new TH1F("MyHistoE","MyHistoE",bins,xmin,xmax);
	TH1F* MyHistoF = new TH1F("MyHistoF","MyHistoF",bins,xmin,xmax);
	TH1F* MyHistoSignal = new TH1F("MyHistoSignal","MyHistoSignal",bins,xmin,xmax);

	TH1F* MyAdd = new TH1F("Data_2017BCDEF","Data_2017BCDEF",bins,xmin,xmax);
	TH1F* MyAdd_MC = new TH1F("c_01_test_Net_Bkg","MC_DY_and_ttbar",bins,xmin,xmax);
	TH1F* MyAdd_MC_DY = new TH1F("c_01_test_DY_Bkg","MC_DY",bins,xmin,xmax);
	TH1F* MyAdd_MC_ttbar = new TH1F("c_01_test_ttbar_Bkg","MC_ttbar",bins,xmin,xmax);
	TH1F* MyAdd_MC_Signal = new TH1F("c_01_test_Net_Signal","MC_Zd150",bins,xmin,xmax);


	TCanvas* c1 = new TCanvas("c1","dimuon_mass",500,500);
	TPad* pad1 = new TPad("pad1","pad1",0,0.3,1,1.0);
	(*pad1).Draw();
	// log scale on and off
	//(*pad1).SetLogy();
	(*pad1).cd();


	// selection for MC
	string MCweight = "PU_wgt*IsoMu_SF_3*MuID_SF_3*MuIso_SF_3*GEN_wgt*";
	string selection1 = "muons[0].pt_Roch > 30 && muons[1].pt_Roch >20 && muons[0].isMediumID == 1 && muons[1].isMediumID == 1 && muons[0].relIso < 0.25 && muons[1].relIso < 0.25 && muPairs.mass_Roch > 60 && muPairs.mass_Roch < 200 && (muons[0].isHltMatched[2]==1 || muons[0].isHltMatched[3]==1 || muons[1].isHltMatched[2]==1 || muons[1].isHltMatched[3]==1)";
	string selection = MCweight + "(" + selection1 + "&&" + selection_eta + ")";
	const char* selection_MC2 = selection.c_str();
	cout << selection_MC2 << endl;
	
	// selection for data
	string selection2 = "muons[0].pt_Roch > 30 && muons[0].isMediumID == 1 && muons[1].isMediumID == 1 && muons[0].relIso < 0.25 && muons[1].relIso < 0.25 && (muons[0].isHltMatched[2]==1 || muons[0].isHltMatched[3]==1 || muons[1].isHltMatched[2]==1 || muons[1].isHltMatched[3]==1)";
	string str_selection_Data = selection1 + "&&" + selection_eta;
	const char* selection_Data = str_selection_Data.c_str();
	cout << selection_Data << endl;

	// selection for signal; trigger bits not used
	string selection3 = "muons[0].pt_Roch > 30 && muons[0].isMediumID == 1 && muons[1].isMediumID == 1 && muons[0].relIso < 0.25 && muons[1].relIso < 0.25";
	string str_selection_Signal = MCweight + "(" + selection3 + "&&" + selection_eta + ")";
	const char* selection_Signal = str_selection_Signal.c_str();
	cout << selection_Signal << endl;


	// filling histograms from ntuples
	//var
	
	string svarexpMC_DY = varToPlot + ">> MyHistoMC_DY";
	const char* varexpMC_DY = svarexpMC_DY.c_str();
	cout << varexpMC_DY << endl;
	(*MyTreeMC_DY).Draw(varexpMC_DY,selection_MC2,"HIST");
	(*MyHistoMC_DY).Scale(scaleFactor_DY);
	(*MyAdd_MC).Add(MyHistoMC_DY);
	(*MyAdd_MC_DY).Add(MyHistoMC_DY);

	string svarexpMC_ttbar = varToPlot + ">> MyHistoMC_ttbar";
	const char* varexpMC_ttbar = svarexpMC_ttbar.c_str();
	cout << varexpMC_ttbar << endl;
	(*MyTreeMC_ttbar).Draw(varexpMC_ttbar,selection_MC2,"HIST");	
	(*MyHistoMC_ttbar).Scale(scaleFactor_ttbar);
	(*MyAdd_MC).Add(MyHistoMC_ttbar);
	(*MyAdd_MC_ttbar).Add(MyHistoMC_ttbar);

	string svarexpB = varToPlot + ">> MyHistoB";
	const char* varexpB = svarexpB.c_str();
	cout << varexpB << endl;
	(*MyTreeB).Draw(varexpB,selection_Data,"HIST"); //"E"

	string svarexpC = varToPlot + ">> MyHistoC";
	const char* varexpC = svarexpC.c_str();
	cout << varexpC << endl;
	(*MyTreeC).Draw(varexpC,selection_Data,"HIST");

	string svarexpD = varToPlot + ">> MyHistoD";
	const char* varexpD = svarexpD.c_str();
	cout << varexpD << endl;
	(*MyTreeD).Draw(varexpD,selection_Data,"HIST");

	string svarexpE = varToPlot + ">> MyHistoE";
	const char* varexpE = svarexpE.c_str();
	cout << varexpE << endl;
	(*MyTreeE).Draw(varexpE,selection_Data,"HIST");

	string svarexpF = varToPlot + ">> MyHistoF";
	const char* varexpF = svarexpF.c_str();
	cout << varexpF << endl;
	(*MyTreeF).Draw(varexpF,selection_Data,"HIST");

	string svarexpSignal = varToPlot + ">> MyHistoSignal";
	const char* varexpSignal = svarexpSignal.c_str();
	cout << varexpSignal << endl;
	(*MyTreeSignal).Draw(varexpSignal,selection_Signal,"HIST");
	(*MyHistoSignal).Scale(scaleFactor_Zd150);
	(*MyAdd_MC_Signal).Add(MyHistoSignal);


	(*MyAdd).Add(MyHistoB);
	(*MyAdd).Add(MyHistoC);
	(*MyAdd).Add(MyHistoD);
	(*MyAdd).Add(MyHistoE);
	(*MyAdd).Add(MyHistoF);

	(*MyAdd).Draw("E");
	(*MyAdd_MC).Draw("HISTSAME");
	(*MyAdd_MC).SetLineColor(kRed);

	//lower pad
	(*c1).cd();
	TPad* pad2 = new TPad("pad2","pad2",0,0.05,1,0.3);
	(*pad2).Draw();
	(*pad2).cd();

	//ratio plot
	TH1F* h3 = (TH1F*)MyAdd->Clone("h3");
	(*h3).SetMinimum(0.5);
	(*h3).SetMaximum(1.5);
	(*h3).Divide(MyAdd_MC);
	h3->GetYaxis()->SetLabelSize(0.1);
	(*h3).Draw("ep");

	TLine* l1 = new TLine(xmin,1,xmax,1);
	(*l1).SetLineColor(kRed);
	(*l1).Draw();
	//var
	
	string file_ext = ".pdf";
	string ssavename = varToPlot + file_ext;
	const char* savename = ssavename.c_str();
	(*c1).SaveAs(savename);
	
	//saving histogram in root file
	TFile* savefile = new TFile("./muPairs_mass.root","RECREATE");
	TDirectory* net_histos = savefile->mkdir("net_histos");

	net_histos->cd();
	MyAdd_MC->Write();
	MyAdd_MC_DY->Write();
	MyAdd_MC_ttbar->Write();
	MyAdd_MC_Signal->Write();
	MyAdd->Write();	

	savefile->Close();
}
