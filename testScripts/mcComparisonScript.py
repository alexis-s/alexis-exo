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
from ROOT import TPad
from ROOT import TLegend
from ROOT import TPaveText



def create_hist(name, title, min, max, n_bins, x_title):

    print "--> creating hist: name = %s, title = %s" % (name, title) 

    # options for hist binning, in keV:
    #binWidth = 14.0
    #n_bins = int((max - min)/binWidth)
    binWidth = (max - min)/n_bins
    print "\t min = %.2f | max = %.2f | binWidth = %.2f | n_bins = %.2f" % (min, max, binWidth, n_bins)
    #max = min + n_bins*binWidth
    #print "\t min = %.2f | max = %.2f | binWidth = %.2f | n_bins = %.2f" % (min, max, binWidth, n_bins)


    #print min, max, n_bins

    hist = TH1D(name, title, n_bins, min, max)
    hist.SetXTitle(x_title)
    hist.SetLineWidth(2)
    hist.Sumw2()

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
      "x_title": "Energy"
    }) 

    hist_info.append({
      "title": "PCD Sum energy", 
      "draw_string": "Sum$(fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy)*1e3", 
    }) 

    hist_info.append({
      "title": "PCD energy", 
      "draw_string": "fMonteCarloData.fPixelatedChargeDeposits.fTotalEnergy*1e3", 
      "max": 2000,
    }) 

    hist_info.append({
      "title": "CC Z Distribution", 
      "draw_string": "fChargeClusters.fZ",
      "min": -250,
      "max": 250,
      "n_bins": 200,
      "x_title": "z [mm]"
    }) 

    hist_info.append({
      "title": "PCD Z Distribution", 
      "draw_string": "fMonteCarloData.fPixelatedChargeDeposits.fCoordinateKey.fZ",
      "min": -1500,
      "max": 1500,
      "n_bins": 200,
      "x_title": "fCoordinateKey.fZ",
    }) 

    hist_info.append({
      "title": "Primary Event X", 
      "draw_string": "fMonteCarloData.fPrimaryEventX", 
      "min": -1500,
      "max": 1500,
      "n_bins": 200,
      "x_title": "x [mm]",
    }) 

    hist_info.append({
      "title": "Primary Event Y", 
      "draw_string": "fMonteCarloData.fPrimaryEventY", 
      "min": -1500,
      "max": 1500,
      "n_bins": 200,
      "x_title": "y [mm]",
    }) 

    hist_info.append({
      "title": "Primary Event Z", 
      "draw_string": "fMonteCarloData.fPrimaryEventZ", 
      "min": -1500,
      "max": 1500,
      "n_bins": 200,
      "x_title": "z [mm]",
    }) 

    hist_info.append({
      "title": "N Scint Clusters", 
      "draw_string": "@fScintClusters.size()", 
      "max": 20,
      "n_bins": 20,
      "x_title": "",
    }) 

    hist_info.append({
      "title": "N Charge Clusters", 
      "draw_string": "@fChargeClusters.size()", 
      "max": 20,
      "n_bins": 20,
      "x_title": "",
    }) 

    # FIXME -- selection isn't being used

    # loop over hist_lists, create empty hists with the specified info:
    for i, hist_dict in enumerate(hist_info):

        name = "hist%i_dir%s" % (i, suffix)
        hist_dict["name"] = name
        title = "%(title)s: %(draw_string)s" % hist_dict
        try: 
            min = hist_dict["min"] 
        except KeyError: 
            min = 0
        try: 
            max = hist_dict["max"] 
        except KeyError: 
            max = 3500
        try: 
            n_bins = hist_dict["n_bins"] 
        except KeyError: 
            n_bins = 250
        try: 
            x_title = hist_dict["x_title"] 
        except KeyError: 
            x_title = "Energy [keV]"

        hist = create_hist(name, title, min, max, n_bins, x_title)
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
            tree.GetEntry(0)
            svn_revision = tree.EventBranch.fEventHeader.fSVNRevision
            build_id = tree.EventBranch.fEventHeader.fBuildID
        except:
            print "BAD FILE"
            continue


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

        #if i_file >= 10: # debugging
        #    print "====> STOPPING AT FILE %s!" % i_file
        #    break 


    for hist_dict in hist_info:

        print "--> scaling %(name)s" % hist_dict
        hist = hist_dict["hist"]
        i_bin = 50
        #print "bin:", i_bin
        #print hist.GetBinContent(i_bin)
        #print hist.GetBinError(i_bin)
        #print hist.GetBinError(i_bin)/hist.GetBinContent(i_bin)*100.0
        hist.Scale(1.0/hist.GetEntries())
        #print hist.GetBinError(i_bin)/hist.GetBinContent(i_bin)*100.0
        hist_dict["n_entries"] = hist.GetEntries()

    return hist_info


def main(directory1, directory2):

    hist_info1 = process_directory(directory1, "1")
    hist_info2 = process_directory(directory2, "2")


    canvas = TCanvas("canvas", "")
    #canvas.Divide(1,2)
    canvas.cd(1)
    #canvas.SetTopMargin(0.2)
    canvas.SetLogy(1)


    for i in xrange(len(hist_info1)):


        hist_dict1 = hist_info1[i] 
        hist_dict2 = hist_info2[i] 

        hist1 = hist_dict1["hist"]
        hist2 = hist_dict2["hist"]

        print "====> hists %i of %i: %s" % (i+1, len(hist_info1), hist1.GetTitle())

        chi2_prob = hist1.Chi2Test(hist2, "WW P")
        ks_prob = hist1.KolmogorovTest(hist2)

        resid_hist = hist1.Clone("resid_hist")
        resid_hist.SetTitle("")
        resid_hist.Add(hist2, -1.0)
        #print resid_hist.GetYaxis().GetLabelSize()
        resid_hist.GetYaxis().SetLabelSize(0.10)
        resid_hist.GetYaxis().SetNdivisions(5)

        pad1 = TPad("pad1", "", 0.0, 0.25, 1.0, 1.0)
        pad1.Draw()

        pad2 = TPad("pad2", "", 0.0, 0.01, 1.0, 0.25)
        pad2.Draw()

        pad1.cd()
        pad1.SetGrid()
        pad1.SetTopMargin(0.2)
        pad1.SetLogy(1)
        hist1.Draw("hist")
        hist2.SetLineColor(2)
        hist2.Draw("hist same")

        legend = TLegend(0.1, 0.81, 0.9, 0.9)
        legend.SetFillColor(0)
        legend_entry = "%(build_id)s, %(n_entries).1e entries"
        legend.AddEntry(hist1, legend_entry % hist_dict1, "l")
        legend.AddEntry(hist2, legend_entry % hist_dict2, "l")
        legend.Draw()

        pave_text = TPaveText(0.85, 0.6, 1.0, 0.82, "NDC")
        pave_text.AddText("Chi2 Prob: %.2f" % chi2_prob)
        pave_text.AddText("KS Prob: %.2f" % ks_prob)
        pave_text.SetBorderSize(1)
        pave_text.Draw()
        pave_text.SetFillColor(0)

        pad2.cd()
        pad2.SetGrid()
        pad2.SetBottomMargin(0)
        resid_hist.Scale(100.0)
        resid_hist.Draw("p e")



        canvas.Update()
        canvas.Print("%s.pdf" % hist1.GetName())
        canvas.Clear()



if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "arguments: [directory of root files 1] [directory of root files 2]"
        sys.exit(1)


    main(sys.argv[1], sys.argv[2])
    #process_directory(sys.argv[1], "1")








