
#central detector

import ROOT as rt

from detector import detector

#_____________________________________________________________________________
class detector_cen(object):
    #_____________________________________________________________________________
    def __init__(self, name, zpos, rmin, rmax, l, ang, ell, eln):
        #vmagnet.__init__(self)

        #upper part
        xup = rmin + (rmax-rmin)/2
        self.upper = detector(name+"_upper", zpos, xup, l, rmax-rmin, ang, ell, eln)
        self.upper.label = name+" #rightarrow"

        #lower part
        xdown = -rmin - (rmax-rmin)/2
        self.lower = detector(name+"_lower", zpos, xdown, l, rmax-rmin, ang, ell, eln)
        self.lower.label = "#leftarrow"
        self.lower.label_down = True

        ell[self.upper.name] = self.upper
        eln.append(self.upper.name)

        ell[self.lower.name] = self.lower
        eln.append(self.lower.name)

    #_____________________________________________________________________________
    def rotate(self, th):

        self.upper.rotate(th)
        self.lower.rotate(th)

    #_____________________________________________________________________________
    def print_pos(self):

        print self.name, "zpos:", self.center_z+self.length/2, "xpos:", self.center_x,
        print "theta:", self.THETA, "zcen:", self.center_z

