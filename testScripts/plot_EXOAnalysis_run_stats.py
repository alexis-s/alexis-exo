import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TChain
from ROOT import TColor


filenames = sys.argv[1:]


stats = TChain("stats")

for filename in filenames:
    print "--> adding %s" % filename
    stats.AddFile(filename)

#tfile = TFile(filename)
#stats = tfile.Get("stats")


digitizer_list = [
  "SmearMCIonizationEnergy", 
  "DigitizeAPDs", 
  "DigitizeWires", 
  "ResetWires",
  "GenerateWireSignalAt", 
  "ShapeWireSignals", 
  "DoADCSamplingWires",
  "AddNoiseToWireSignals", 
  "ScaleAndDigitizeWireSignals", 
  "TrimSaturatedSignals"
]

recon_list = [
"define_cross_product", 
"define_apd_sums", 
"matched_filter_finder",
"uwire_adjacent_ind_sig_finder.PrepareMatchFilter",
"uwire_adjacent_ind_sig_finder.ApplyMatchFilter", 
"multiple_sig_finder",
"apd_gang_finder", 
"uwire_adjacent_ind_sig_finder", 
"u_and_apd_fitter",
"u_and_apd_fitter.FitAndGetChiSquare", 
"u_and_apd_fitter.CalculateBaselineAndNoise",
"u_and_apd_fitter.AddAPDSignal", 
"u_and_apd_fitter.AddUWireSignal",
"u_and_apd_fitter.AddVWireSignal"
]


stats.SetFillColor(TColor.kBlue+1)


canvas = TCanvas("canvas", "")
canvas.SetLogy(1)

for item in digitizer_list:
    print item

    stats.Draw("DigitizerStatistics.fTimingInfo.fTotalCpuTime",
    "DigitizerStatistics.fTimingInfo.fWatchName.Data()==\""+item+"\"")

    canvas.Print("%s.pdf" % item)

for item in recon_list:
    print item

    stats.Draw("ReconStatistics.fTimingInfo.fTotalCpuTime",
    "ReconStatistics.fTimingInfo.fWatchName.Data()==\""+item+"\"")

    canvas.Print("%s.pdf" % item)

