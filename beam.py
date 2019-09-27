
import ROOT as rt
from ROOT import TVector2, TMath, TGraph

#_____________________________________________________________________________
class beam(object):
    #beam, represented as a straight line
    #_____________________________________________________________________________
    def __init__(self, z_neg, z_pos, is_electron=True):
        #negative and positive extent along z, rotated by the respective angle
        self.is_electron = is_electron

        angle = 0.
        if self.is_electron: angle = -0.025

        self.vec_neg = TVector2(z_neg, 0).Rotate(angle)
        self.vec_pos = TVector2(z_pos, 0).Rotate(angle)

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin

        self.vec_neg = self.vec_neg.Rotate(theta)
        self.vec_pos = self.vec_pos.Rotate(theta)

    #_____________________________________________________________________________
    def draw_2d(self):

        self.gbeam = TGraph(2)
        col = rt.kRed
        if self.is_electron: col = rt.kBlue
        self.gbeam.SetLineColor(col)

        self.gbeam.SetPoint(0, self.vec_neg.Px(), self.vec_neg.Py()*100)
        self.gbeam.SetPoint(1, self.vec_pos.Px(), self.vec_pos.Py()*100)

        self.gbeam.Draw("lsame")


