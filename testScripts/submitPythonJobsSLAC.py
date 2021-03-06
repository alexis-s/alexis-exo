#!/usr/bin/env python

"""
submit batch jobs at SLAC

arguments:
1: python script name 
2: filenames

if running as exodata, do this first:
source /afs/slac.stanford.edu/u/xo/alexis4/.cshrc

slac batch info:
https://www.slac.stanford.edu/exp/glast/wb/prod/pages/installingOfflineSW/usingSlacBatchFarm.htm

02 Apr 2014 AGS
"""

import os
import sys

#queue = "long" # <= 2 hours
queue = "xlong" # <= 16 hours
hours = 15
minutes = 00

python_script = sys.argv[1]
filenames = sys.argv[2:]

#print "\n".join(filenames)
#filenames.sort()
#print "\n".join(filenames)
#sys.exit()

wrap_python = "/nfs/slac/g/exo/software/applications/bin/wrap_python.sh"

print 'python_script:', python_script


for filename in filenames:
    print "--> processing:", filename

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    #print basename

    script = """
bsub \\
  -R rhel60 \\
  -q %(queue)s \\
  -W %(hours)02i:%(minutes)02i \\
  -o out_%(base)s.out \\
  -J %(base)s_py \\
   'printenv; python %(python_script)s %(filename)s'
""" % {
      "queue": queue,
      "hours": hours,
      "minutes": minutes,
      "base": basename,
      "python_script": python_script,
      "filename": filename,
    }

    print script

    write_handle = os.popen(script, 'w')
    write_handle.close()



