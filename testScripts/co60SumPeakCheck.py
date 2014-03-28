#!/usr/bin/env python

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TH1D
from ROOT import TFile
from ROOT import TCanvas


filenames = sys.argv[1:]

hist = TH1D("hist", "", 4000, 0, 4000)

for index, filename in enumerate(filenames):
    print '--> processing file %i: %s' % (index, filename)

    root_file = TFile(filename)
    tree = root_file.Get('tree')
    hist.GetDirectory().cd()

    #n_entries = tree.Draw('Sum$(fChargeClusters.fRawEnergy)>>+ hist', '', '')
    n_entries = tree.Draw('fMonteCarloData.fTotalEnergyInLiquidXe>>+ hist', '', '')
    print '\t %s entries' % n_entries
    print hist.GetEntries()
    

    #if index > 0: break # debugging


canvas = TCanvas('canvas', '')
hist.Draw()
canvas.SetLogy(1)
canvas.Update()
canvas.Print("co60plot.pdf")

half_width = 10

cts_1173 = hist.Integral(1173 - half_width, 1173 + half_width)
cts_1332 = hist.Integral(1332 - half_width, 1332 + half_width)
cts_2505 = hist.Integral(2505 - half_width, 2505 + half_width)

print 'cts in 1173:', cts_1173
print 'cts in 1332:', cts_1332
print 'cts in 2505:', cts_2505

co60_results = TFile('co60_results.root', 'recreate')
hist.Write()

