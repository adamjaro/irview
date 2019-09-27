
import ROOT as rt
from ROOT import TVector2, TMath

from magnet import magnet
from beam import beam
from bpipe_el_rear import bpipe_el_rear
from photon_detector import photon_detector

from plot_2d import plot_2d

#_____________________________________________________________________________
class interaction_region:
    #Interaction Region
    #_____________________________________________________________________________
    def __init__(self):
        self.elements = {}

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate elements by angle theta

        for i in self.elements.itervalues():
            #select elements with rotation
            if not hasattr(i, "rotate"): continue
            #apply the rotation
            i.rotate(theta)

        #unify theta for rear electron magnets
        self.elements["B2ER"].THETA = self.elements["Q1ER"].THETA

    #_____________________________________________________________________________
    def add_photon_detector(self):
        self.elements["photon_detector"] = photon_detector()

    #_____________________________________________________________________________
    def add_bpipe_el_rear(self):
        #electron beampipe on the rear side
        self.elements["bpipe_el_rear"] = bpipe_el_rear()

    #_____________________________________________________________________________
    def add_beam(self, z_neg, z_pos, is_electron=True):
        #add beam representation, negative and positive extent along z
        name = "beam_electron"
        if is_electron == False: name = "beam_hadron"
        self.elements[name] = beam(z_neg, z_pos, is_electron)


    #_____________________________________________________________________________
    def load_magnets(self, nam, is_electron=True):
        #load magnets from input description

        #input loop
        for line in open(nam, "read"):
            line = line.lstrip()
            #comment
            if line.find("#") == 0:
                if line[1:].lstrip().find("name") == 0:
                    #get table format
                    ft = self.get_formtab(line[1:]) # 1: is to strip # character
                continue
            #set dictionary with magnet parameters
            lin = self.get_parameters(line, ft)
            #add the magnet to the elements
            self.elements[ lin["name"].upper() ] = magnet(lin, is_electron)

    #_____________________________________________________________________________
    def read_survey_hadron(self, nam):
        #read MAD-X survey file for hadron beam

        #for now the purpose is to get THETA, selecting
        #only items with _S

        #input hadron survey loop
        for line in open(nam, "read"):
            line = line.lstrip()
            #comment
            if line.find("##") == 0:
                if line[2:].lstrip().find("NAME") == 0:
                    #get table format
                    ft = self.get_formtab(line[2:]) # 1: is to strip # character
                continue
            #get values for the parameters
            lin = self.get_parameters(line, ft)
            #select only lines with _S
            if lin["NAME"].find("_S") < 0: continue
            #remove the trailing '_S'
            lin["NAME"] = lin["NAME"][ 0 : lin["NAME"].find("_S") ]
            #invert theta for hadron magnets
            theta_new = -1*float( lin["THETA"] )
            lin["THETA"] = "{0:.11f}".format(theta_new)
            #set survey values to the magnets
            if self.elements.get(lin["NAME"]):
                self.elements[ lin["NAME"] ].read_survey(lin)

    #_____________________________________________________________________________
    def read_survey_lepton(self, nam):
        #read MAD-X survey file for lepton beam

        #input survey loop
        for line in open(nam, "read"):
            line = line.lstrip()
            #comment
            if line.find("@") == 0 or line.find("$") == 0: continue
            #get table format in lepton survey
            if line.find("*") == 0:
                ft = self.get_formtab(line[1:])
                continue
            #get values for the parameters
            lin = self.get_parameters(line, ft)
            #remove '"' characters from the beginning and the end of the name
            lin["NAME"] = lin["NAME"][1:-1]
            #remove leading 'D' in the name if present
            if lin["NAME"].find("D") == 0:
                lin["NAME"] = lin["NAME"][1:]
            #set survey values to the magnets
            if self.elements.get(lin["NAME"]):
                self.elements[ lin["NAME"] ].read_survey(lin)

    #_____________________________________________________________________________
    def get_formtab(self, line):
        #magnets table formatting
        formtab = {}
        ll = line.split()
        for i in xrange(len(ll)):
            formtab[i] = ll[i]
        return formtab

    #_____________________________________________________________________________
    def get_parameters(self, line, ft):
        #set dictionary with magnet parameters
        #from input line according to table format ft
        lin = {}
        ll = line.split()
        for i in xrange(len(ll)):
            lin[ft[i]] = ll[i]
        return lin

    #_____________________________________________________________________________
    def draw_2d(self):

        p2d = plot_2d()
        p2d.draw(self.elements)

    #_____________________________________________________________________________
    def analysis(self):
        pass
        #general analysis

        #print angle of selected magnets
        #mag = self.elements["Q1ER"]
        #vec = TVector2(mag.center_z, mag.center_x)
        #print "theta:", TMath.Pi()-vec.Phi()

        #angle between magnets
        #m0 = self.elements["Q1ER"]
        #m1 = self.elements["Q1APR"]
        #v0 = TVector2(m0.center_z, m0.center_x)
        #v1 = TVector2(m1.center_z, m1.center_x)
        #print "dtheta:", v1.DeltaPhi(v0)

        #position of a magnet
        #m = self.elements["Q1ER"]
        #print m.center_z









































