#!/usr/bin/env python

"""
A script to backup my SU silver macbook to an external drive. 
07 Mar 2013 AGS
"""


import os
import sys
import commands


print 'here we go!'


if __name__ == '__main__':


  #source_dir = '/Users/alexis/test'
  source_dir = '/'
  target_dir = '/Volumes/AGS_SU_Bkup/'

  log_file = '/Users/alexis/backup.log'

  if not os.path.isdir(target_dir):
    print 'oops, mount the drive.'
    sys.exit(1)


  rsync_command = []
  rsync_command.append('time')
  rsync_command.append('rsync')
  #rsync_command.append('-n')           # dry run
  rsync_command.append('-avzh')                 
  rsync_command.append('--progress')
  rsync_command.append('--exclude-from=rsync_excludes.txt')
  rsync_command.append('--delete-after')

  rsync_command.append(source_dir)
  rsync_command.append(target_dir)

  rsync_command.append('>& %s' % log_file)


  rsync_command = ' '.join(rsync_command)
  print rsync_command

  output = commands.getstatusoutput(rsync_command)
  print output[1]


  print 'the end.'



