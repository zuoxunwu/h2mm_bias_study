Double_t ScaleX(Double_t x){
    Double_t v;
    v = 0.025*x-3.75; // center at 150(GeV) [-1,1] not quite on lower bound
    return v;
}

void ScaleAxis(TAxis *a, Double_t (*Scale)(Double_t))
{
  if (!a) return; // just a precaution
  if (a->GetXbins()->GetSize())
    {
      // an axis with variable bins
      // note: bins must remain in increasing order, hence the "Scale"
      // function must be strictly (monotonically) increasing
      TArrayD X(*(a->GetXbins()));
      for(Int_t i = 0; i < X.GetSize(); i++) X[i] = Scale(X[i]);
      a->Set((X.GetSize() - 1), X.GetArray()); // new Xbins
    }
  else
    {
      // an axis with fix bins
      // note: we modify Xmin and Xmax only, hence the "Scale" function
      // must be linear (and Xmax must remain greater than Xmin)
      a->Set( a->GetNbins(),
              Scale(a->GetXmin()), // new Xmin
              Scale(a->GetXmax()) ); // new Xmax
    }
  return;
}


void ScaleXaxis(TH1 *h, Double_t (*Scale)(Double_t))
{
  if (!h) return; // just a precaution
  ScaleAxis(h->GetXaxis(), Scale);
  return;
}


// main function
void xRescale(){
    TFile* MyFile = new TFile("muPairs_mass.root");
    TH1F* histo_signal = (TH1F*)MyFile->Get("net_histos/c_01_test_Net_Signal");
    TH1F* histo_data = (TH1F*)MyFile->Get("net_histos/Data_2017BCDEF");

    ScaleXaxis(histo_signal,ScaleX);
    ScaleXaxis(histo_data,ScaleX);
    histo_signal->Draw();
    histo_data->Draw();

    TFile* savefile = new TFile("m1p1.root","RECREATE");
    TDirectory* net_histos = savefile->mkdir("net_histos");
    net_histos->cd();
    histo_signal->Write();
    histo_data->Write();
    savefile->Close();
}
