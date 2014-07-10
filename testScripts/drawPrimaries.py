#!/usr/bin/env python

import os
import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TChain
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor
from ROOT import TH1D
from ROOT import TH2D


if len(sys.argv) < 2:
    print "usage: %s [root file name]" % sys.argv[0]
    sys.exit()

canvas = TCanvas("canvas", "")
canvas.SetTopMargin(0.2)

legend = TLegend(0.1, 0.81, 0.9, 0.9)
legend.SetFillColor(0)


#tfile = TFile(sys.argv[1])
#tree = tfile.Get("tree")

tree = TChain("tree")
for root_file in sys.argv[1:]:
    tree.Add(root_file)

prefix = os.path.commonprefix(sys.argv[1:])
prefix = os.path.splitext(os.path.basename(prefix))[0]
print prefix

max = 3500
bin_width = 14
n_bins = int(max/bin_width)

hist_xy = TH2D("hist_xy","x vs. y",50,-500,500,50,-500,500)
hist_xz = TH2D("hist_xz","x vs. z",50,-500,500,50,-500,500)
hist_yz = TH2D("hist_yz","y vs. z",50,-500,500,50,-500,500)

half_width = 0.25
hist_atomic_number = TH1D("hist_atomic_number", "atomic number", 80,
200-half_width, 240-half_width)
hist_charge = TH1D("hist_charge", "charge", 40, 80-half_width, 100-half_width)


print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventX : fMonteCarloData.fPrimaryEventY >> hist_xy", "", "goff")
hist_xy.Draw("colz")
canvas.Update()
canvas.Print("%s_xy.pdf" % prefix)

print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventX : fMonteCarloData.fPrimaryEventZ >> hist_xz", "", "goff")
hist_xz.Draw("colz")
canvas.Update()
canvas.Print("%s_xz.pdf" % prefix)

print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventY : fMonteCarloData.fPrimaryEventZ >> hist_yz", "", "goff")
hist_yz.Draw("colz")
canvas.Update()
canvas.Print("%s_yz.pdf" % prefix)

canvas.SetLogy(1)
color = TColor.kBlue
hist_atomic_number.SetLineColor(color)
hist_atomic_number.SetFillColor(color)
print "%s entries" % tree.Draw("fMonteCarloData.fParticleInformation.fAtomicNumber >> hist_atomic_number", "", "goff")
hist_atomic_number.Draw()
canvas.Update()
canvas.Print("%s_atomic_number.pdf" % prefix)

hist_charge.SetLineColor(color)
hist_charge.SetFillColor(color)
print "%s entries" % tree.Draw("fMonteCarloData.fParticleInformation.fCharge >> hist_charge", "", "goff")
hist_charge.Draw()
canvas.Update()
canvas.Print("%s_charge.pdf" % prefix)

