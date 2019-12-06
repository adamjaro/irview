
import ROOT as rt
from ROOT import TVector2, TGraph

from exit_window import exit_window

#_____________________________________________________________________________
class bpipe_el_rear(object):
    #beampipe for electrons, rear side
    #_____________________________________________________________________________
    def __init__(self):

        #points representing the beam pipe
        self.zx_pos = []

        #points before exit window, crossed frame
        pos = [(-15.1, -2), (-16, -2)]
        self.add_points(pos)

        #attach photon exit window
        #geom = "flat"
        geom = "tilt"
        self.phot = exit_window(geom)

        #points connecting the exit window, in electron beamline frame
        ang = 0.008 # transform to electron beamline and back
        self.rotate(ang)
        pos = [(-18.8, -5)]
        if geom == "flat":
            pos += [(-21.7, -5)] # for flat exit window
        pos += [(-21.7, 5)]
        self.add_points(pos)
        self.rotate(-ang)

        #points after exit window, crossed frame
        pos = [(-27, 45), (-31, 55), (-31, 65)]
        pos += [(-27.5, 56), (-27, 68), (-18.5, 30), (-15.1, 26)]
        self.add_points(pos)

        #angle of initial rotation, 25 mrad
        self.rotate(-0.017)



    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin
        for i in xrange(len(self.zx_pos)):
            self.zx_pos[i] = self.zx_pos[i].Rotate(theta)
            pass

        #rotate the attached exit window
        self.phot.rotate(theta)

    #_____________________________________________________________________________
    def draw_2d(self):

        #draw the beam pipe

        self.geom = TGraph(len(self.zx_pos))
        self.geom.SetLineColor(rt.kMagenta)
        self.geom.SetLineWidth(2)

        ipoint = 0
        for i in self.zx_pos:
            self.geom.SetPoint(ipoint, i.X(), 100*i.Y())
            ipoint += 1

        self.geom.Draw("lsame")

        #put photon exit window
        self.phot.draw_2d()


    #_____________________________________________________________________________
    def add_points(self, p):

        for i in p:
            # z at 0 and x at 1, converted to cm
            self.zx_pos.append( TVector2(i[0], 0.01*i[1]) )














