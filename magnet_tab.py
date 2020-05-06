
from vmagnet import vmagnet

#_____________________________________________________________________________
class magnet_tab(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, lin):
        vmagnet.__init__(self)

        #table format
        ft = {"name":1, "l":4, "b":8, "angle":12}

        #set magnet from line in description table
        self.name = lin[ft["name"]]
        self.center_z = -float( lin[11] )
        self.center_x = float( lin[10] )
        self.length = float( lin[ft["l"]] )
        self.rad1 = 0.07
        self.rad2 = 0.07
        self.field = float( lin[ft["b"]] )
        #electron or hadron
        self.is_electron = True
        #initial angle
        self.THETA = float( lin[ft["angle"]] )
        self.has_survey = True







