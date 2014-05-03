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
from ROOT import TLegend



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


    # create a dict of info for each hist to be created:
    hist_info = []

    hist_info.append({
      "title": "Energy deposited in LXe sum", 
      "draw_string": "fMonteCarloData.fTotalEnergyInLiquidXe", 
    }) 

    # this is not really calibrated!
    hist_info.append({
      "title": "Sum Raw Energy Clusters", 
      "draw_string": "Sum$(fChargeClusters.fRawEnergy)", 
    }) 

    hist_info.append({
      "title": "PCD Sum energy", 
      "draw_string": "Sum$(fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy)*1e3", 
    }) 

    # FIXME -- selection isn't being used
    # hist, draw string

    # loop over hist_lists, create empty hists with the specified info:
    for i, hist_dict in enumerate(hist_info):

        name = "hist%i_dir%s" % (i, suffix)
        hist_dict["name"] = name
        
        title = "%(title)s: %(draw_string)s" % hist_dict
        hist = create_hist(name, title)
        hist_dict["hist"] = hist
        #print hist_dict


    root_filenames = glob.glob("%s/*.root" % directory)
    print "%i files" % len(root_filenames)


    for (i_file, root_filename) in enumerate(root_filenames):

        print "\t processing file %i of %i: %s" % (
            i_file, 
            len(root_filenames),
            root_filename,
        )

        try:
            root_file = TFile(root_filename)
            tree = root_file.Get("tree")
            n_entries = tree.GetEntries()
            print "\t\t %i entries" % n_entries
        except:
            print "BAD FILE"
            continue

        tree.GetEntry(0)
        svn_revision = tree.EventBranch.fEventHeader.fSVNRevision
        build_id = tree.EventBranch.fEventHeader.fBuildID

        if i_file == 0:
            prev_svn_revision = svn_revision
        if svn_revision != prev_svn_revision:
            print "SVN version changed!!"
        #print "\t\t", svn_revision, build_id

        hist_info[0]["hist"].GetDirectory().cd()


        for hist_dict in hist_info:

            draw_string = "%(draw_string)s >>+ %(name)s" % hist_dict
            #print draw_string
            tree.Draw(draw_string)
            #print "\t\t%i entries in %(name)s: %(title)s" % (n_entries, hist_dict)
            hist_dict["svn_revision"] = svn_revision
            hist_dict["build_id"] = build_id
            hist_dict["n_entries"] = hist.GetEntries()

        if i_file > 500: # debugging
            print "====> STOPPING AT FILE %s!" % i_file
            break 


    for hist_dict in hist_info:

        print "--> scaling %(name)s" % hist_dict
        hist = hist_dict["hist"]
        hist.Scale(1.0/hist.GetEntries())
        hist_dict["n_entries"] = hist.GetEntries()

    return hist_info


def main(directory1, directory2):

    hist_info1 = process_directory(directory1, "1")
    hist_info2 = process_directory(directory2, "2")


    canvas = TCanvas("canvas", "")
    canvas.SetTopMargin(0.2)
    canvas.SetLogy(1)

    for i in xrange(len(hist_info1)):

        print "hists", i

        hist_dict1 = hist_info1[i] 
        hist_dict2 = hist_info2[i] 

        hist1 = hist_dict1["hist"]
        hist2 = hist_dict2["hist"]

        legend = TLegend(0.1, 0.8, 0.9, 0.9)
        legend_entry = "%(build_id)s, %(n_entries).1e entries"
        legend.AddEntry(hist1, legend_entry % hist_dict1, "l")
        legend.AddEntry(hist2, legend_entry % hist_dict2, "l")

        hist1.Draw()
        hist2.SetLineColor(2)
        hist2.Draw("same")
        legend.Draw()

        canvas.Update()
        canvas.Print("%s.pdf" % hist1.GetName())



if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "arguments: [directory of root files 1] [directory of root files 2]"
        sys.exit(1)


    main(sys.argv[1], sys.argv[2])
    #process_directory(sys.argv[1], "1")








