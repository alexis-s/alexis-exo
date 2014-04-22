#!/usr/bin/env python

"""
This script is based on Jeff Wood's GeantComparisonScriptSingleFiles.C.
This is being used to compare EXOAnalysis output before and after incorporation
of neutron capture code.

wish list:
* more flexibility in axis labels (CCs are not in keV)
* add position info
* add legends
* add meaningful file names

11 Apr 2014 A.G. Schubert
"""

import sys
import glob

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile
from ROOT import TCanvas



def create_hist(name, title=""):

    print "--> creating hist: name = %s, title = %s" % (name, title) 

    # options for hist binning, in keV:
    binWidth = 14.0
    minE = 0.0
    maxE = 3500.0 # even number of bins, 14-keV wide
    nBins = int((maxE - minE)/binWidth)
    print "\t minE = %.2f | maxE = %.2f | binWidth = %.2f | nBins = %.2f" % (minE, maxE, binWidth, nBins)
    maxE = minE + nBins*binWidth
    print "\t minE = %.2f | maxE = %.2f | binWidth = %.2f | nBins = %.2f" % (minE, maxE, binWidth, nBins)


    #print minE, maxE, nBins

    hist = TH1D(name, title, nBins, minE, maxE)
    hist.SetXTitle("Energy [keV]")
    hist.SetLineWidth(2)

    return hist


def process_directory(
    directory, # directory w root files
    suffix,    # hist name suffix
):


    print "--> processing directory:", directory


    # these hists will get created (hist title, draw string, selection):
    hist_lists = []
    hist_lists.append(("Energy deposited in LXe sum", "fMonteCarloData.fTotalEnergyInLiquidXe", "")) 

    # this is not really calibrated!
    hist_lists.append(("Sum Raw Energy Clusters", "Sum$(fChargeClusters.fRawEnergy)", ""))
    hist_lists.append(("PCD Sum energy", "Sum$(fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy)*1e3", ""))


    hist_info = []

    # loop over hist_lists, create empty hists with the specified info:
    for i, hist_list in enumerate(hist_lists):

        (title, draw_string, selection) = hist_list
        name = "hist%i" % i

        
        title = "%s: %s" % (title, draw_string)
        if selection != "": title += " {%s}" % selection
        hist = create_hist(name, title)
        hist_info.append((hist, draw_string))

    for hist_list in hist_lists:
        print hist_list


    root_filenames = glob.glob("%s/*.root" % directory)
    print "%i files" % len(root_filenames)


    for root_filename in root_filenames:

        print "\t processing", root_filename
        try:
            root_file = TFile(root_filename)
            tree = root_file.Get("tree")
            n_entries = tree.GetEntries()
            print "\t\t %i entries" % n_entries
        except:
            print "BAD FILE"
            continue

        hist_info[0][0].GetDirectory().cd()


        for (hist, draw_string) in hist_info:

            name = hist.GetName()
            tree.Draw("%s >> +%s" % (draw_string, name))
            print "\t\t%i entries in %s: %s" % (hist.GetEntries(), name, hist.GetTitle())


    hists = []

        print "--> scaling %s" % hist.GetName()
        hist.Scale(1.0/hist.GetEntries())
        hists.append(hist)

    return hists


def main(directory1, directory2):

    hists1 = process_directory(directory1, "1")
    hists2 = process_directory(directory2, "2")


    canvas = TCanvas("canvas", "")
    canvas.SetLogy(1)

    for i in xrange(len(hists1)):

        print "hists", i

        hist1 = hists1[i]
        hist2 = hists2[i]

        hist1.Draw()
        hist2.SetLineColor(2)
        hist2.Draw("same")

        canvas.Update()
        canvas.Print("%s.pdf" % hist1.GetName())



if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "arguments: [directory of root files 1] [directory of root files 2]"
        sys.exit(1)


    main(sys.argv[1], sys.argv[2])
    #process_directory(sys.argv[1], "1")








