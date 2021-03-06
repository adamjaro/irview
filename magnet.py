
from vmagnet import vmagnet

#_____________________________________________________________________________
class magnet(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, lin, is_electron=True):
        vmagnet.__init__(self)
        #set magnet from configuration dictionary
        self.name = lin["name"]
        self.center_z = float( lin["center_z"] )
        self.center_x = float( lin["center_x"] )
        self.length = float( lin["length"] )
        self.rad1 = float( lin["rad1"] )
        self.rad2 = float( lin["rad2"] )
        self.field = float( lin["B"] )
        #electron or hadron
        self.is_electron = is_electron
        #initial angle
        self.theta_0 = 0.017
        #parameters from MAD-X survey
        self.S = 0.
        self.L = 0.
        self.X = 0.
        self.Z = 0.
        self.THETA = 0.
        self.has_survey = False







