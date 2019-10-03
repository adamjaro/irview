
import ROOT as rt
from ROOT import TVector2, TGraph

#_____________________________________________________________________________
class bpipe_el_rear(object):
    #beampipe for electrons, rear side
    #_____________________________________________________________________________
    def __init__(self):
        #input points
        self.pos = [(-16, -14.8), (-18.5, -5), (-23, -5), (-23, 5), (-21.5, 5)]
        self.pos += [(-27, 23.4), (-31, 30.2), (-31, 40.2)]
        self.pos += [(-27, 36.4), (-26, 45.2), (-18.5, 17.2), (-16, 14.2)]
        #points in z and x, both in m
        self.zx_pos = []
        for i in self.pos:
            # z at 0 and x at 1, converted to cm
            self.zx_pos.append( TVector2(i[0], 0.01*i[1]) )
        #angle of initial rotation, 25 mrad
        self.rotate(-0.025)

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin
        for i in xrange(len(self.zx_pos)):
            self.zx_pos[i] = self.zx_pos[i].Rotate(theta)

    #_____________________________________________________________________________
    def draw_2d(self):
        #print type(self), self.zx_pos

        self.geom = TGraph(len(self.zx_pos))
        self.geom.SetLineColor(rt.kMagenta)
        self.geom.SetLineWidth(2)

        ipoint = 0
        for i in self.zx_pos:
            self.geom.SetPoint(ipoint, i.X(), 100*i.Y())
            ipoint += 1

        self.geom.Draw("lsame")

















