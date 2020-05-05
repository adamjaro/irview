
import math

import ROOT as rt
from ROOT import TVector2, TGraph, TText

#_____________________________________________________________________________
class exit_window(object):
    #photon exit window, part of electron beam pipe, rear side
    #_____________________________________________________________________________
    def __init__(self, geom):

        #input points, in electron beamline frame
        if geom == "flat":
            self.pos = [(-21.7, -5), (-21.7, 5)] # flat geometry
        if geom == "tilt":
            self.pos = [(-18.8, -5), (-21.7, 5)] # tilted geometry

        #print the geometry
        self.print_position()

        #points in z and x, both in m
        self.zx_pos = []
        for i in self.pos:
            # z at 0 and x at 1, converted to cm
            self.zx_pos.append( TVector2(i[0], 0.01*i[1]) )

        #angle of initial rotation
        self.rotate(-0.008)

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin
        for i in xrange(len(self.zx_pos)):
            self.zx_pos[i] = self.zx_pos[i].Rotate(theta)

    #_____________________________________________________________________________
    def draw_2d(self):

        #draw the exit window

        self.geom = TGraph(len(self.zx_pos))
        self.geom.SetLineColor(rt.kGreen+1)
        self.geom.SetLineWidth(4)

        ipoint = 0
        for i in self.zx_pos:
            self.geom.SetPoint(ipoint, i.X(), 100*i.Y())
            ipoint += 1

        self.geom.Draw("lsame")

        #label

        zpos = (self.zx_pos[0].X() + self.zx_pos[1].X())/2.
        self.label = TText(zpos, (self.zx_pos[0].Y())*100-6, "Exit window")
        self.label.SetTextSize(0.03)
        #self.label.SetTextAngle(90)
        #self.label.SetTextAlign(32)
        self.label.SetTextAlign(23)
        #self.label.Draw("same")

    #_____________________________________________________________________________
    def print_position(self):

        #show position and angle of the exit window
        z1 = self.pos[0][0]*1e3 # to mm
        z2 = self.pos[1][0]*1e3

        x1 = self.pos[0][1]*10. # to mm
        x2 = self.pos[1][1]*10.
        print "z_mid:", (z1 + z2)/2., "mm"
        print "x_mid:", (x1 + x2)/2., "mm"

        #length in x-z plane
        dl = math.sqrt((z1-z2)**2 + (x1-x2)**2)
        print "len:", dl, "mm"

        #angle in x-z plane
        dz = abs(z2-z1)
        dx = abs(x2-x1)
        #theta = math.atan( dx/dz )
        theta = math.asin( dx/dl )
        print "dz:", dz, "mm"
        print "dx:", dx, "mm"
        print "theta:", theta, "rad"
        print "pi/2 - theta:", math.pi/2. - theta, "rad"













