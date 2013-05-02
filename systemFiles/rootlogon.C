{

  cout << "this is alexis' rootlogon.C" << endl;

  gROOT->SetStyle("Plain");     
  gStyle->SetOptStat(0);        // suppress box on plots
  gStyle->SetPalette(1);        // rainbow palette

  // use consistent number of decimal places in plots:
  gStyle->SetStripDecimals(kFALSE);

}
