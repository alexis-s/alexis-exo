#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TChain
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor
from ROOT import TH1D

if len(sys.argv) < 2:
    print "argument: [root file name]"
    sys.exit()

#tfile = TFile(sys.argv[1])
#tree = tfile.Get("tree")

tree = TChain("tree")
for root_file in sys.argv[1:]:
    tree.Add(root_file)

#tree.Scan("fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy:fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy:fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy")


hist_all = TH1D("hist_all", "", 100, 0, 3500)
hist_all.SetLineWidth(2)
hist_compt = hist_all.Clone("hist_compt")
hist_compt.SetLineColor(TColor.kBlue)
hist_pp = hist_all.Clone("hist_pp")
hist_pp.SetLineColor(TColor.kRed)
hist_pe = hist_all.Clone("hist_pe")
hist_pe.SetLineColor(TColor.kGreen+1)

hist_beta = hist_compt.Clone("hist_beta")

canvas = TCanvas("canvas", "")
canvas.SetGrid()
canvas.SetLogy(1)

canvas.SetTopMargin(0.2)
legend = TLegend(0.1, 0.81, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetNColumns(2)

legend.AddEntry(hist_all, "All counts", "l")
#legend.AddEntry(hist_compt, "compton", "l")
legend.AddEntry(hist_pp, "pair prod", "l")
#legend.AddEntry(hist_pe, "pe?", "l")

print "beta:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_beta",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fBetaEnergy)>0")

print "all:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_all", "")

#print "compt:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_compt",
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)>0", "same")

print "pp:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_pp",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)>0", "same")

#print "pe:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist_pe",
#"(Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy+fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0)", 
#"same")
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0", 

legend.Draw()
canvas.Update()
canvas.Print("plot_all.pdf")

hist_all.Draw()
hist_beta.Draw("same")
canvas.Update()
canvas.Print("plot_beta.pdf")

tree.SetLineWidth(2)
tree.SetLineColor(TColor.kBlack)
print "all_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> h(100, 0, 3500)", "@fChargeClusters.size()==1")

tree.SetLineColor(TColor.kRed)
print "pp_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)>0 && @fChargeClusters.size()==1", "same")

#tree.SetLineColor(TColor.kBlue)
#print "compt_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)>0 && @fChargeClusters.size()==1", "same")

#tree.SetLineColor(TColor.kGreen+1)
#print "pe_ss:", tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe", 
#"(Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy+fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0) && (@fChargeClusters.size()==1)", 
#"same")
#"(Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)==0) && (Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0) && (@fChargeClusters.size()==1)", 

#print tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe",
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0 && @fChargeClusters.size()==1")

#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)==0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)==0 && @fChargeClusters.size()==1")
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)>0 && @fChargeClusters.size()==1 ", "same")
#"Sum$(fMonteCarloData.fPixelatedChargeDeposits.fConversionEnergy)>0 && Sum$(fMonteCarloData.fPixelatedChargeDeposits.fComptonEnergy)>0 && @fChargeClusters.size()==1 ", "same")

legend.Draw()
canvas.Update()
canvas.Print("plot_ss.pdf")

