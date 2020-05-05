
from vmagnet import vmagnet

#_____________________________________________________________________________
class magnet_tab(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, lin, is_electron=True):
        vmagnet.__init__(self)
        #set magnet from line in description table
        self.name = lin[1]
        self.center_z = -float( lin[11] )
        self.center_x = float( lin[10] )
        self.length = float( lin[4] )
        self.rad1 = 0.07
        self.rad2 = 0.07
        self.field = float( lin[8] )
        #electron or hadron
        self.is_electron = is_electron
        #initial angle
        self.theta_0 = 0.
        #parameters from MAD-X survey
        self.S = 0.
        self.L = 0.
        self.X = 0.
        self.Z = 0.
        self.THETA = 0.01
        self.has_survey = True







