#!/usr/bin/env python

"""
submit batch jobs at NERSC

arguments:
1: python script name 
2: filenames

26 Oct 2014 AGS
"""

import os
import sys

#options:
queue = "regular" 
hours = 1
minutes = 30
do_debug = True

if do_debug:
  queue = "debug" 
  hours = 0
  minutes = 10

python_script = sys.argv[1]
filenames = sys.argv[2:]

#print "\n".join(filenames)
#filenames.sort()
#print "\n".join(filenames)
#sys.exit()


print 'python_script:', python_script


for filename in filenames:
    print "--> processing:", python_script, filename

    basename = os.path.basename(filename)
    print "basename:", basename

    qsub_cmd = """
qsub \\
  -q %(queue)s \\
  -l walltime=%(hours)02i:%(minutes)02i:00 \\
  -N output_%(name)s \\
  -d %(cwd)s \\
  -V \\
""" % {
      "queue": queue,
      "hours": hours,
      "minutes": minutes,
      "name": basename,
      "cwd": os.getcwd(),
      }


    cmd = "printenv \n"
    cmd += "aprun -n 1 python ./%(python_script)s %(filename)s \n"  % {
      "python_script": python_script,
      "filename": filename,
    }
    cmd += "done"
    #script += "'printenv; aprun -n 1 python "+python_script+" "+filename+" '"

    print qsub_cmd
    print cmd

    write_handle = os.popen(qsub_cmd, 'w')
    write_handle.write(cmd)
    write_handle.close()

    if do_debug:
        print "==> debugging! only running first job!!"
        break



