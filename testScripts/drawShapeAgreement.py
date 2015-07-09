#!/bin/env python

"""
draw results from shape agreement plots
"""
import os
import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TPad

def process_file(file_name):
    print "--> processing", file_name

    canvas = TCanvas("canvas", "", 600, 700)

    pad1 = TPad("pad1", "", 0.0, 0.5, 1.0, 1.0)
    pad1.Draw()

    pad2 = TPad("pad2", "", 0.0, 0.0, 1.0, 0.5)
    pad2.Draw()

    basename = os.path.basename(file_name)
    basename = os.path.splitext(basename)[0]
    basename = basename.split("_")
    title = "_".join(basename[2:])

    # grab data hists
    tfile = TFile(file_name)
    hist_ss_data = tfile.Get("Th-228_5_ss_data")
    hist_ss_data.SetTitle("%s_ss" % title)
    hist_ms_data = tfile.Get("Th-228_5_ms_data")
    hist_ms_data.SetTitle("%s_ms" % title)
    
    # grab mc hists
    hist_ss_mc = tfile.Get("Th-228_5_ss_mc")
    hist_ms_mc = tfile.Get("Th-228_5_ms_mc")

    # grab ratio hists
    hist_ss_ratio = tfile.Get("Th-228_5_ss_ratio")
    hist_ms_ratio = tfile.Get("Th-228_5_ms_ratio")

    # draw ms stuff
    pad1.cd()
    pad1.SetLogy(1)
    pad1.SetGrid(1,1)
    hist_ms_data.Draw()
    hist_ms_data.SetMaximum(3e5)
    hist_ms_data.SetMinimum(1e2)
    hist_ms_mc.Draw("same hist")
    pad2.cd()
    pad2.SetGrid(1,1)
    hist_ms_ratio.SetMaximum(1.4)
    hist_ms_ratio.SetMinimum(0.6)
    hist_ms_ratio.Draw("hist")
    canvas.Update()
    canvas.Print("ms_%s.pdf" % title)

    # draw ss stuff
    pad1.cd()
    pad1.SetLogy(1)
    pad1.SetGrid(1,1)
    hist_ss_data.Draw()
    hist_ss_data.SetMaximum(1e5)
    hist_ss_mc.Draw("same hist")
    pad2.cd()
    pad2.SetGrid(1,1)
    #pad2.SetLogy(1) # not possible with negative error bars
    hist_ss_ratio.Draw("hist")
    #hist_ss_ratio.SetMaximum(12.0)
    hist_ss_ratio.SetMaximum(1.5)
    hist_ss_ratio.SetMinimum(0.5)
    canvas.Update()
    canvas.Print("ss_%s.pdf" % title)



if __name__ == "__main__":

    file_names = sys.argv[1:]
    for file_name in file_names:
        process_file(file_name)
