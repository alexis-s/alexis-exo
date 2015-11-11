#!/bin/env python


"""
A script for transferring files from NERSC to SLAC using rsync. 

First try for 3D digitizer work.

11 Nov 2015 AGS
"""

import re
import commands


# remove ansi escape characters, color formatting
ansi_escape = re.compile(r'\x1b[^m]*m')

# find list of subdirectories at NERSC:
cmd = "ssh alexis3@hopper.nersc.gov ls -1 /scratch/scratchdirs/alexis3/ | grep hopque"
output = commands.getstatusoutput(cmd)
index =  output[1].find("*")
lines = output[1].split('\n')

directory_list = []

for line in lines:
    index = line.find("hopque")
    if index > 0:
        line = ansi_escape.sub('', line)
        print line
        directory_list.append(line)

print "%i directories to transfer..." % len(directory_list)

for (i, directory) in enumerate(directory_list):

    print "processing directory %i: %s" % (i, directory)

    # dry run:
    #cmd = 'rsync -n --progress -rltDvzh -e ssh alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/%s/ .' % directory

    cmd = 'rsync --progress -rlDvzh -e ssh alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/%s/ .' % directory

    if i == 0:
        new_cmd = "%s >& test.out" % cmd
    else:
        new_cmd = "%s >> test.out 2>&1" % cmd
    print new_cmd
    output = commands.getstatusoutput(new_cmd)

    print "\n--> output:"
    print output[1]
    print "\n\n"



#time rsync --include='/1' --exclude='/*'--progress -rltDvzh -e 'ssh' alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/13565457.hopque01/ .
#time rsync --progress -rltDvzh -e 'ssh' alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/13565457.hopque01/ .

