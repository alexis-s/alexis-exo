


"""

"""

import os
import sys
import math
from array import array


from ROOT import gROOT
#gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TColor
from ROOT import TPad
from ROOT import TGraphErrors
from ROOT import TLegend



def compare_files(ensdf_file_name, mc_file_name):

    # options
    do_chi2 = False # this TH1D test doesn't work for bins with 0 content
    color = TColor.kRed # MC color
    y_division = 0.5 # divide the canvas at y = y_division
    rebin_factor = 100 # hist starts with 0.01-keV bins
    do_debug = False # print debugging output
    minE = 1000.0
    #maxE = 2000.0 # draw a subset of the full energy: 228-Ac
    maxE = 3000.0 # draw a subset of the full energy: 208-Tl


    # grab and set up ENSDF hist:
    print "--> processing ENSDF file", ensdf_file_name
    ensdf_basename = os.path.splitext(os.path.basename(ensdf_file_name))[0]
    print ensdf_basename
    ensdf_file = TFile(ensdf_file_name)
    ensdf_hist = ensdf_file.Get("gamma_hist")
    for i_bin in xrange(ensdf_hist.GetNbinsX()+1):
        ensdf_hist.SetBinError(i_bin, 0.0)
    if rebin_factor > 1.0:
        ensdf_hist.Rebin(rebin_factor)
    ensdf_hist.SetAxisRange(minE,maxE)
    ensdf_hist.SetMarkerStyle(24)
    ensdf_hist.SetMarkerSize(0.5)
    print "%i ENSDF gamma entries" % ensdf_hist.GetEntries()
    print "\t %i hist bins | bin width = %.3f" % ( ensdf_hist.GetNbinsX(),
        ensdf_hist.GetBinWidth(1) )

    # grab and set up MC hist:
    mc_file = TFile(mc_file_name)
    mc_hist = mc_file.Get("gamma_hist")
    mc_basename = os.path.splitext(os.path.basename(mc_file_name))[0]
    print mc_basename
    mc_hist.SetLineColor(color)
    mc_hist.SetMarkerColor(color)
    mc_hist.SetMarkerStyle(26)
    mc_hist.SetMarkerSize(0.5)
    mc_hist.SetAxisRange(minE,maxE)
    if rebin_factor > 1.0:
        mc_hist.Rebin(rebin_factor)
    print "%i MC gamma entries" % mc_hist.GetEntries()


    # use ROOT's chi^2 test -- doesn't work if zero error on ENSDF
    if do_chi2:

        initial_residuals = [0.]*(ensdf_hist.GetNbinsX()+2)
        residuals = array("d", initial_residuals)

        residuals = array("d", initial_residuals)
        # use arrays of length one here to get an address
        chi2 = array("d", [0.0])
        ndf = array("i", [0])
        igood = array("i", [0])

        chi2_prob = ensdf_hist.Chi2TestX(mc_hist, chi2, ndf, igood, "WW P", residuals)
        #chi2_prob = mc_hist.Chi2TestX(ensdf_hist, chi2, ndf, igood, "WW P", residuals)
        print "p-val:", chi2_prob
        print "chi2:", chi2[0]
        print "ndf:", ndf[0]
        print "igood:", igood[0]
        for i, val in enumerate(residuals):
            if val != 0:
                print i, val


    # fill resid_hist with ensdf_hist - mc_hist
    #resid_hist = ensdf_hist.Clone("resid_hist")
    #resid_hist.Add(mc_hist, -1.0)
    resid_hist = mc_hist.Clone("resid_hist")
    resid_hist.Add(ensdf_hist, -1.0)
    resid_hist.SetAxisRange(minE,maxE)
    resid_hist.SetLineColor(TColor.kBlack)
    resid_hist.SetMarkerColor(TColor.kBlack)
    resid_hist.SetTitle("")
    #resid_hist.SetYTitle("residual [#sigma] ")
    resid_hist.SetYTitle("MC - ENSDF [%]")
    resid_hist.GetYaxis().CenterTitle()
    #resid_hist.GetYaxis().SetLabelSize(0.1)
    #resid_hist.GetYaxis().SetTitleSize(0.1)
    resid_hist.GetYaxis().SetNdivisions(5)
    resid_hist.SetMarkerStyle(8)
    resid_hist.SetMarkerSize(0.0)
    #resid_hist2 = resid_hist.Clone("resid_hist2")
    resid_hist2 = TH1D("resid_hist2", "",
        resid_hist.GetNbinsX(),
        resid_hist.GetBinLowEdge(1),
        resid_hist.GetBinLowEdge(resid_hist.GetNbinsX())+resid_hist.GetBinWidth(1)
    )
    #print resid_hist.GetNbinsX()
    #print resid_hist.GetBinLowEdge(1)
    #print resid_hist.GetBinLowEdge(resid_hist.GetNbinsX())+resid_hist.GetBinWidth(1)
    resid_hist2.SetLineColor(color)
    resid_hist2.SetMarkerColor(color)
    resid_hist2.SetMarkerStyle(8)
    resid_hist2.SetMarkerSize(0.5)

    resid_graph = TGraphErrors()

    # divide each bin in resid_hist by the error
    # this makes resid_hist (hist2 - hist1)/error
    for i_bin in xrange(resid_hist.GetNbinsX()+1):

        resid_hist2.SetBinContent(i_bin, 0.0)
        resid_hist2.SetBinError(i_bin, 0.0)

        if ensdf_hist.GetBinCenter(i_bin) < minE: continue 
        if ensdf_hist.GetBinCenter(i_bin) > maxE: 
            print "--> skipping rest of events > %.2f keV" % maxE
            break

        difference = resid_hist.GetBinContent(i_bin)
        #error = resid_hist.GetBinError(i_bin)
        error = mc_hist.GetBinError(i_bin)
        value = ensdf_hist.GetBinContent(i_bin)
        if ensdf_hist.GetBinContent(i_bin) == 0 and mc_hist.GetBinContent(i_bin) == 0:
            continue # skip bins with zero content

        try:
            residual = difference / error # 03 Sept 2015, using units of sigma
        except ZeroDivisionError:
            residual = 0.0

        # set bin content & error based on statistical error:
        #resid_hist.SetBinContent(i_bin, residual)
        #resid_hist.SetBinError(i_bin, 0.0)

        resid_hist.SetBinContent(i_bin, difference)
        resid_hist.SetBinError(i_bin, error)

        # replace resid_hist values with actual residuals calculated from chi^2
        if do_chi2:
            resid_hist2.SetBinContent(i_bin, residuals[i_bin-resid_hist.FindBin(minE)])
        
        n_points = resid_graph.GetN()
        resid_graph.SetPoint(n_points, ensdf_hist.GetBinCenter(i_bin), difference)
        resid_graph.SetPointError(n_points, 0.0, error)

        # some verbose output:
        if math.fabs(residual) > 3.0 or do_debug:
            #print "bin: %i | E: %.2f | ENSDF: %.3f +/- %.1e| MC: %.4f +/- %.4f | diff: %.4f | err: %.4f | resid: %.4f | resid2: %.4f" % (
            print "bin: %i | E: %.2f | ENSDF: %.3f +/- %.1e| MC: %.4f +/- %.4f | diff: %.4f | err: %.4f | resid: %.4f " % (
                i_bin, 
                ensdf_hist.GetBinCenter(i_bin),
                ensdf_hist.GetBinContent(i_bin),
                ensdf_hist.GetBinError(i_bin),
                mc_hist.GetBinContent(i_bin),
                mc_hist.GetBinError(i_bin),
                difference,
                error,
                resid_hist.GetBinContent(i_bin),
                #resid_hist2.GetBinContent(i_bin),
            )

        # end loop over bins



    # set up canvas:
    canvas = TCanvas("canvas","")

    # create a large main pad for comparing the two; lower small pad for
    # residuals
    pad1 = TPad("pad1", "", 0.0, y_division, 1.0, 1.0)
    pad1.Draw()
    pad2 = TPad("pad2", "", 0.0, 0.05, 1.0, y_division)
    pad2.Draw()

    legend = TLegend(0.1, 0.85, 0.9, 0.99)
    #legend.SetNColumns(2)
    legend.AddEntry(mc_hist, mc_hist.GetTitle(), "pl")
    legend.AddEntry(ensdf_hist, "ENSDF %s" % ensdf_hist.GetTitle(), "p")

    pad1.cd()
    pad1.SetGrid()
    pad1.SetTopMargin(0.2)
    pad1.SetLogy(1)
    #ensdf_hist.SetTitle(mc_hist.GetTitle())
    ensdf_hist.SetTitle("")
    ensdf_hist.Draw("p")
    mc_hist.Draw("pe same")
    legend.Draw()

    pad2.cd()
    pad2.SetGrid()
    #pad2.SetBottomMargin(0) # hide resid hist x axis labels
    resid_hist.Draw("p")
    #resid_hist2.Draw("p same")
    #resid_hist2.Draw("p")
    #resid_graph.SetMarkerColor(TColor.kBlue)
    #resid_graph.SetMarkerStyle(26)
    resid_graph.SetMarkerStyle(8)
    resid_graph.SetMarkerSize(0.6)
    resid_graph.Draw("p")


    canvas.Update()
    if not gROOT.IsBatch():
        raw_input("any key to continue... ")

    plot_name = "%s_%s_%i_keV_bins" % (ensdf_basename, mc_basename, mc_hist.GetBinWidth(1))
    canvas.Print("%s.pdf" % plot_name)

    pad1.SetLogy(0)
    canvas.Update()
    canvas.Print("%s_lin.pdf" % plot_name)



if __name__ == "__main__":


    if len(sys.argv) < 3:
        print "arguments: [ENSDF decay data file] [EXO offline MC root file]"
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
