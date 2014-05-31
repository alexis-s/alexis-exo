#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor

if len(sys.argv) < 2:
    print "argument: [root file name]"
    sys.exit()

tfile = TFile(sys.argv[1])
tree = tfile.Get("tree")

#tree.Scan("fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy:fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution:fMonteCarloData.fPixelatedChargeDeposits.fConvContribution")


canvas = TCanvas("canvas", "")
canvas.SetGrid()
legend = TLegend(0.1, 0.9, 0.9, 0.99)

tree.SetLineWidth(2)
tree.SetLineColor(TColor.kBlack)
print "all:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> h(100, 0, 3500)", "")
legend.AddEntry(tree, "All counts", "l")
tree.SetLineColor(TColor.kBlue)
print "compt:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)>0", "same")
tree.SetLineColor(TColor.kRed)
print "pp:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)>0", "same")
tree.SetLineColor(TColor.kGreen)
print "none:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)==0", "same")

canvas.Update()
canvas.Print("plot_all.pdf")

tree.SetLineColor(TColor.kBlack)
print "all_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> h(100, 0, 3500)",
"@fChargeClusters.size()==1")
tree.SetLineColor(TColor.kBlue)
print "compt_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)>0 && @fChargeClusters.size()==1", "same")
tree.SetLineColor(TColor.kRed)
print "pp_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)>0 && @fChargeClusters.size()==1", "same")
tree.SetLineColor(TColor.kGreen)
print "none:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)==0&& @fChargeClusters.size()==1", "same")

canvas.Update()
canvas.Print("plot_ss.pdf")

