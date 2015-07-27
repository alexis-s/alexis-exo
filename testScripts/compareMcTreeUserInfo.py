"""
This script compares the talkto commands used to generate a root file. 
"""


import os
import sys
import commands

from ROOT import gROOT
gROOT.SetBatch(True)

from ROOT import TFile



def get_exo_file(filename):
    """ 
    reconstruct a .exo file from a provided root file
    """

    print "--> processing", filename

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]

    tfile = TFile(filename)
    tree = tfile.Get("tree")

    # The TTree "tree" in a root file of MC output contains a TList of user info,
    # which has all of the talkto commands from the .exo file, among other
    # things
    exoProcessingInfo = tree.GetUserInfo().At(0)
    cmds = exoProcessingInfo.GetCommandsCalled()

    outfilename = '%s.exo' % basename
    outfile = file(outfilename, 'w')

    do_print = False
    #print len(commands)
    for cmd in cmds:

        # print everything after "load"
        if "load" in cmd:
            do_print = True

        if do_print:
            outfile.write(cmd + '\n')

    outfile.close()
    return outfilename



if len(sys.argv) < 3:
    print "arguments [MC root file 1] [MC root file 2]"
    sys.exit(1)

filename1 = sys.argv[1]
filename2 = sys.argv[2]

exo_file1 = get_exo_file(filename1)
exo_file2 = get_exo_file(filename2)

cmd = "diff %s %s" % (exo_file1, exo_file2)
print cmd

out = commands.getstatusoutput(cmd)
print out[1]


