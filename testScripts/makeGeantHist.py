

"""
Make a hist of gammas emitted in decay
"""

import os
import sys


from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile


def make_hist(file_name):

    # options
    minE = -8.0 # to put a 14-keV bin boundary at 1 MeV
    maxE = 10000.0
    n_bins = int((maxE-minE)*100)

    print "--> processing", file_name

    ensdf_file = file(file_name)
    
    basename = os.path.basename(file_name)

    root_file = TFile(file_name)
    tree = root_file.Get("tree")
    n_entries = tree.GetEntries()
    print "%i entries in tree" % n_entries

    tree.GetEntry(n_entries-1)
    n_g4_events = tree.EventBranch.fEventHeader.fGeant4EventNumber+1
    svn_revision = tree.EventBranch.fEventHeader.fSVNRevision
    build_id = tree.EventBranch.fEventHeader.fBuildID
    print "%i decays" % n_g4_events
    print "build_id:", build_id
    print "svn_revision:", svn_revision


    # The TTree "tree" in a root file of MC output contains a TList of user info,
    # which has all of the talkto commands from the .exo file, among other
    # things
    #exoProcessingInfo = tree.GetUserInfo().At(0)
    #cmds = exoProcessingInfo.GetCommandsCalled()
    #for cmd in cmds:
    #    print cmd


    new_file = TFile("G4_svn_r%s_%s" % (svn_revision, basename), "recreate")
    hist = TH1D("gamma_hist", build_id, n_bins, 0.0, maxE)
    hist.SetXTitle("Energy [keV]")
    hist.SetYTitle("Intensity [%]")
    hist.Sumw2()

    hist.GetDirectory().cd()

    tree.Draw(
        "fKineticEnergykeV >> %s" % hist.GetName(),
        "fID==3", # EXO-200 offline gammas
        "goff"
    )
    hist_entries = hist.GetEntries()
    print "%i entries in hist" % hist_entries

    hist.Scale(100.0/n_g4_events)

    new_file.Write()




if __name__ == "__main__":


    if len(sys.argv) < 2:
        print "arguments: ENSDF decay data file"
        sys.exit(1)

    for file_name in sys.argv[1:]:
        make_hist(file_name)
