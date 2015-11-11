#!/usr/bin/env python

import commands

ssh_cmd = "ssh -Y -A alexis4@rhel6-64%s.slac.stanford.edu screen -ls"

nodes = ['a','b']

for i in xrange(12):
    
    node = chr(ord('a') + i)
    print node
    cmd = ssh_cmd % node
    #print cmd
    output = commands.getstatusoutput(cmd)
    #print output[1]
    result = output[1].find("There is")
    if result == 0:
        #print "%s: %i" % (node, result)
        print "\t", output[1]
        print "\t", cmd



