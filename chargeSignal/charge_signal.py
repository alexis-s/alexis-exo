#!/usr/bin/env python

"""
This script simulated the charge induced on an anode pad.
24 Feb 2014 AGS

Comparing to Liangjian's images.
LW used:
q = -10e5 (listed in his talk)
z_0 = 25cm (I thought he said 25mm?)
v_elec = 2.71 insead of 1.71

to do -- add ion drift?
"""

import math

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import TMath
from ROOT import TGraph
from ROOT import TCanvas
from ROOT import TColor


def get_induced_charge_per_area(q, z, rho=1.5):
    """
    Returns the charge per unit area induced on a conducting plane due to a
    point charge above the plane. 
    This is based on method of images:
    http://en.wikipedia.org/wiki/Method_of_image_charges#Reflection_in_a_conducting_plane
    where:
        q = charge
        z = perpendicular distance from conducting plane
        rho = distance along conducting plane, in cylindrical coords
    """

    # FIXME -- relative permittivity?

    pi = TMath.Pi()
    if z <= 0: return 0.0
    sigma = -q*z/(2*pi*pow(rho*rho + z*z, 3.0/2)) 
    return sigma

def get_rho(x, y):
    rho = math.sqrt(x*x + y*y)
    return rho

def get_charge_on_pad(q, z, x, y):
    area = 3.0*3.0/2            # area of one anode pad in mm
    rho = get_rho(x,y)
    charge = get_induced_charge_per_area(q, z, rho)*area
    return charge


def get_charge_on_x_string(q, z, y_index):
    """
    An x-string runs horizontally.
    y_index identifies the string.
    """
    if math.fabs(y_index) > 14: print "WARNING! There are only 28 strings"

    spacing = 3.0
    y = y_index * spacing
    

    # x_index identifies the pad. There are 29 pads: +0 to 14, -0 to -13
    charge = 0
    for x_index in xrange(15):
        x = 1.5 + x_index
        delta_charge = get_charge_on_pad(q, z, x, y)
        #print "x_index: %s, delta_charge: %.2f" % (x_index, delta_charge)
        charge += delta_charge
        if x_index <= 13:
            charge += delta_charge
            #print "x_index: %s, delta_charge: %.2f" % (x_index, delta_charge)
    #print 'total charge: %.2f' % charge
    return charge


def get_charge_on_y_string(q, z, x_index):
    return get_charge_on_x_string(q, z, x_index)


def make_plot():
    """
    Produces a PDF plot of q vs. time
    """
    
    # options
    q = -1e5                    # n electrons - same as LW
    v_elec = 1.71               # mm / microsecond # arxiv 1306.6106
    time_duration = 200         # microseconds
    delta_t = 0.1               # microseconds
    z_0 = 250                   # starting position in mm
    graph = TGraph()
    t = 0.0
    x = 1.5
    y = 0.0

    while t < time_duration:
        z = z_0 - v_elec*t
        #charge = get_charge_on_pad(q, z, x, y)
        charge = get_charge_on_x_string(q, z, y_index=0)
        #print 'time: %.2f | z: %.2f | charge: %.2f' % (t, z, charge)
        i_point = graph.GetN()
        graph.SetPoint(i_point, t, charge)
        t += delta_t


    graph.SetLineColor(TColor.kBlue+1)
    graph.SetTitle("q=%s;time [microseconds];charge [electrons]" % q)
    hist = graph.GetHistogram()
    hist.GetYaxis().SetTitleOffset(1.6)

    canvas = TCanvas("canvas", "")
    canvas.SetLeftMargin(0.15)
    canvas.SetGrid(True)

    graph.Draw()
    canvas.Update()
    canvas.Print('test_signal.pdf')


if __name__ == "__main__":

    make_plot()

    
