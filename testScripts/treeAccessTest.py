#!/usr/bin/env python

"""
testing random access of TTree, to debug issue during struck data building for
charge-readout test stand. 
"""


import sys
import time
import math

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TRandom3


def process_file(filename):
    
    print "---> processing file: ", filename


    # open the root file and grab the tree
    root_file = TFile(filename)
    tree = root_file.Get("tree")
    n_entries = tree.GetEntries()
    print "%i entries" % n_entries

    generator = TRandom3(0)

    rand_vals = []
    for i in xrange(n_entries):
        val = int(math.floor(generator.Rndm() * n_entries))
        rand_vals.append(val)


    reporting_period = 100 
    start_time = time.clock()
    now = start_time


    entries_of_timestamp = {} # a dictionary mapping timestamps to lists of tree entries




    for i_entry in xrange(n_entries):
        
        if i_entry % reporting_period == 0:
            last_time = now
            now = time.clock()
            print "==> event %i of %i (%.2f percent, %i events in %.1f seconds, %.2f seconds elapsed)" % (
                i_entry,
                n_entries, 
                100.0*i_entry/n_entries,
                reporting_period,
                now - last_time,
                now - start_time,
            )

        # fill dict of timestamps -> entry numbers
        try:
            entries_of_timestamp[timestamp]
            #print "timestamp already exists!!"
        except KeyError:
            entries_of_timestamp[timestamp] = []
        entries_of_timestamp[timestamp].append(i_entry)
        if len(entries_of_timestamp[timestamp]) > 6:
            print "more than 6 entries with timestamp", timestamp





        i = rand_vals[i_entry]
        tree.GetEntry(i_entry)


    now = time.clock()
    print "sequential access: %i entries in %.1f seconds" % (n_entries, now - start_time)

    start_time = now

    for i_entry in xrange(n_entries):

        #print i_entry
        if i_entry % reporting_period == 0:

            last_time = now
            now = time.clock()
            print "==> event %i of %i (%.2f percent, %i events in %.1f seconds, %.2f seconds elapsed)" % (
                i_entry,
                n_entries, 
                100.0*i_entry/n_entries,
                reporting_period,
                now - last_time,
                now - start_time,
            )

        i = rand_vals[i_entry]
        tree.GetEntry(i)


    now = time.clock()
    print "random access: %i entries in %.1f seconds" % (n_entries, now - start_time)


    
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "arguments: [sis root files]"
        sys.exit(1)


    for filename in sys.argv[1:]:
        process_file(filename)










