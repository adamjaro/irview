
from vmagnet import vmagnet

#_____________________________________________________________________________
class magnet_tab_sl(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, lin, bp, theta):
        vmagnet.__init__(self)
        #set magnet from line in description table

        #table format
        ft = {"name":1, "l":4, "b":8}

        self.name = lin[ft["name"]]
        self.center_z = -bp.Y()
        self.center_x = bp.X()
        self.length = float( lin[ft["l"]] )
        self.rad1 = 0.07
        self.rad2 = 0.07
        self.field = float( lin[ft["b"]] )
        #electron or hadron
        self.is_electron = True
        #initial angle
        self.theta_0 = 0.
        #parameters from MAD-X survey
        self.S = 0.
        self.L = 0.
        self.X = 0.
        self.Z = 0.
        self.THETA = -theta
        self.has_survey = True







