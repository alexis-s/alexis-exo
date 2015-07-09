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
from ROOT import TColor
from ROOT import TLegend


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
    # cut off leading stuff from start and "new" from end
    title = "_".join(basename[2:-2])

    # grab data hists
    tfile = TFile(file_name)
    hist_ss_data = tfile.Get("Th-228_5_ss_data")
    hist_ss_data.SetTitle("%s_ss" % title)
    hist_ms_data = tfile.Get("Th-228_5_ms_data")
    hist_ms_data.SetTitle("%s_ms" % title)
    blue = TColor.kBlue
    width=2
    hist_ms_data.SetLineColor(TColor.kBlack)
    hist_ss_data.SetLineColor(TColor.kBlack)
    print "data hist color", hist_ms_data.GetLineColor()

    
    # grab mc hists
    hist_ss_mc = tfile.Get("Th-228_5_ss_mc")
    hist_ms_mc = tfile.Get("Th-228_5_ms_mc")
    hist_ss_mc.SetLineColor(blue)
    hist_ms_mc.SetLineColor(blue)
    print "MC hist color", hist_ms_mc.GetLineColor()

    # grab ratio hists
    hist_ss_ratio = tfile.Get("Th-228_5_ss_ratio")
    hist_ms_ratio = tfile.Get("Th-228_5_ms_ratio")
    hist_ss_ratio.SetLineColor(blue)
    hist_ms_ratio.SetLineColor(blue)
    print "ratio hist color", hist_ms_ratio.GetLineColor()

    for hist in [hist_ss_mc, hist_ms_mc, hist_ms_data, hist_ss_data]:
        hist.SetXTitle("Energy [keV]")
        hist.SetYTitle("Counts")
        hist.SetLineWidth(width)

    for hist in [hist_ss_ratio, hist_ms_ratio]:
        hist.SetXTitle("Energy [keV]")
        hist.SetYTitle("Ratio")
        hist.SetLineWidth(width)

    # draw ms stuff
    pad1.cd()
    pad1.SetLogy(1)
    pad1.SetGrid(1,1)
    hist_ms_data.Draw()
    hist_ms_data.SetMaximum(3e5)
    hist_ms_data.SetMinimum(1e2)
    hist_ms_mc.Draw("same hist")
    hist_ms_data.Draw("same")
    pad2.cd()
    pad2.SetGrid(1,1)
    hist_ms_ratio.SetMaximum(1.4)
    hist_ms_ratio.SetMinimum(0.6)
    hist_ms_ratio.Draw("hist")
    canvas.Update()
    canvas.Print("ms_%s.png" % title)

    # draw ss stuff
    pad1.cd()
    pad1.SetLogy(1)
    pad1.SetGrid(1,1)
    hist_ss_data.Draw()
    hist_ss_data.SetMaximum(1e5)
    hist_ss_mc.Draw("same hist")
    hist_ss_data.Draw("same")
    pad2.cd()
    pad2.SetGrid(1,1)
    #pad2.SetLogy(1) # not possible with negative error bars
    hist_ss_ratio.Draw("hist")
    #hist_ss_ratio.SetMaximum(12.0)
    hist_ss_ratio.SetMaximum(1.5)
    hist_ss_ratio.SetMinimum(0.5)
    canvas.Update()
    canvas.Print("ss_%s.png" % title)


def draw_ratio_comparison(filenames):
    print "drawing ratio comparison of n files=", len(filenames)

    canvas = TCanvas("canvas", "") #, 600, 700)
    canvas.SetGrid(1,1)
    canvas.SetTopMargin(0.15)

    blue = TColor.kBlue
    width=2

    out_file = TFile("hist_comparison.root","recreate")
    tfiles = []
    ss_ratio_hists = []
    ms_ratio_hists = []
    titles = []

    for file_name in filenames:

        # grab data hists
        tfile = TFile(file_name)
        # grab ratio hists
        hist_ss_ratio = tfile.Get("Th-228_5_ss_ratio")
        hist_ms_ratio = tfile.Get("Th-228_5_ms_ratio")
        for hist in [hist_ss_ratio, hist_ms_ratio]:
            hist.SetXTitle("Energy [keV]")
            hist.SetYTitle("Ratio")
            hist.SetLineColor(blue)
            hist.SetLineWidth(width)

        # for a title
        basename = os.path.basename(file_name)
        basename = os.path.splitext(basename)[0]
        basename = basename.split("_")
        title = " ".join(basename[2:-2])

        # store everything in a list, for a hack solution for keeping things in
        # memory
        tfiles.append(tfile)
        ss_ratio_hists.append(hist_ss_ratio)
        ms_ratio_hists.append(hist_ms_ratio)
        titles.append(title)

    legend = TLegend(0.1, 0.86, 0.9, 0.98)
    legend.SetNColumns(2)

    colors = [1,2,3,4,6,9]

    # draw ss ratio hists
    for (i, title) in enumerate(titles):
        print title
        hist_ss_ratio = ss_ratio_hists[i]
        hist_ss_ratio.SetLineColor(colors[i])
        #hist_ss_ratio.SetFillColor(colors[i])
        legend.AddEntry(hist_ss_ratio, title, "lf")
        if i ==0:
            hist_ss_ratio.Draw("hist")
            hist_ss_ratio.SetMaximum(1.5)
            hist_ss_ratio.SetMinimum(0.5)
        else:
            hist_ss_ratio.Draw("hist same")

    legend.Draw()
    canvas.Update()
    canvas.Print("ss_ratios.png")

    # draw ms ratio hists
    for (i, title) in enumerate(titles):
        print title
        hist_ms_ratio = ms_ratio_hists[i]
        hist_ms_ratio.SetLineColor(colors[i])
        #hist_ms_ratio.SetFillColor(colors[i])
        #legend.AddEntry(hist_ms_ratio, title, "l")
        if i ==0:
            hist_ms_ratio.Draw("hist")
            hist_ms_ratio.SetMaximum(1.5)
            hist_ms_ratio.SetMinimum(0.5)
        else:
            hist_ms_ratio.Draw("hist same")

    legend.Draw()
    canvas.Update()
    canvas.Print("ms_ratios.png")




if __name__ == "__main__":

    file_names = sys.argv[1:]
    for file_name in file_names:
        process_file(file_name)
        #pass

    draw_ratio_comparison(file_names)

