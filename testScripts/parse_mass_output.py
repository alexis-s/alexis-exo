#!/bin/env python

import os
import sys
import glob
import commands

"""
grab all of the log files from mass test runs

This script is used to collect log files for Mike Tarka's use. 
"""


def process_directory(directory, i_file=0):
    """
    Loop over directory contents, searching for logfiles
    """

    print "--> processing directory:" 
    #print "\t", directory

    # check if this directory contains logFile.txt:
    filename = ("%s/logFile.txt" % directory)
    if os.path.isfile(filename):
        process_file(filename, i_file)
        i_file += 1

    # otherwise, loop over subdirectories:
    else:
        items = glob.glob("%s/*" % directory)
        items.sort()
        for item in items:
            if os.path.isdir(item):
                i_file = process_directory(item, i_file)

    return i_file


def process_file(filename, i_file):

    #print "--> processing file %i:" % i_file 
    print "\t", filename
    #if i_file >= 10: sys.exit() # debugging

    # see if this file contains geometry dump info:
    search_string = 'Material = LXe'
    if not search_string in open(filename).read():
        print "NO GEOMETRY DUMP!!"
        return

    cmd = "cp %s logFile_%i.txt" % (filename, i_file)
    #print cmd
    output = commands.getstatusoutput(cmd)
    if output[0] != 0:
        print output[1]

    #print "\t ok"

directory  = \
"/nfs/slac/g/exo/exo_data/pipeline/logFiles/prod/EXOGenericMonteCarlo/1.7/SimulationStream/runMonteCarlo/001xxx/182/"
#"/nfs/slac/g/exo/exo_data/pipeline/logFiles/prod/EXOGenericMonteCarlo/1.7/SimulationStream/runMonteCarlo/001xxx/084/"
#"/nfs/slac/g/exo/exo_data/pipeline/logFiles/prod/EXOGenericMonteCarlo/1.7/SimulationStream/runMonteCarlo/001xxx/084/000/"

process_directory(directory)

