#! /usr/bin/python 

"""
This is a wip for processing labview output.

A. Schubert 13 July 2013
"""

import sys

#from ROOT import gROOT
#gROOT.SetBatch(True)
#from ROOT import TH1D
#from ROOT import TFile
#from ROOT import TCanvas


def main(input_file_name):

    print '--> processing %s' % input_file_name

    try:
        input_file = file(input_file_name)    
    except IOError:
        print '--> file does not exist'
        return

    for line in input_file:
        #print line
        values = line.split()[2:]
        print values





if __name__ == '__main__':


    if len(sys.argv) < 2:
        print 'usage: [labview readout results file]'
        sys.exit(1)

    main(input_file_name=sys.argv[1])

