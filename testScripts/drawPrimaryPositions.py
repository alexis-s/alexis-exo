#!/usr/bin/env python

import os
import sys
import glob

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TChain
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor
from ROOT import TH1D
from ROOT import TH2D


# options:
do_debug = False

if len(sys.argv) < 2:
    print "usage: %s [directories of root files]" % sys.argv[0]
    sys.exit()
    
directories = sys.argv[1:]
chains = []
hists_xy = []

for (index, directory) in enumerate(directories):

    suffix = os.path.split(directory)[-1]
    folders = directory.split("/")
    suffix = folders[-1]
    if suffix == "":
        suffix = folders[-2]
    
    print "suffix", suffix


    hist = TH2D("hist_xy_%s" % suffix,"x vs. y",50,-1000,1000,50,-1000,1000)
    hist.SetMarkerColor(index+1)
    hist.SetLineColor(index+1)
    hists_xy.append(hist)


print "you provided %i directories" % len(directories)

for (index, directory) in enumerate(directories):

    print "directory %i: %s" % (index, directory)

    root_files = glob.glob("%s/*.root" % directory)
    print "%i root files" % len(root_files)


    tree = TChain("tree")
    if do_debug: # only use first 100 files
        root_files = root_files[:100]

    for root_file in root_files:
        print root_file
        tree.Add(root_file)

    tree.SetLineColor(index+1)
    tree.SetMarkerColor(index+1)
    chains.append(tree)



canvas = TCanvas("canvas", "")
canvas.SetTopMargin(0.2)

legend = TLegend(0.1, 0.81, 0.9, 0.9)
legend.SetFillColor(0)



#prefix = os.path.commonprefix(sys.argv[1:])
#prefix = os.path.splitext(os.path.basename(prefix))[0]
#print prefix



for (index, tree) in enumerate(chains):

    options = ""
    if index > 0:
        options = " same"

    hist.GetDirectory().cd()
    hist = hists_xy[index]
    name = hist.GetName()

    draw_string = "fMonteCarloData.fPrimaryEventX : fMonteCarloData.fPrimaryEventY"
    draw_string += " >> %s " % name


    #if index == 0:
    #    draw_string += " >> h(50, -1000, 1000, 50, -1000, 1000)"


    n_events = tree.Draw(draw_string, "", options)
    print "--> drawing chain %i: %s" % (index, name)
    print "%s, %s" % (draw_string, options)
    print "%i events" % n_events
    print "color: %i" % tree.GetLineColor()
    canvas.Update()
    canvas.Print("%s.pdf" % name)


for (index, hist) in enumerate(hists_xy):
    if index == 0:
        hist.Draw()
    else:
        hist.Draw("same")

canvas.Update()
canvas.Print("hist_xy.pdf")

sys.exit()

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

