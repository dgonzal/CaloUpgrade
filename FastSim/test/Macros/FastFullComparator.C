{

  bool bRebinTrans = true;//false;

  for (int j = 0; j < 7; j++){

    int iMass = 10*TMath::Power(2, j);
                  
    string sName("PBWO_FEB2012_PERFECT_LIGHT_COLLECTION_ETA23_ELECTRON_WITH_SAMPLING_"); sName = sName  + Form("%d", iMass)  + "_FORWARD";

    //    string sName("SHASHLIK_PbLSO_REALISTIC_LIGHT_COLLECTION_ETA23_ELECTRON_"); sName = sName  + Form("%d", iMass)  + "_FORWARD";

    string sNameFast("ELECTRON_FORWARD/DQM_ShowerShape_"); sNameFast = sNameFast + "" + sName + ".root";
    string sNameFull("ELECTRON_FORWARD/OUT_SHORTSTEPS/PBWO_FEB2012_FULLSIM_PERFECT_LIGHT_COLLECTION_ELECTRON_"); sNameFull = sNameFull + Form("%d", iMass) + ".root";
    //    string sNameFull("ELECTRON_FORWARD/PbLSO_SHASHLIK_FULLSIM_PERFECT_LIGHT_COLLECTION_ELECTRON_"); sNameFull = sNameFull + Form("%d", iMass) + ".root";


    TFile *_file0 = TFile::Open(sNameFast.c_str());
    TFile *_file1 = TFile::Open(sNameFull.c_str());
    _file0->cd("DQMData/Run 1/EMShower/Run summary");
  
    TCanvas* c = new TCanvas();
    c->Divide(2,2);


    TH1F* LongShapeFastSim = (TH1F*) gDirectory->Get("LongitudinalShape;1");
    TH1F* LongShapeFullSim = new TH1F(*LongShapeFastSim);
    LongShapeFullSim->Scale(0);
    
    LongShapeFullSim->SetLineColor(kYellow);
    LongShapeFullSim->SetFillColor(kYellow);
    
    TH1F* EcalLoShape = (TH1F*) _file1->Get("EcalLoShape;1");
    
    for (int i = 1; i < LongShapeFullSim->GetNbinsX()+1; i++){
    
      LongShapeFullSim->SetBinContent(i, EcalLoShape->GetBinContent(i));
    }

    double intFullSim = LongShapeFullSim->Integral();
    LongShapeFullSim->Scale(1./intFullSim);

    double intFastSim = LongShapeFastSim->Integral();
    LongShapeFastSim->Scale(1./intFastSim);
    LongShapeFastSim->SetLineColor(kRed);


    c->cd(1);

    string sTitle("Longitudinal shape E(Electron) = "); sTitle = sTitle + Form("%d", iMass); 
    
    LongShapeFullSim->SetStats(0);
    LongShapeFastSim->SetStats(0);

    LongShapeFullSim->SetTitle(sTitle.c_str());
    LongShapeFastSim->SetTitle(sTitle.c_str());

    LongShapeFullSim->DrawClone();
    LongShapeFastSim->DrawClone("SAME");
  
    

    c->cd(3);

    TLine* L = new TLine(0, 1, 26, 1);
    L->SetLineWidth(2);
    L->SetLineStyle(2);

    LongShapeFastSim->SetMaximum(1.5);
    LongShapeFastSim->SetMinimum(0.5);

    LongShapeFastSim->SetYTitle("Fast/Full");

    LongShapeFastSim->Divide(LongShapeFullSim);
    LongShapeFastSim->Draw();
    L->Draw("SAME");

    _file0->cd("DQMData/Run 1/EMShower/Run summary");
    TH1F* TransShapeFastSim = (TH1F*) gDirectory->Get("TransverseShape;1");
    TH1F* TransShapeFullSim = new TH1F(*TransShapeFastSim);
    TransShapeFullSim->Scale(0);
  
    TransShapeFullSim->SetLineColor(kYellow);
    TransShapeFullSim->SetFillColor(kYellow);

    TH1F* EcalTrShape = (TH1F*) _file1->Get("EcalTrShape;1");
    //TH1F* EcalTrShape = (TH1F*) _file1->Get("AbsTrShape;1");
    for (int i = 1; i < TransShapeFullSim->GetNbinsX()+1; i++){

      TransShapeFullSim->SetBinContent(i, EcalTrShape->GetBinContent(i));
    }

    double intFullSim = TransShapeFullSim->Integral();
    TransShapeFullSim->Scale(1./intFullSim);

    double intFastSim = TransShapeFastSim->Integral();
    TransShapeFastSim->Scale(1./intFastSim);

    TransShapeFastSim->SetLineColor(kRed);

    c->cd(2);

    TLegend* Legend = new TLegend(0.5, 0.7, 0.9., 0.9);

    gPad->SetLogy();

    string sTitle("Transverse shape E(Electron) = "); sTitle = sTitle + Form("%d", iMass); 
 
    TransShapeFullSim->SetStats(0);
    TransShapeFastSim->SetStats(0);

    TransShapeFullSim->SetTitle(sTitle.c_str());
    TransShapeFastSim->SetTitle(sTitle.c_str());

    if (bRebinTrans) {
      TransShapeFullSim->Rebin();     TransShapeFullSim->Rebin();      TransShapeFullSim->Rebin();
      TransShapeFastSim->Rebin();     TransShapeFastSim->Rebin();      TransShapeFastSim->Rebin();
    }

    TransShapeFullSim->DrawClone();
    TransShapeFastSim->DrawClone("SAME");

    double intFull = TransShapeFullSim->Integral();
    double intFast = TransShapeFastSim->Integral();

    double rateFullPrevious = -1;
    double rateFastPrevious = -1;
    
    double MrFull = -1.;//TransShapeFullSim->GetBinCenter(k);
    double MrFast = -1.;//TransShapeFastSim->GetBinCenter(k);

    for (int k = 1; k < TransShapeFullSim->GetNbinsX()+1; k++){
      
      double rateFull = TransShapeFullSim->Integral(1, k)/intFull;
      //     cout << "k = " << k << " rateFull = " << rateFull << endl;
      if (rateFull > 0.9 && rateFullPrevious < 0.9) {
	cout << "rateFull = " << rateFull << endl;
	//<< " TransShapeFullSim->GetBinCenter(k) = " 
	//		       << TransShapeFullSim->GetBinCenter(k) << endl;
	MrFull = TransShapeFullSim->GetBinCenter(k);

      }

      rateFullPrevious = rateFull;

      double rateFast = TransShapeFastSim->Integral(1, k)/intFast;
      if (rateFast > 0.9 && rateFastPrevious < 0.9) {
	cout << "rateFast = " << rateFast << endl;
      //" TransShapeFastSim->GetBinCenter(k) = " 
      //			       << TransShapeFastSim->GetBinCenter(k) << endl;

	MrFast = TransShapeFullSim->GetBinCenter(k);

      }

      rateFastPrevious = rateFast;

    }
    
    cout << "Mass = " << iMass << " Mr Full = " << MrFull << " Mr Fast = " <<  MrFast << endl;


    Legend->AddEntry(TransShapeFastSim, "Fast Sim", "l");
    Legend->AddEntry(TransShapeFullSim, "Full Sim", "f");

    Legend->Draw();

    c->cd(4);

    TLine* LT = new TLine(0, 1, 7, 1);
    LT->SetLineWidth(2);
    LT->SetLineStyle(2);

    TransShapeFastSim->SetMaximum(2.0);
    TransShapeFastSim->SetMinimum(0.0);

    TransShapeFastSim->SetYTitle("Fast/Full");

    TransShapeFastSim->Divide(TransShapeFullSim);
    TransShapeFastSim->Draw();

    LT->Draw("SAME");
    

    string sNamePng("ELECTRON_FORWARD/OUT_SHORTSTEPS/"); 

    if (!bRebinTrans) sNamePng = sNamePng + "" + sName + ".png";
    else sNamePng = sNamePng + "" + sName + "_COARSE.png";

    c->SaveAs(sNamePng.c_str());

  }

}
