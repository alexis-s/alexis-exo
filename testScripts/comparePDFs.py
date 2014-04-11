#!/usr/bin/env python

"""
Using this to compare old and new sets of PDFs.

10 Apr 2014 AGS
"""



import os
import sys
import glob



def get_list_from_filenames_in_dir(directory):

    print "\n\nlooking in %s" % directory

    filenames = glob.glob("%s/*.root" % directory)
    filenames.sort()

    names = set()

    for filename in filenames:
        #print filename

        info = os.path.basename(filename) 
        info = os.path.splitext(info)[0]
        print info

        names.add(info)   

    print "%i files found" % len(names)

    return names



pdfs1 = get_list_from_filenames_in_dir(sys.argv[1])
pdfs2 = get_list_from_filenames_in_dir(sys.argv[2])

date1 = sys.argv[1].split('/')[-2]
date2 = sys.argv[2].split('/')[-2]

print "\n\nin both %s and %s:" % (date1, date2)
result = list(pdfs1.intersection(pdfs2))
result.sort()
print "\n".join(result)


print "\n\nin %s but not %s:" % (date1, date2)
result = list(pdfs1.difference(pdfs2))
result.sort()
print "\n".join(result)


print "\n\nin %s but not %s:" % (date2, date1)
result = list(pdfs2.difference(pdfs1))
result.sort()
print "\n".join(result)

