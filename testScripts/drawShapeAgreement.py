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
    hist_ms_data.Draw()
    hist_ms_data.SetMaximum(300e3)
    hist_ms_mc.Draw("same hist")
    pad2.cd()
    hist_ms_ratio.Draw()
    canvas.Update()
    canvas.Print("%s_ms.png" % title)

    # draw ss stuff
    pad1.cd()
    hist_ss_data.Draw()
    hist_ss_data.SetMaximum(100e3)
    hist_ss_mc.Draw("same hist")
    pad2.cd()
    hist_ss_ratio.Draw()
    canvas.Update()
    canvas.Print("%s_ss.png" % title)



if __name__ == "__main__":

    file_names = sys.argv[1:]
    for file_name in file_names:
        process_file(file_name)
