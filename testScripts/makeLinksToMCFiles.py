#!/bin/env python


import re
import os
import glob
import commands

# remove ansi escape characters, color formatting
ansi_escape = re.compile(r'\x1b[^m]*m')

scratch_dir = "/scratch/scratchdirs/alexis3/"

cmd = "ls -1 %s | grep hopque" % scratch_dir
output = commands.getstatusoutput(cmd)
directories = output[1].split('\n')
directories.sort()

print "%i directories found" % len(directories)

for (i, directory) in enumerate(directories):
    print "job %i of %i: %s" % (i, len(directories), directory)
    subdirectories = glob.glob("%s/%s/*" % (scratch_dir, directory))
    for subdirectory in subdirectories:
        #print "\t subdirectory:", subdirectory
        if os.path.isdir(subdirectory):
            #files = glob.glob("%s/*" % subdirectory)
            files = glob.glob("%s/*.root" % subdirectory)
            task = os.path.split(subdirectory)[-1]
            print "\t %s" % task
            cmd = "mkdir %s" % task
            output = commands.getstatusoutput(cmd)
            #print output[1]
            print "\t\t %i files" % len(files)
            n_output_exists = 0
            for i_file in files:
                #print i_file
                cmd = "ln -s %s %s/" % (i_file, task)
                output = commands.getstatusoutput(cmd)
                if output[0] != 0:
                    #print output[1]
                    n_output_exists += 1
            #print "\t%i links already existed" % n_output_exists
            print "\t\t %i links created" % (len(files) - n_output_exists)
    

