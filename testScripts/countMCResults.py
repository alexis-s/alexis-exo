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
    tree = root_file.Get("tree")

    try:
        n_entries = tree.GetEntries()
        print "\t n_entries", n_entries
        total_entries += n_entries
    except AttributeError:
        print "\t BAD FILE!!"  
 


print "total files:", total_files
print "total entries:", total_entries
print "events / file:", total_entries/total_files


