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

max = 3500
bin_width = 14
n_bins = int(max/bin_width)

hist_xy = TH2D("hist_xy","x vs. y",50,-500,500,50,-500,500)
hist_xz = TH2D("hist_xz","x vs. z",50,-500,500,50,-500,500)
hist_yz = TH2D("hist_yz","y vs. z",50,-500,500,50,-500,500)


print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventX : fMonteCarloData.fPrimaryEventY >> hist_xy", "", "goff")
print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventX : fMonteCarloData.fPrimaryEventZ >> hist_xz", "", "goff")
print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventY : fMonteCarloData.fPrimaryEventZ >> hist_yz", "", "goff")

hist_xy.Draw("colz")
canvas.Update()
canvas.Print("xy.pdf")

hist_xz.Draw("colz")
canvas.Update()
canvas.Print("xz.pdf")

hist_yz.Draw("colz")
canvas.Update()
canvas.Print("yz.pdf")
