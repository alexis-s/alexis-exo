#!/bin/env python



import commands

# remove ansi escape characters, color formatting
ansi_escape = re.compile(r'\x1b[^m]*m')


cmd = "ls -1 /scratch/scratchdirs/alexis3/ | grep hopque"
output = commands.getstatusoutput(cmd)
directories = output[1].split('\n')

for directory in directories:
    print directory

