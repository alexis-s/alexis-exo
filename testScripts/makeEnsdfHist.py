

"""
ENSDF data:
http://www.nndc.bnl.gov/ensdf/

ENSDF format manual:
http://www.nndc.bnl.gov/nndcscr/documents/ensdf/ensdf-manual.pdf

"""

import os
import sys


from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile


def make_hist(file_name):

    # options
    minE = -8.0 # to put a 14-keV bin boundary at 1 MeV
    maxE = 10000.0
    n_bins = int((maxE-minE)*100)


    print "--> processing", file_name

    ensdf_file = file(file_name)
    
    basename = os.path.basename(file_name)

    root_file = TFile("%s.root" % basename, "recreate")
    hist = TH1D("gamma_hist","%s gammas" % basename, n_bins, 0.0, maxE)
    hist.SetXTitle("Energy [keV]")
    hist.SetYTitle("Intensity [%]")

    i_line = 0
    n_gammas = 0
    assigned = False
    # try to find gammas listed in the file
    search_string = "%s  G" % file_name
    #print search_string
    for line in ensdf_file:
        if i_line == 0:
            date = line[74:]
            print "release date:", date
        i_line += 1

        # try to find first instance of level record -- everything above this is
        # unnasigned
        if not assigned:
            result = line.find("%s  L" % file_name)
            if result == 0:
                assigned = True
            continue

        # try to find gammas listed in the file
        result = line.find("%s  G" % file_name)
        #print i_line, result
        #print line
        if result > -1: # result is -1 if found, should be 0 otherwise
            #print line
            #print result

            # grab the data:
            try:
                line_energy = float(line[9:18])
                intensity = float(line[21:28])
                comment_flag = line[76]
            except:
                print "ERROR PROCESSING LINE %s" % i_line
                print line
                continue

            #if comment_flag == '&': # multiply placed gamma, intensity not divided
            #    print line
            print "\t gamma: %s keV, %s" % (line_energy, intensity), "%"

            # add this info to the hist
            i_bin = hist.FindBin(line_energy)
            content = hist.GetBinContent(i_bin)
            if content > 0:
                print "\t\t already content in bin %i, energy %.3f: %s" % (
                    i_bin, 
                    hist.GetBinCenter(i_bin),
                    content,
                )
                print line
                print "comment_flag:", comment_flag
                if comment_flag == '@':
                    print "\t\t --> intensity is suitably divided"
                if comment_flag == '&':
                    if intensity != content:
                        print "\t\t WARNING: intensity != content"
                    print "\t\t --> skipping"

            hist.SetBinContent(i_bin, intensity + content)
            if content > 0:
                print "\t\t new content: %s" % (intensity + content)

            n_gammas += 1

        #if i_line > 200: break # debugging

        # end loop over file

    print "%i gammas found" % n_gammas

    hist.SetTitle("%s %s" % (basename, date))
    root_file.Write()




if __name__ == "__main__":


    if len(sys.argv) < 2:
        print "arguments: ENSDF decay data file"
        sys.exit(1)

    for file_name in sys.argv[1:]:
        make_hist(file_name)
