
#magnet from csv

from math import sqrt

from vmagnet import vmagnet

#_____________________________________________________________________________
class magnet_csv(vmagnet):
    #_____________________________________________________________________________
    def __init__(self, inp):
        vmagnet.__init__(self)

        #set magnet from line in description table
        self.name = inp["name"]
        self.THETA = inp["roty(mrad)"]*1e-3 # to rad
        self.center_z = inp["z0(m)"] + (inp["z1(m)"]-inp["z0(m)"])/2.
        self.center_x = inp["x0(m)"] + (inp["x1(m)"]-inp["x0(m)"])/2.
        self.length = sqrt( (inp["z1(m)"]-inp["z0(m)"])**2 + (inp["x1(m)"]-inp["x0(m)"])**2 )

        self.rad1 = inp["d0(mm)"]*1e-3/2. # to m
        self.rad2 = inp["d1(mm)"]*1e-3/2. # to m

        self.field = inp["field(T_T/m)"]

        #electron or hadron
        self.is_electron = True
        #survey (legacy)
        self.has_survey = True







