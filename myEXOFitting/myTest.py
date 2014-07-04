from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT,sys,subprocess,os,shutil,glob
from optparse import OptionParser
import sys

if len(sys.argv) < 2:
    print "argument: pre-proc root file"
    sys.exit(1)

ROOT.gSystem.Load("../lib/libEXOFitting");
ROOT.EXOFitter fitter;
#fitter->SetHexCut(163,5,182);
fitter.BuildWorkspace();
fitter.BuildRotationModel();
#RooRealVar sd("standoff_distance","standoff_distance",0,200);
#RooWorkspace* wsp = fitter.GetWorkspace();
#wsp->import(sd);
#TString path = "path to MC here";
fitter.BuildPdf(sys.argv[1],"test_pdf",true);
fitter.SaveWorkspace("myWorkspace.root")
