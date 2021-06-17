
import ROOT as rt

from vmagnet import vmagnet

#_____________________________________________________________________________
class exit_window(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, name, zpos, xpos, l, dx, ang):
        vmagnet.__init__(self)

        self.name = name
        self.center_z = zpos
        self.center_x = xpos
        self.length = l
        self.rad1 = dx/2
        self.rad2 = dx/2
        self.THETA = ang

        self.has_survey = True
        self.line_col = rt.kRed
        self.fill_col = rt.kYellow+1















