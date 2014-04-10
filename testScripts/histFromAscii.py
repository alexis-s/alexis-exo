#!/usr/bin/env python

"""
Looking at binned VdA Material Screening results for nEXO UHMW PE, from 04 Apr
2014.

09 Apr 2014 AGS
"""

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TCanvas

import sys

if len(sys.argv) < 2:
    print "argument: [text file MCA spectrum]"

filename = sys.argv[1]

print "processing %s" % filename
binned_file = file(filename)

lines = binned_file.readlines()

n_bins = len(lines)
print "there are %i bins" % n_bins

# almost calibrated
min_bin = 3.3942 # a0
max_bin = 0.2062 * n_bins # a1

hist = TH1D("hist", "", n_bins, 0, max_bin)

for (i, bin_content) in enumerate(lines):
    
    print "%i | %s" % (i, bin_content)

    bin_content = float(bin_content)
    hist.SetBinContent(i+1, bin_content)


hist.Rebin(10)

canvas = TCanvas("canvas", "")
canvas.SetLogy(1)
hist.Draw()
canvas.Update()
canvas.Print("hist.pdf")


