
import ROOT as rt
from ROOT import TVector2, TGraph, TText

#_____________________________________________________________________________
class photon_detector(object):
    #_____________________________________________________________________________
    def __init__(self):
        #length, height and distance of the front side from the origin, all in m
        self.length = 8.
        self.height = 0.15
        self.dist = 23.2
        self.angle = -0.025 # rotation to be on electron beam axis

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin
        self.angle += theta

    #_____________________________________________________________________________
    def draw_2d(self):

        #make corner points
        vec = []
        vec.append( TVector2(self.length/2, -self.height/2) )
        vec.append( TVector2(-self.length/2, -self.height/2) )
        vec.append( TVector2(-self.length/2, self.height/2) )
        vec.append( TVector2(self.length/2, self.height/2) )

        #rotate and translate along electron beam
        vtrans = TVector2(-1, 0).Rotate(self.angle)
        vtrans.SetMagPhi(self.dist+self.length/2, vtrans.Phi())
        for i in xrange(len(vec)):
            vec[i] = vec[i].Rotate(self.angle)
            vec[i] += vtrans

        #last point same as the first
        vec.append( vec[0] )

        self.geom = TGraph(len(vec))
        self.geom.SetLineWidth(2)
        self.geom.SetLineColor(rt.kYellow+1)
        self.geom.SetFillColor(rt.kYellow)
        for i in xrange(len(vec)):
            self.geom.SetPoint(i, vec[i].X(), vec[i].Y()*100)

        self.geom.Draw("lfsame")

        #label
        self.label = TText(vtrans.X(), (vtrans.Y()-self.height/2-0.11)*100-3, "Lumi detector")
        self.label.SetTextSize(0.03)
        #self.label.SetTextAngle(90)
        #self.label.SetTextAlign(32)
        self.label.SetTextAlign(23)
        self.label.Draw("same")






















