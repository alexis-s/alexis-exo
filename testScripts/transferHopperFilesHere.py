#!/bin/env python

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

for line in lines: # FIXME
    index = line.find("hopque")
    if index > 0:
        line = ansi_escape.sub('', line)
        print line
        directory_list.append(line)


directory_list.sort()

print "---------------------------------------"

for directory in directory_list[4:]:
    print directory

print "---------------------------------------"

print "%i directories to transfer..." % len(directory_list[4:])

for (i, directory) in enumerate(directory_list[4:]):

    print "processing directory %i: %s" % (i+1, directory)

    # dry run:
    #cmd = 'rsync -n --progress -rltDvzh -e ssh alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/%s/ .' % directory

    #cmd = 'rsync -n --progress -rlDvzh -e ssh alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/%s/ .' % directory
    cmd = 'rsync -n --exclude "*.out" --progress -rLDvzh -e ssh alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/MonteCarlo/svn10448_3d_digitizer/ .' 

    if i == 0:
        new_cmd = "%s >& test.out" % cmd
    else:
        new_cmd = "%s >> test.out 2>&1" % cmd
    print new_cmd
    output = commands.getstatusoutput(new_cmd)

    print "\n--> output:"
    print output[1]
    print "\n\n"
    break # debugging



#time rsync --include='/1' --exclude='/*'--progress -rltDvzh -e 'ssh' alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/13565457.hopque01/ .
#time rsync --progress -rltDvzh -e 'ssh' alexis3@hopper.nersc.gov:/scratch/scratchdirs/alexis3/13565457.hopque01/ .

