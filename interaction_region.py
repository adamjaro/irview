
from pandas import read_csv

import ROOT as rt
from ROOT import TVector2, TMath

from magnet import magnet
from beam import beam
from bpipe_el_rear import bpipe_el_rear
from photon_detector import photon_detector
from magnet_tab import magnet_tab
from magnet_tab_sl import magnet_tab_sl
from detector import detector
from detector_cen import detector_cen
from magnet_csv import magnet_csv

from plot_2d import plot_2d

#_____________________________________________________________________________
class interaction_region:
    #Interaction Region
    #_____________________________________________________________________________
    def __init__(self):
        self.elements = {}
        self.element_names = []

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate elements by angle theta

        for i in self.elements.itervalues():
            #select elements with rotation
            if not hasattr(i, "rotate"): continue
            #apply the rotation
            i.rotate(theta)

        #unify theta for rear electron magnets
        #self.elements["B2ER"].THETA = self.elements["Q1ER"].THETA

    #_____________________________________________________________________________
    def translateX(self, xt):

        #translate the elements along x

        for i in self.elements.itervalues():
            #select elements with translation
            if not hasattr(i, "translateX"): continue

            #apply the translation
            i.translateX(xt)

    #_____________________________________________________________________________
    def rotate_translateX(self, theta, xt):

        #combined rotatation and translation
        self.rotate(theta)
        self.translateX(xt)

    #_____________________________________________________________________________
    def add_element(self, el):

        self.elements[el.name] = el
        self.element_names.append(el.name)

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
            line = line.strip()

            #empty line
            if line == "": continue

            #comment
            if line.find("#") == 0:
                if line[1:].lstrip().find("name") == 0:
                    #get table format
                    ft = self.get_formtab(line[1:]) # 1: is to strip # character
                continue

            #set dictionary with magnet parameters
            lin = self.get_parameters(line, ft)

            #add center_z if start_z is provided
            if lin.get("start_z") is not None:
                lin["center_z"] = str( -float(lin["start_z"]) - float(lin["length"])/2 )

            #add the magnet to the elements
            nam = lin["name"].upper()
            mag = magnet(lin, is_electron)
            mag.THETA = float(lin["angle"])*1e-3
            mag.has_survey = True
            self.elements[ nam ] = mag
            self.element_names.append(nam)

        #move to default frame
        self.rotate(0.017)

        #ecal in central beam frame
        ecal = detector_cen("ECAL", -3.28, 0.1, 0.95, 0.2, 0, self.elements, self.element_names)
        ecal.rotate(-0.008)

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
    def draw_2d(self, zmin, xmin, zmax, xmax):

        p2d = plot_2d(zmin, xmin, zmax, xmax)
        p2d.draw(self.elements)

    #_____________________________________________________________________________
    def load_tab(self, nam, smax=999):

        #load electron magnets from description table

        #table format
        ft = {"name":1, "etype":2, "s":3}

        iel = 0 # element index for multiple instances of the same name

        for line in open(nam, "read"):

            ll = line.split()

            #comments and beginning line
            if ll[0][0] == "#" or ll[0][0] == "0": continue

            #max s position to load
            s = float(ll[ft["s"]])
            if smax<0 and -s < smax: break

            #magnets only
            name = ll[ft["name"]]
            etype = ll[ft["etype"]]
            if etype == "Marker": continue
            if etype == "Drift" and name.find("ECRAB")<0 and name.find("D3ER")<0:
                continue

            #more instances of the same name
            if self.elements.get(name) is not None:
                name = name + "_" + str(iel)
                iel += 1

            #add the magnet
            self.elements[name] = magnet_tab(ll)
            self.element_names.append(name)

        self.set_inner_radii()

        #electron tagger in central beam frame
        #tag = detector("lowQ2", -27, 0.472, 0.35, 0.1, 0.02, self.elements, self.element_names)
        #tag.rotate(-0.008)

        #two taggers in outgoing beam frame
        tag1 = detector("lowQ2_1", -24, 0.31, 0.35, 0.4, 0, self.elements, self.element_names)
        tag1.label = "Tagger 1"
        tag2 = detector("lowQ2_2", -37, 0.205, 0.35, 0.3, 0, self.elements, self.element_names)
        tag2.label = "Tagger 2"

        for itag in tag1, tag2: itag.rotate_translateX(-0.026332, -0.224548100304)

        #luminosity detector in central beam frame
        colim = detector("colim", -27, 0, 0.3, 0.3, 0, self.elements, self.element_names)
        colim.label = "Colimator"
        ew = detector("ew", -20.75, 0.06, 2.5, 0.13*2, 0.1, self.elements, self.element_names)
        ew.label = "Exit window"
        lumi_dipole = detector("lumi_dipole", -28, 0, 0.6, 0.1, 0, self.elements, self.element_names)
        lumi_dipole.label = "Spectrometer dipole"
        phot = detector("phot", -37, 0, 0.35, 0.2, 0, self.elements, self.element_names)
        phot.label = "Luminosity det"
        up = detector("up", -36.5, 0.1+0.042, 0.35, 0.2, 0, self.elements, self.element_names)
        up.no_label = True
        down = detector("down", -36.5, -0.1-0.042, 0.35, 0.2, 0, self.elements, self.element_names)
        down.no_label = True

        for ilumi in colim, ew, lumi_dipole, phot, up, down:
            ilumi.rotate(-0.008)
            ilumi.label_down = True

        #ecal in central beam frame
        ecal = detector_cen("ECAL", -3.28, 0.08, 0.62, 0.2, 0, self.elements, self.element_names)
        ecal.rotate(-0.008)

    #_____________________________________________________________________________
    def load_csv(self, nam):

        #electron magnets from a csv
        
        inp = read_csv(nam)

        for i, row in inp.iterrows():

            #add the magnet
            name = row["name"]
            self.elements[name] = magnet_csv(row)
            self.element_names.append(name)

    #_____________________________________________________________________________
    def set_inner_radii(self):

        #manual entry for inner radii
        self.elements["Q1ER"].rad1 = 0.066
        self.elements["Q1ER"].rad2 = 0.079
        self.elements["Q2ER"].rad1 = 0.083
        self.elements["Q2ER"].rad2 = 0.094

        B2 = self.elements["B2ER"]
        B2.rad1 = 0.097
        B2.rad2 = 0.139

        Q3 = self.elements["Q3ER"]
        Q3.rad1 = 0.040
        Q3.rad2 = 0.045

        D3 = self.elements["D3ER"]
        D3.rad1 = B2.rad2
        D3.rad2 = Q3.rad1
        D3.fill_style = 3207

    #_____________________________________________________________________________
    def load_tab_sl(self, nam, smax=999):

        #load electron magnets from description table with s and l of the elements

        #table formatting
        ft = {"s":3, "angle":7, "name":1, "etype":2, "l":4}
        #ft = {"s":5, "angle":7, "name":1, "etype":2, "l":6}

        #current position along electron beam
        bp = TVector2(0, 0); # x, z

        s0 = 0. # movement in s
        l0 = 0. # length of previous element
        theta = 0. # angle of individual elements

        iel = 0 # element index

        for line in open(nam, "read"):

            ll = line.split()

            #comments and beginning line
            if ll[0][0] == "#" or ll[0][0] == "0": continue

            #load the s position and element length
            s = float(ll[ft["s"]])

            if smax<0 and -s < smax: break

            delt = TVector2(0, s-s0-l0/2)
            delt = delt.Rotate(theta)
            s0 = s
 
            #move to the next element
            bp += delt;

            #add the element, magnets only
            name = ll[ft["name"]]
            etype = ll[ft["etype"]]

            if (etype != "Drift" and etype != "Marker") or name.find("ECRAB")>=0 or name.find("D3ER")>=0:
            #if True:

                #more instances of the same name
                if self.elements.get(name) is not None:
                    name = name + "_" + str(iel)
                    iel += 1

                self.elements[name] = magnet_tab_sl(ll, bp, theta)
                self.element_names.append(name)

                #print name, bp.X(), bp.Y()

            #move current position to the end of the current element
            l0 = float(ll[ft["l"]])
            delt = TVector2(0, l0/2)
            delt = delt.Rotate(theta)
            bp += delt;

            #angle for the next element
            theta += float(ll[ft["angle"]]) 

        self.set_inner_radii()

        #electron tagger
        detector("lowQ2", -27, 0.472, 0.35, 0.1, 0.02, self.elements, self.element_names)




    #_____________________________________________________________________________
    def analysis(self):
        pass
        #general analysis

        #Q3ER
        #m = self.elements["Q3ER"]
        #print "Q3ER", m.center_x, m.center_z

        #B2eR location and dimensions for low Q2 simulations
        #b2 = self.elements["B2ER"]
        #print "B2eR:"
        #print "x:", b2.center_x, "m"
        #print "z:", b2.center_z, "m"
        #print "length:", b2.length, "m"
        #print "rad1:", b2.rad1, "m"
        #print "rad2:", b2.rad2, "m"
        #print "field:", b2.field, "T"

        #print angle of selected magnets
        mag = self.elements["Q1ER"]
        vec = TVector2(mag.center_z, mag.center_x)
        print("theta:", TMath.Pi()-vec.Phi())

        #angle between magnets
        #m0 = self.elements["Q1ER"]
        #m1 = self.elements["Q1APR"]
        #v0 = TVector2(m0.center_z, m0.center_x)
        #v1 = TVector2(m1.center_z, m1.center_x)
        #print "dtheta:", v1.DeltaPhi(v0)

        #position of a magnet
        #m = self.elements["Q1ER"]
        #print m.center_z

    #_____________________________________________________________________________
    def print_magnets(self):

        #for i in self.elements.itervalues():
        for name in self.element_names:
            i = self.elements[name]

            #elements with own print
            if hasattr(i, "print_pos"):
                i.print_pos()
                continue

            #default action
            print(i.name, " z:", i.center_z, " x:", i.center_x, " l:", i.length,\
            " r1:", i.rad1, " r2:", i.rad2, " theta:", i.THETA,\
            "start_z:", i.center_z+i.length/2.)





































