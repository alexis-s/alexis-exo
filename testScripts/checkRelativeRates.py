"""
no rate checking --- count events

arguments: [directories of root MC output]

"""

#!/usr/bin/env python

import os
import sys
import glob
import json
#import countMCResults

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TChain

directories = sys.argv[1:]


total_info = []

for subdirectory in directories:

    print "--> processing directory", subdirectory

    filenames = glob.glob("%s/*.root" % subdirectory)
    filenames = "%s/*.root" % subdirectory
    tree = TChain("tree")
    tree.Add(filenames)

    total_entries = tree.GetEntries()

    print subdirectory, total_entries

    total_info.append((subdirectory, total_entries))
    
# expect 5000000 events of ActiveLXe_Pb214_only
#scale_factor = 5000000 / total_info[0][1]

#scale_factor = 1000000 / total_info[0][1]
print "\n\nsummary of events:"

results_dict = {}

for (subdirectory, total_entries) in total_info:

    name = os.path.split(subdirectory)[-1]

    print "%s : %.1e" % (name, total_entries)
    results_dict[name] = total_entries

#print "scale_factor:", scale_facto

outputfile = open("mc_rates2.json", 'w')
json.dump(results_dict, outputfile, indent=4, sort_keys=True)
outputfile.close()

