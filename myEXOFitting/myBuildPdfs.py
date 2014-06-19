# This script is used to build PDFs (RooHistPdfs) from preprocessed MC trees.
# The directory that contains the preprocessed MC trees is specified as first
# argument.
# The file that contains the workspace to which the PDFs are saved is 
# specified as second argument.
# This stage fixes various parameters such as:
#   - The fiducial volume with which the PDFs are built
#   - The energy resolution with which the PDFs are built
#   - The beta scale with which the PDFs are built
#   - Which background components are used in the fit (!!!)

from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import sys
from optparse import OptionParser

def main(workspacefile,infile,outfile,Parameters):
  fitter = ROOT.EXOFitter()
  fitter.fUseBetaScale = True
  fitter.SetUseMCBasedFitEnergyCalibration(Parameters["useMCBasedFitCalibration"])
  fitter.LoadWorkspace(workspacefile)
  exoWorkspace = fitter.GetWorkspace()

  livetime = fitter.GetLivetime()

  wsp = ROOT.RooWorkspace("pdfWorkspace","pdfWorkspace")
  pdfInfo = fitter.FillPdfInfo(infile)

  #Get observables
  energy = exoWorkspace.var("energy")
  energy_ss = exoWorkspace.var("energy_ss")
  energy_ms = exoWorkspace.var("energy_ms")
  standoff = exoWorkspace.var("standoff_distance")
  mst_metric = exoWorkspace.var("u_cluster_mst_metric")

  pdfs_used = set( [
                   "bb0n",
                   ])

  if Parameters["extra_pdf"]:
    pdfs_used.add(Parameters["extra_pdf"])
 
  if Parameters["remove_pdf"]:
    pdfs_used.discard(Parameters["remove_pdf"])
 
  for pdf in pdfs_used:
    pdfInfo.find(pdf).SetUsedInFit(True)
    
  res = Parameters["res"]
  #Set resolution parameters if requested (otherwise use database values)
  if res:
    ROOT.EXOEnergyResCalib.SetUserValuesForRotated(*res)

  #Set resolution database flavor
  if Parameters["resFlavor"]:
    fitter.SetResolutionDatabaseFlavor(Parameters["resFlavor"])

  #Set beta scale
  fitter.fBetaScaleMCHistogram = Parameters["bscale"]
  betascale = ROOT.RooRealVar("betascale","betascale",fitter.fBetaScaleMCHistogram)

  #Create the low background PDF (this is the actual building function)
  print energy
  print standoff
  print mst_metric
  pdfs = fitter.GetLowBackgroundPdf(pdfInfo,
                                    livetime,
                                    ROOT.RooArgSet(),
                                    ROOT.RooArgSet(),
                                    ROOT.RooArgSet(
                                        energy,
                                        standoff,
                                        mst_metric
                                    ))
  getattr(wsp, 'import')(pdfInfo)
  getattr(wsp, 'import')(betascale)
  for i in range(2):   
    # [0] is SS pdf, [1] is MS pdf, [2] would be all sites (MST) pdf
    # for now do not save total pdf, because it crashes at
    # wsp.writeToFile(outfile)
    getattr(wsp, 'import')(pdfs[i])

  #Save the workspace
  wsp.writeToFile(outfile)

if __name__ == "__main__":
  usage = """
This script builds (the low background) PDFs (RooHistPdfs) from the 
preprocessed MC trees and saves the PDFs in a workspace.

usage: %prog [options] EXOWorkspaceFile.root pdfInfoFile.txt outputFile.root"""

  parser = OptionParser(usage)
  parser.add_option("-r","--resolution", dest="resolution",
                    help="set resolution parameters [default is database]",
                    metavar="P0_SS P1_SS P2_SS P0_MS P1_MS P2_MS", nargs=6)
  parser.add_option("--res-flavor",dest="resFlavor",
                    help="set energy resolution database flavor",
                    metavar="FLAVOR")
  parser.add_option("-s","--betascale", dest="betascale",
                    help="set beta scale parameter. [default = 1.004]", default=1.004,
                    metavar="BSCALE")
  parser.add_option("--hexcut", dest="hexcut",
                    help="set hexagonal cut parameters [default is database fiducial cut]",
                    metavar="APOTHEM ZMIN ZMAX", nargs=3)
  parser.add_option("--radcut", dest="radcut",
                    help="set radial cut parameters [default is database fiducial cut]",
                    metavar="RADIUS ZMIN ZMAX", nargs=3)
  parser.add_option("--extra-pdf",dest="extra_pdf", metavar="PDF",
                    help="include additional pdf PDF")
  parser.add_option("--remove-pdf",dest="remove_pdf", metavar="PDF",
                    help="remove pdf PDF")
  parser.add_option("--use-mcbasedfit-calibration",dest="useMCBasedFitCalibration",
                    help="use MC-based fit energy calibration",
                    action="store_true",default=False)
  options,args = parser.parse_args()
  if len(args) != 3:
    parser.print_help()
    sys.exit(1)

  ROOT.gSystem.Load("../lib/libEXOFitting")
  ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

  if options.hexcut and options.radcut:
    print("Error: Cannot use hexagonal AND radial cut")
    sys.exit(1)

  if options.hexcut:
    print("Using user provided hexagonal cut:")
    ROOT.EXOFiducialVolume().SetUserHexCut(float(options.hexcut[0]), float(options.hexcut[1]), float(options.hexcut[2]))
  elif options.radcut:
    print("Using user provided radial cut:")
    ROOT.EXOFiducialVolume().SetUserRadialCut(float(options.radcut[0]), float(options.radcut[1]), float(options.radcut[2]))
  else:
    print("Using database fiducial cut:")
  calib = ROOT.EXOCalibManager.GetCalibManager()
  fidvol = calib.getCalib("fiducial-volume","vanilla",ROOT.EXOTimestamp())
  print(fidvol)

  if options.resolution and options.resFlavor:
    print("Error: specifying user resolution and resolution database flavor does not make sense!")
    sys.exit(1)

  if options.resolution:
    res = map(float,options.resolution)
  else:
    res = None

  Parameters = {"bscale" : float(options.betascale),
                "res" : res,
                "extra_pdf" : options.extra_pdf,
                "remove_pdf": options.remove_pdf,
                "resFlavor" : options.resFlavor,
                "useMCBasedFitCalibration" : options.useMCBasedFitCalibration}
  print(Parameters)
  main(args[0],args[1],args[2],Parameters)

