#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)

from ROOT import TFile

filenames = sys.argv[1:]

total_entries = 0
total_files = len(filenames)

for filename in filenames:

    print "--> processing:", filename

    root_file = TFile(filename)
    tree = TFile.Get("tree")
    n_entries = tree.GetNEntries()
    total_entries += n_entries

    print "\t %s entries" % n_entries


print "total files:", total_files
print "total entries:", total_entries


