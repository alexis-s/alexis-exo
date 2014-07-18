#!/usr/bin/env python

"""
Draw positions, atomic number, and proton number of primaries. 
Generate pdf files and root file.

arguments: [root files of MC output]
"""

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

#-------------------------------------------------------------------------------
# options:
#-------------------------------------------------------------------------------

do_debug = False
selection = "(fMonteCarloData.fPrimaryEventZ < 400) && (fMonteCarloData.fPrimaryEventZ > -400)"

# for x, y, z [mm]:
n_bins = 200
max_bin = 800
min_bin = -max_bin

title_offset = 1.4
margin = 0.13

#-------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print "usage: %s [root file name]" % sys.argv[0]
    sys.exit()



canvas = TCanvas("canvas", "", 700, 700)
canvas.SetTopMargin(margin)
canvas.SetBottomMargin(margin)
canvas.SetLeftMargin(margin)
canvas.SetRightMargin(margin)

prefix = os.path.commonprefix(sys.argv[1:])
prefix = os.path.splitext(os.path.basename(prefix))[0]
print prefix

# open a new root file
out_file = TFile("%s.root" % prefix, "recreate")

# setup hists:
hist_xy = TH2D("hist_xy", prefix, n_bins, min_bin, max_bin, n_bins, min_bin, max_bin)
hist_xy.GetXaxis().SetTitleOffset(title_offset)
hist_xy.GetYaxis().SetTitleOffset(title_offset)
hist_xy.SetTitle(";x [mm];y [mm]")

hist_xz = TH2D("hist_xz", prefix, n_bins, min_bin, max_bin, n_bins, min_bin, max_bin)
hist_xz.GetXaxis().SetTitleOffset(title_offset)
hist_xz.GetYaxis().SetTitleOffset(title_offset)
hist_xz.SetTitle(";z [mm];x [mm]")

hist_yz = TH2D("hist_yz", prefix, n_bins, min_bin, max_bin, n_bins, min_bin, max_bin)
hist_yz.GetXaxis().SetTitleOffset(title_offset)
hist_yz.GetYaxis().SetTitleOffset(title_offset)
hist_yz.SetTitle(";z [mm];y [mm]")

half_width = 0.25
hist_atomic_number = TH1D("hist_atomic_number", "", 80, 200-half_width, 240-half_width)
hist_atomic_number.GetXaxis().SetTitle("atomic number")
hist_n_protons = TH1D("hist_n_protons", "", 40, 80-half_width, 100-half_width)
hist_n_protons.GetXaxis().SetTitle("n protons")


root_files = sys.argv[1:]
if do_debug: # only use first 100 files
    print "====> debugging!!"
    root_files = root_files[:100]

tree = TChain("tree")
print "--> adding %i files" % len(root_files)
for root_file in root_files:
    tree.Add(root_file)


hist_xy.GetDirectory().cd()
canvas.SetLogz(1)

print "%s entries" % tree.Draw("fMonteCarloData.fPrimaryEventY : fMonteCarloData.fPrimaryEventX >> hist_xy", "", "goff")
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

hist_n_protons.SetLineColor(color)
hist_n_protons.SetFillColor(color)
print "%s entries" % tree.Draw("fMonteCarloData.fParticleInformation.fCharge >> hist_n_protons", "", "goff")
hist_n_protons.Draw()
canvas.Update()
canvas.Print("%s_n_protons.pdf" % prefix)


out_file.Write()
out_file.Close()

