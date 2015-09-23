"""
draw results from shape agreement plots


To make the input files, SS and MS MC were independently normalized to integral
of data hists in range from 500 to 3500 keV. 

29 Apr 2015
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

def print_integral(hist):
    """
    214 bins
    hist min: 500 keV
    hist max: 3500 keV
    """
    
    #print "low edge 0", hist.GetBinLowEdge(0)
    #print "low edge 1", hist.GetBinLowEdge(1)
    #print "low edge 980", hist.GetBinLowEdge(hist.FindBin(980))
    #print "high edge 214", hist.GetBinLowEdge(hist.GetNbinsX()) + hist.GetBinWidth(1)
    #print "n bins", hist.GetNbinsX()

    integral = hist.Integral(
        hist.FindBin(980), 
        hist.FindBin(3500)
    )
    print "integral of %s: %.2f" % (hist.GetName(), integral)
    return integral

def process_file(file_name):
    print "--> processing", file_name

    canvas = TCanvas("canvas", "", 600, 700)
    canvas.SetGrid(1, 1)

    pad1 = TPad("pad1", "", 0.0, 0.5, 1.0, 1.0)
    pad1.SetGrid(1,1)
    pad1.Draw()

    pad2 = TPad("pad2", "", 0.0, 0.0, 1.0, 0.5)
    pad2.SetGrid(1,1)
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
    blue = TColor.kBlue
    width=2
    hist_ms_data.SetLineColor(TColor.kBlack)
    hist_ss_data.SetLineColor(TColor.kBlack)
    #print "data hist color", hist_ms_data.GetLineColor()
    
    # grab mc hists
    hist_ss_mc = tfile.Get("Th-228_5_ss_mc")
    hist_ms_mc = tfile.Get("Th-228_5_ms_mc")
    hist_ss_mc.SetLineColor(blue)
    hist_ms_mc.SetLineColor(blue)
    #print "MC hist color", hist_ms_mc.GetLineColor()

    # print integrals
    integral_ss_data = print_integral(hist_ss_data)
    integral_ss_mc = print_integral(hist_ss_mc)
    integral_ms_data = print_integral(hist_ms_data)
    integral_ms_mc = print_integral(hist_ms_mc)

    # rescale mc hists
    print "ms scale factor", integral_ms_data/integral_ms_mc
    #hist_ms_mc.Scale(integral_ms_data/integral_ms_mc)
    print "ss scale factor", integral_ss_data/integral_ss_mc
    #hist_ss_mc.Scale(integral_ss_data/integral_ss_mc)

    # grab ratio hists
    hist_ss_ratio = tfile.Get("Th-228_5_ss_ratio")
    hist_ms_ratio = tfile.Get("Th-228_5_ms_ratio")
    hist_ss_ratio.SetLineColor(blue)
    hist_ms_ratio.SetLineColor(blue)
    #print "ratio hist color", hist_ms_ratio.GetLineColor()

    for hist in [hist_ss_mc, hist_ms_mc, hist_ms_data, hist_ss_data]:
        hist.SetXTitle("Energy [keV]")
        hist.SetYTitle("Counts")
        hist.SetLineWidth(width)
    hist_ss_ratio.SetTitle(hist_ss_ratio.GetName())
    hist_ms_ratio.SetTitle(hist_ms_ratio.GetName())
    hist_ms_ratio.SetMaximum(1.5)
    hist_ms_ratio.SetMinimum(0.5)
    hist_ss_ratio.SetMaximum(1.5)
    hist_ss_ratio.SetMinimum(0.5)

    # set axis to see normal energy range
    for hist in (hist_ss_ratio, hist_ms_ratio, hist_ss_mc, hist_ms_mc,
      hist_ss_data, hist_ms_data):
        #hist.SetAxisRange(980.0, 3500.0)
        pass

    # draw ms stuff
    pad1.cd()
    hist_ms_data.Draw()
    hist_ms_data.SetMaximum(500e3)
    hist_ms_mc.Draw("same hist")
    pad2.cd()
    hist_ms_ratio.Draw()
    canvas.Update()
    canvas.Print("%s_ms.png" % title)

    # draw ss stuff
    pad1.cd()
    hist_ss_data.Draw()
    hist_ss_data.SetMaximum(350e3)
    hist_ss_mc.Draw("same hist")
    pad2.cd()
    hist_ss_ratio.Draw()
    canvas.Update()
    canvas.Print("ss_%s.png" % title)


def draw_ratio_comparison(filenames):
    n_files = len(filenames)
    print "drawing ratio comparison of n files=", n_files

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

    if n_files > 2:
        legend = TLegend(0.1, 0.86, 0.9, 0.98)
    else:
        legend = TLegend(0.1, 0.86, 0.9, 0.9)
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
    canvas.Print("ss_ratios_%i.png" % n_files)

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
    canvas.Print("ms_ratios_%i.png" % n_files)

    canvas.Print("%s_ss.png" % title)



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "arguments: root files of shape agreement studies"

    file_names = sys.argv[1:]
    for file_name in file_names:
        process_file(file_name)

    draw_ratio_comparison(file_names)
