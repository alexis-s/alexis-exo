

"""

"""

import os
import sys


from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile


def make_hist(file_name):

    # options
    maxE = 10000.0 # 10 MeV
    n_bins = int(maxE*100)


    print "--> processing", file_name

    ensdf_file = file(file_name)
    
    basename = os.path.basename(file_name)

    root_file = TFile(file_name)
    tree = root_file.Get("tree")
    n_entries = tree.GetEntries()
    print "%i entries in tree" % n_entries

    tree.GetEntry(n_entries-1)
    n_g4_events = tree.EventBranch.fEventHeader.fGeant4EventNumber
    print "%i decays" % n_g4_events

    new_file = TFile("gammas_G4_%s.root" % basename, "recreate")
    hist = TH1D("gamma_hist","%s gammas" % basename, n_bins, 0.0, maxE)
    hist.SetXTitle("Energy [keV]")
    hist.SetXTitle("Intensity [%]")
    hist.Sumw2()

    hist.GetDirectory().cd()

    tree.Draw(
        "fKineticEnergykeV >> %s" % hist.GetName(),
        "fID==3", # EXO-200 offline gammas
        "goff"
    )
    hist_entries = hist.GetEntries()
    print "%i entries in hist" % hist_entries

    hist.Scale(1.0/n_g4_events)

    new_file.Write()




if __name__ == "__main__":


    if len(sys.argv) < 2:
        print "arguments: ENSDF decay data file"
        sys.exit(1)

    for file_name in sys.argv[1:]:
        make_hist(file_name)
