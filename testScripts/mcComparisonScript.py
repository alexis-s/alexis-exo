#!/usr/bin/env python

"""
This script is based on Jeff Wood's GeantComparisonScriptSingleFiles.C.
This is being used to compare EXOAnalysis output before and after incorporation
of neutron capture code.

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

    # options for hist binning, in keV:
    binWidth = 14.0
    minE = 0.0
    maxE = 10010.0 # even number of bins, 14-keV wide
    nBins = int((maxE - minE)/binWidth)

    #print minE, maxE, nBins

    hist = TH1D(name, title, nBins, minE, maxE)
    hist.SetXTitle("Energy [keV]")

    return hist


def process_directory(
    directory, # directory w root files
    suffix,    # hist name suffix
):


    print "--> processing directory:", directory

    histTotELXe = create_hist("histTotELXe_%s" % suffix, "Total Energy in LXe")
    histCCRawE = create_hist("histCCRawE_%s" % suffix, "CC Sum energy")
    histSumPCDE = create_hist("histSumPCDE_%s" % suffix, "PCD Sum energy")


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

        histTotELXe.GetDirectory().cd()

        tree.Draw("fMonteCarloData.fTotalEnergyInLiquidXe >> +%s" % histTotELXe.GetName())
        print "%i entries in hist %s " % (histTotELXe.GetEntries(), histTotELXe.GetName())

        tree.Draw("Sum$(fChargeClusters.fRawEnergy) >> +%s" % histCCRawE.GetName())
        print "%i entries in hist %s " % (histCCRawE.GetEntries(), histCCRawE.GetName())

        tree.Draw("Sum$(fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy)*1e3 >> +%s" % histSumPCDE.GetName())
        print "%i entries in hist %s " % (histSumPCDE.GetEntries(), histSumPCDE.GetName())

    histTotELXe.Scale(1.0/histTotELXe.GetEntries())
    histCCRawE.Scale(1.0/histCCRawE.GetEntries())
    histSumPCDE.Scale(1.0/histSumPCDE.GetEntries())

    return (histTotELXe, histCCRawE, histSumPCDE)


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
        canvas.Print("%s_vs_%s.pdf" % (hist1.GetName(), hist2.GetName()) )



if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "arguments: [directory of root files 1] [directory of root files 2]"
        sys.exit(1)


    main(sys.argv[1], sys.argv[2])
    #process_directory(sys.argv[1], "1")








