#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor
from ROOT import TH1D

if len(sys.argv) < 2:
    print "argument: [root file name]"
    sys.exit()

tfile = TFile(sys.argv[1])
tree = tfile.Get("tree")

#tree.Scan("fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy:fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution:fMonteCarloData.fPixelatedChargeDeposits.fConvContribution")


hist_all = TH1D("hist_all", "", 100, 0, 3500)
hist_all.SetLineWidth(2)
hist_compt = hist_all.Clone("hist_compt")
hist_compt.SetLineColor(TColor.kBlue)
hist_pp = hist_all.Clone("hist_pp")
hist_pp.SetLineColor(TColor.kRed)
hist_pe = hist_all.Clone("hist_pe")
hist_pe.SetLineColor(TColor.kGreen+1)

canvas = TCanvas("canvas", "")
canvas.SetGrid()
canvas.SetLogy(1)

canvas.SetTopMargin(0.2)
legend = TLegend(0.1, 0.81, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetNColumns(2)

legend.AddEntry(hist_all, "All counts", "l")
legend.AddEntry(hist_compt, "compton", "l")
legend.AddEntry(hist_pp, "pair prod", "l")
legend.AddEntry(hist_pe, "pe?", "l")

print "all:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_all", "")

print "compt:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_compt",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)>0", "same")

print "pp:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_pp",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)>0", "same")

print "none:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_pe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)==0", "same")

legend.Draw()
canvas.Update()
canvas.Print("plot_all.pdf")

tree.SetLineWidth(2)
tree.SetLineColor(TColor.kBlack)
print "all_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> h(100, 0, 3500)",
"@fChargeClusters.size()==1")
tree.SetLineColor(TColor.kBlue)
print "compt_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)>0 && @fChargeClusters.size()==1", "same")
tree.SetLineColor(TColor.kRed)
print "pp_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)>0 && @fChargeClusters.size()==1", "same")
tree.SetLineColor(TColor.kGreen+1)
print "none:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConvContribution)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonContribution)==0&& @fChargeClusters.size()==1", "same")

legend.Draw()
canvas.Update()
canvas.Print("plot_ss.pdf")

