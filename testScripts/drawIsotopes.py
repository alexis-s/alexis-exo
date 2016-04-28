from ROOT import gROOT

import os
import sys
import glob

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH2D
from ROOT import TFile
from ROOT import TCanvas
from ROOT import gSystem
from ROOT import gStyle


#gSystem.Load("$EXOLIB/lib/libEXOUtilities")
gROOT.SetStyle("Plain")     
gStyle.SetOptStat(0)        
gStyle.SetPalette(1)        
gStyle.SetTitleStyle(0)     
gStyle.SetTitleBorderSize(0)       


def process_directory(directory):


    # options:
    if False: # 238-U / 232-Th
        minA = 205
        maxA = 240
        minZ = 80
        maxZ = 94
    else:
        minA = 0
        maxA = 42
        minZ = 0
        maxZ = 20
    draw_string = "fAtomicNumber:fCharge"

    n_binsA = (maxA-minA)*2
    n_binsZ = (maxZ-minZ)*2

    hist = TH2D("hist","",
        n_binsZ, minZ, maxZ,
        n_binsA, minA, maxA,
    )
    hist.SetXTitle("Number of protons")
    hist.SetYTitle("Atomic number")


    root_filenames = glob.glob("%s/*.root" % directory)
    print "%i files" % len(root_filenames)
    n_total_events = 0
    n_total_g4_events = 0
    basename = os.path.commonprefix(root_filenames)
    basename = os.path.basename(basename)
    basename = basename.split("_") # split on underscores
    basename = "_".join(basename[:-1]) # remove stuff after last underscore
    print "basename:", basename

    for (i_file, root_filename) in enumerate(root_filenames):
        
        if (True):
            if n_total_events > 1e6:
                print "stopping at %i events!!" % n_total_events
                break

                break

        print "\t processing file %i of %i (%.2f percent): %s" % (
            i_file, 
            len(root_filenames),
            i_file*100.0/len(root_filenames),
            root_filename,
        )

        try:
            root_file = TFile(root_filename)
            tree = root_file.Get("tree")
            n_entries = tree.GetEntries()
            print "\t\t %i entries" % n_entries
            n_total_events += n_entries
            print "\t\t %i total entries" % n_total_events
            tree.GetEntry(n_entries-1)
            n_g4_events = tree.EventBranch.fEventHeader.fGeant4EventNumber
            n_total_g4_events += n_g4_events
            print "\t\t %i g4 events" % n_g4_events
            print "\t\t %i total g4 events" % n_total_g4_events
            tree.GetEntry(0)
            svn_revision = tree.EventBranch.fEventHeader.fSVNRevision
            build_id = tree.EventBranch.fEventHeader.fBuildID
        except:
            print "BAD FILE"
            continue


        if i_file == 0:
            prev_svn_revision = svn_revision
            print "\t\t", svn_revision, build_id
        if svn_revision != prev_svn_revision:
            print "SVN version changed!!"
            print "\t\t", svn_revision, build_id

        # add info to hist
        hist.GetDirectory().cd()
        n_entries = tree.Draw("%s >>+ %s" % (draw_string, hist.GetName()), "","goff")
        print "\t entries added"

        # end loop over root files

    print "%i entries in hist" % hist.GetEntries()

    canvas = TCanvas("canvas", "",500,500)
    canvas.SetLogz(1)
    canvas.SetGrid(1,1)
    margin = 0.13
    canvas.SetMargin(margin, margin, margin, margin)

    hist.GetYaxis().SetTitleOffset(1.5)
    hist.SetTitle(basename)
    hist.Scale(1.0/n_total_g4_events)
    hist.SetAxisRange(1e-3, 1.0, "z")
    hist.Draw("colz")

    canvas.Update()
    canvas.Print("isotopes_%s.pdf" % basename)
    


if __name__ == "__main__":


    if len(sys.argv) < 2:
        print "arguments: [directory of MC root files]"
        sys.exit(1)

    for directory in sys.argv[1:]:
        process_directory(directory)
