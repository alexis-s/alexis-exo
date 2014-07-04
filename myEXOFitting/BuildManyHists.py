


import os
import sys
import Build1Hist

# loop over all input files, create a pre-processed file for each

filenames = sys.argv[1:]
for (index, filename) in enumerate(filenames):

    print "--> processing file %i of %i: %s" % (index+1, len(filenames), filename)
    dirname = os.path.dirname(filename)
    outputfile = "pre_" + os.path.basename(filename)
    if os.path.isfile(outputfile):
        print "\t\t SKIPPING! %s already exists" % outputfile
    else:
        Build1Hist.main(
            inputfiles=filename, 
            outputfile=outputfile, 
            outputdir=".", 
            scratch=False
        )
