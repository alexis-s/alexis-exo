#!/usr/bin/env python

import os
import sys
import glob
import countMCResults

directories = sys.argv[1:]


total_info = []

for subdirectory in directories:

    print "--> processing directory", subdirectory

    filenames = glob.glob("%s/*.root" % subdirectory)

    total_entries = countMCResults.main(filenames)

    name = os.path.split(subdirectory)[-2]

    total_info.append((subdirectory, total_entries))
    
# expect 5000000 events of ActiveLXe_Pb214_only

scale_factor = 5000000 / total_info[0][1]

for (name, total_entries) in total_info:

    print "%s : %.1e" % (name, total_entries * scale_factor)


print scale_factor
