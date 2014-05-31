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
    print "usage: %s [root file name]" % sys.argv[0]
    sys.exit()

canvas = TCanvas("canvas", "")
canvas.SetGrid()
canvas.SetLogy(1)
canvas.SetTopMargin(0.2)

legend = TLegend(0.1, 0.81, 0.9, 0.9)
legend.SetFillColor(0)


tfile = TFile(sys.argv[1])
tree = tfile.Get("tree")

max = 3500
bin_width = 14
n_bins = int(max/bin_width)

hist = TH1D("hist", "", n_bins, 0, 3500)
hist.SetXTitle("Energy [keV]")
hist.SetYTitle("Counts / %s keV" % hist.GetBinWidth(0))

print "%s entries" % tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> hist", "")

canvas.Update()
canvas.Print("test.pdf")

