
import ROOT as rt
from ROOT import TVector2, TGraph

#_____________________________________________________________________________
class bpipe_el_rear(object):
    #beampipe for electrons, rear side
    #_____________________________________________________________________________
    def __init__(self):
        #input points
        self.pos = [(-16, -2), (-27, 45), (-31, 55), (-31, 65), (-27, 58)]
        self.pos += [(-26, 66), (-18.5, 32), (-16, 27)]
        #points in z and x, both in m
        self.zx_pos = []
        for i in self.pos:
            #self.zx_pos.append( {"z": i[0], "x": 0.01*i[1]} )
            # z at 0 and x at 1, converted to cm
            self.zx_pos.append( TVector2(i[0], 0.01*i[1]) )
        #angle of initial rotation, 17 mrad
        #self.theta_0 = -0.017
        self.rotate(-0.017)

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
            #self.geom.SetPoint(ipoint, i["z"], 100*i["x"])
            self.geom.SetPoint(ipoint, i.X(), 100*i.Y())
            ipoint += 1

        self.geom.Draw("lsame")

















