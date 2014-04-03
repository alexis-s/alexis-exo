#!/usr/bin/env python

"""
Flatten directories from NERSC output

02 Apr 2014 AGS
"""

import os
import sys
import glob
import commands


def process_directory(directory):
    print "--> processing directory:", directory

    # loop over each item in this directory, process as a file or directory
    items = glob.glob("%s/*" % directory)
    for item in items:

        if os.path.isdir(item):
            process_directory(item)

        else:
            process_file(item)

        #break # debugging


def process_file(filename):

    print "\t --> processing file:", filename


    # create the n-1th directory, if it doesn't exist yet:
    last_dir = os.path.dirname(filename)
    last_dir = os.path.split(last_dir)[-1]
    #print last_dir

    #cwd = os.getcwd()
    #print cwd

    # create the descriptive directory:
    if not os.path.exists(last_dir):
        cmd = "mkdir %s" % last_dir
        print cmd
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            print status
            print output
            sys.exit(1)


    # move the root file:
    cmd = "mv %s %s/" % (filename, last_dir)
    print cmd
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        print output
        sys.exit(1)





directories = sys.argv[1:]

for directory in directories:

    process_directory(directory)

    break # debugging



