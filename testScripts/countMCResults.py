#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)

from ROOT import TFile



def main(filenames):

    total_entries = 0
    total_files = len(filenames)

    for filename in filenames:

        print "--> processing:", filename

        root_file = TFile(filename)
        tree = root_file.Get("tree")

        try:
            #n_entries = tree.GetEntries()
            # haven't seen any issues yet...
            n_entries = tree.GetEntriesFast()
            print "\t n_entries %i (so far: %i)" % (n_entries, total_entries)
            total_entries += n_entries
        except AttributeError:
            print "\t BAD FILE!!"  
     


    print "total files:", total_files
    print "total entries: %.2e" % total_entries
    try:
        print "total | events / file:", total_entries/total_files
    except:
        pass
    return total_entries


if __name__ == "__main__":

    filenames = sys.argv[1:]
    main(filenames)

