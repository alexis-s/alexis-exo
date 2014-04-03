#!/usr/bin/env python


"""
For file transfer to SLAC, we stage tarballs in $EXOPROJDIR/MonteCarlo/, but we
have exceeded our quota there using transfer_and_tar.py. The script
transfer_and_tar.py operates on a directory, so it will be useful to have the
files that need to be xferred in their own directory...

Right now, do the following:

* If a tar file in $EXOPROJDIR/MonteCarlo/ exists and is bigger than 50GB, assume
  it is good. 
* If the file is good, delete the tarball, move the corresponding directory of
  root results from $SCRATCH to $SCRATCH/alreadyMovedToSLAC
* If the file is not good, delete the tarball, move the dir of root results to
  $SCRATCH/moveToSLAC

"""

import os
import sys
import commands

tarballs = sys.argv[1:]

# loop over all the tarballs
for tarball in tarballs:

  print '--> processing', tarball

  # calculate tarball size
  size = os.path.getsize(tarball)
  print "\t size", size

  # grab the original job # from the tarball name
  job_name = os.path.basename(tarball).split(".")[0]
  print "\t job name", job_name

  output_files = "%s.hopque01" % job_name

  dir = "moveToSLAC"

  # if the tarball is > 50GB, things are probably ok
  if size > 50e9:
    print "\t good!"

    dir = "alreadyMovedToSLAC"

  else:
    print "\t fail!"


  # move the directory of files that were tar'd:
  cmd = "mv $SCRATCH/%s $SCRATCH/%s/output/" % (output_files, dir)
  print '\t', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status != 0:
      print output
      sys.exit(1)

  # move the tarball
  cmd = "mv %s $SCRATCH/%s/tar/" % (tarball, dir)
  print '\t', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status != 0:
      print output


