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
from optparse import OptionParser

def process_files(python_script, filenames, nparallel):

    #options:
    queue = "regular" 
    hours = 1
    minutes = 30
    do_debug = False # debugging

    if do_debug:
        queue = "debug" 
        hours = 0
        minutes = 10

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
        #cmd += "aprun -n 1 python ./%(python_script)s %(filename)s \n"  % {
        cmd += "aprun -n 1 python %(python_script)s %(filename)s \n"  % {
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


if __name__ == "__main__":

    usage = "%prog [options] python_script files_to_process"
    parser = OptionParser(usage)

    parser.add_option("--nparallel",dest="nparallel",type="int",default=1,
        help="set number of jobs to submit at the same time [Default = 5]")
    options, args = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        parser.error("Wrong number of arguments!")

    python_script = args[0]
    filenames = args[1:]
    print 'python_script:', python_script

    process_files(python_script, filenames, options.nparallel)

    #print "\n".join(filenames)
    #filenames.sort()
    #print "\n".join(filenames)
    #sys.exit()



