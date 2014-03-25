#!/usr/bin/env python

"""
A script to backup my SU silver macbook to an external drive. 
07 Mar 2013 AGS

This takes ~20 minutes just to look over the files, even if no data is
transferred.
"""


import os
import sys
import datetime
import commands


print 'here we go!'


if __name__ == '__main__':


  #source_dir = '/Users/alexis/test'
  source_dir = '/'
  target_dir = '/Volumes/AGS_SU_Bkup/'


  if not os.path.isdir(target_dir):
    print 'oops, mount the drive.'
    sys.exit(1)

  date_info = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

  log_file = '/Users/alexis/.ags_backups/backup_%s.log' % date_info
  print 'log file:', log_file

  # get the full path to the exclude file
  exclude_file = os.path.realpath(__file__)
  exclude_file = os.path.dirname(exclude_file) + '/'
  exclude_file += 'rsync_excludes.txt'
  print 'exclude file:', exclude_file


  rsync_command = []
  rsync_command.append('time')
  rsync_command.append('rsync')
  #rsync_command.append('-n')           # dry run
  rsync_command.append('-avzh')                 
  rsync_command.append('--progress')
  rsync_command.append('--exclude-from=%s' % exclude_file)
  rsync_command.append('--delete-after')
  rsync_command.append('--delete-excluded') # good to use after changing rsync_excludes.txt

  rsync_command.append(source_dir)
  rsync_command.append(target_dir)

  rsync_command.append('>& %s' % log_file)


  rsync_command = ' '.join(rsync_command)
  print rsync_command

  output = commands.getstatusoutput(rsync_command)
  print output[1]

  print 'the end.'



