{ 
 f1 = new TFile("ZGJ_Skim_Skim.root","UPDATE");
 f2 = new TFile("WWG_Skim_Skim.root","UPDATE");
 f = new TFile("TMVA_ZGJ_WWG.root","UPDATE");
 f->cd();
 TTree *t1; f1->GetObject("Events",t1);
 TTree *t2; f2->GetObject("Events",t2);
 
 t1->SetName("TreeB");
 t1->CloneTree()->Write();
 t2->SetName("TreeS");
 t2->CloneTree()->Write();

}
