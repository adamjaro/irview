
import ROOT as rt

from vmagnet import vmagnet

#_____________________________________________________________________________
class detector(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, name, zpos, xpos, l, dx, ang, ell=None, eln=None):
        vmagnet.__init__(self)

        self.name = name
        self.center_z = zpos-l/2
        self.center_x = xpos
        self.length = l
        self.rad1 = dx/2
        self.rad2 = dx/2
        self.THETA = ang

        self.has_survey = True
        self.line_col = rt.kRed
        self.fill_col = rt.kYellow+1

        if ell is not None:
            ell[self.name] = self
            eln.append(self.name)

    #_____________________________________________________________________________
    def print_pos(self):

        print(self.name, "zpos:", self.center_z+self.length/2, "xpos:", self.center_x)
        print("theta:", self.THETA, "zcen:", self.center_z)

        print(" ".ljust(len(self.name)), "x_lo:", self.center_x-self.rad1)
        print("x_hi:", self.center_x+self.rad1)


