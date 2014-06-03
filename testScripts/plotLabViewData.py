#!/usr/bin/env python

import os
import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TFile
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TColor
from ROOT import TH1D
from ROOT import TGraph

def process_file(filename):

    print "--> processing file:", filename

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]

    #sys.exit(1) # exit for debugging

    dat_file = file(filename)

    graphs = []
    graphs.append(TGraph())
    graphs.append(TGraph())

    colors = []
    colors.append(TColor.kBlue+1)
    colors.append(TColor.kRed+1)

    for (i_graph, graph) in enumerate(graphs):
        color = colors[i_graph]  
        graph.SetLineColor(color)
        graph.SetMarkerColor(color)
        graph.SetMarkerStyle(8)
        graph.SetMarkerSize(0.5)
        graph.SetLineWidth(2)


    t_offset = 2082844800 # LV uses seconds since 1904
    #t_offset = 0 # LV uses seconds since 1904

    t_offset = float(dat_file.readline().split()[0])


    # data structure:
    # col 0: time stamps, in seconds since 1904

    minimum = 300
    maximum = 0

    #print "%s lines in file" % len(dat_file.readlines())
    for line in dat_file:
        #print line
        values = line.split()
        #print values
        time_stamp = (float(values[0]) - t_offset)/3600.0
        #time_stamp = 1401769753
        #print time_stamp

        for (i_val, value) in enumerate(values[1:]):
            graph = graphs[i_val]
            i_point = graph.GetN()
            y = float(value) #- i_val*0.01
            if y < 296.0:
                #print i_val, value
            if y > 0.0:
                graph.SetPoint(i_point, time_stamp, y)
                if y > maximum: maximum = y
                if y < minimum: minimum = y

    canvas = TCanvas("canvas", "")
    canvas.SetGrid()
    canvas.SetLeftMargin(0.15)
    #canvas.SetTopMargin(0.2)
    #canvas.SetBottomMargin(0.2)


    #legend = TLegend(0.1, 0.81, 0.9, 0.9)
    #legend.SetFillColor(0)


    graphs[0].Draw("a")
    frame_hist = graphs[0].GetHistogram()
    frame_hist.SetMinimum(minimum-0.1)
    frame_hist.SetMaximum(maximum+0.1)
    frame_hist.GetXaxis().SetTitle("Time [hours]")
    frame_hist.GetYaxis().SetTitle("Temperature [K]")
    frame_hist.GetYaxis().SetTitleOffset(1.6)

    # http://root.cern.ch/root/HowtoTimeAxis.html
    #frame_hist.GetXaxis().SetTimeDisplay(1)
    #frame_hist.GetXaxis().SetNdivisions(3)
    #frame_hist.GetXaxis().SetTimeOffset(-7,"gmt");
    #frame_hist.GetXaxis().SetTimeFormat("%H:%M %m-%d");

    frame_hist.Draw()
    for graph in graphs:
        n_points = graph.GetN()
        print "%i points" % n_points
        if n_points > 0:
            graph.Draw("pl")

    #graphs[0].Draw("pl")
    graphs[1].Draw("pl")


    canvas.Update()
    canvas.Print("ts_plot_%s.pdf" % basename)

    #print "%s lines in file" % len(dat_file)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage: %s [.dat file name]" % sys.argv[0]
        sys.exit(1)

    for filename in sys.argv[1:]:
        process_file(filename)

