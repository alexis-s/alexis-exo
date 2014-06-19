#!/bin/sh
# This script builds workspaces with PDFs with default parameters for the current
# analysis and should be kept up to date with whatever the current analysis is.
# This also serves as a documentation of how the files were built.

# Beta scale values are taken from here:
# https://confluence.slac.stanford.edu/download/attachments/158047120/BetaScale_denoised_2014Jan19.pdf?version=1&modificationDate=1390200185000&api=v2

python myBuildPdfs.py --res-flavor=2014-v1 --betascale=0.9946 --hexcut=162 10 182 ../analysis/EXO_Workspace_Run2abc.root myPdfInfo.txt myPDFs.root
#python myBuildPdfs.py --res-flavor=2014-v1 --betascale=0.0 --hexcut=162 10 182 ../analysis/EXO_Workspace_Run2abc.root myPdfInfo.txt myPDFs_tinyBS.root

