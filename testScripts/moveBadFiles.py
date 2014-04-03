#!/usr/bin/env python

"""
This script loops through directories; finds & removes bad root files
"""


import os
import sys
import glob
import commands

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile


def is_root_file_ok(filename):
    """
    check whether this is a valid file
    """

    print "--> processing file:", filename

    file_type = os.path.splitext(filename)[1]
    #print file_type
    if file_type == ".mac":
        return True


    size = os.path.getsize(filename)

    print "\t size:", size
    
    root_file = TFile(filename)
    tree = root_file.Get("tree")
    try:
        n_entries = tree.GetEntries()
        print "\t n_entries", n_entries
        return True
    except AttributeError:
        print "\t BAD FILE!!"  
        return False
    


def process_directory(
    directory,  # directory we're searching
    bad_file_dir,  # place to put bad files
):

    print "--> processing directory:", directory

    # loop over each item in this directory, process as a file or directory
    items = glob.glob("%s/*" % directory)
    for item in items:

        if os.path.isdir(item):
            process_directory(item, bad_file_dir)

        else:
            test_result = is_root_file_ok(item)

            if not test_result:
                cmd = 'mv %s %s/' % (item, bad_file_dir)
                print cmd
                (status, output) = commands.getstatusoutput(cmd)
                print status
                print output

        #break # debugging


    

directories = sys.argv[1:]

bad_file_dir = 'bad_files3'
cmd = "mkdir %s" % bad_file_dir
print cmd
(status, output) = commands.getstatusoutput(cmd)
print status
print output


for directory in directories:

    process_directory(directory, bad_file_dir)

    #break # debugging







