
import ROOT as rt
from ROOT import TFrame, TText, TLatex
from ROOT import  TGraph, TVector2, TMath

#_____________________________________________________________________________
class vmagnet(object):
    #_____________________________________________________________________________
    def __init__(self):
        #set magnet from configuration dictionary
        self.name = ""
        self.center_z = 0.
        self.center_x = 0.
        self.length = 0.
        self.rad1 = 0.
        self.rad2 = 0.
        self.field = 0.
        #electron or hadron
        self.is_electron = True
        #initial angle
        self.theta_0 = 0.
        #parameters from MAD-X survey
        self.S = 0.
        self.L = 0.
        self.X = 0.
        self.Z = 0.
        self.THETA = 0.
        self.has_survey = False
        #drawing configuration
        self.fill_style = 1000
        self.label_down = False
        self.label = ""
        self.no_label = False
        self.line_col = rt.kBlue
        self.fill_col = rt.kGreen-2

    #_____________________________________________________________________________
    def read_survey(self, lin):
        #values from MAD-X survey

        self.S = float( lin["S"] )
        self.L = float( lin["L"] )
        self.X = float( lin["X"] )
        self.Z = float( lin["Z"] )
        self.THETA = float( lin["THETA"] ) + self.theta_0
        self.has_survey = True

    #_____________________________________________________________________________
    def rotate_translateX(self, theta, xt):

        #combined rotation and translation
        self.rotate(theta)
        self.translateX(xt)

    #_____________________________________________________________________________
    def translateX(self, xt):

        #translate the magnet along x

        self.center_x += xt

    #_____________________________________________________________________________
    def rotate(self, theta):
        #rotate by angle theta about the origin

        #get new center_z and center_x by TVector2 rotation
        vec = TVector2(self.center_z, self.center_x).Rotate(theta)
        self.center_z = vec.X()
        self.center_x = vec.Y()

        #rotate along magnet center
        self.THETA = self.THETA - theta

    #_____________________________________________________________________________
    def draw_2d(self):

        #draw only magnets with survey defined
        if not self.has_survey: return

        #self.draw_box()
        self.draw_graph()

    #_____________________________________________________________________________
    def draw_graph(self):

        #inner and outer radius
        if self.center_z < 0:
            rad_right = self.rad1
            rad_left = self.rad2
        else:
            rad_right = self.rad2
            rad_left = self.rad1

        #edge points of the magnet
        vec = []
        vec.append( TVector2(self.length/2, rad_right) )
        vec.append( TVector2(self.length/2, -rad_right) )
        vec.append( TVector2(-self.length/2, -rad_left) )
        vec.append( TVector2(-self.length/2, rad_left) ) 

        #rotate along magnet axis and move to magnet center
        vpos = TVector2(self.center_z, self.center_x)
        for i in range(len(vec)):
            vec[i] = vec[i].Rotate(-self.THETA) + vpos

        #export points to the graph
        self.gbox = TGraph(len(vec)+1)
        self.gbox.SetLineColor(self.line_col)
        self.gbox.SetLineWidth(2)
        self.gbox.SetFillStyle(self.fill_style)
        self.gbox.SetFillColor(self.fill_col)

        for i in range(len(vec)):
            self.gbox.SetPoint(i, vec[i].X(), 100*vec[i].Y())

        #last point same as the first
        self.gbox.SetPoint(len(vec), vec[0].X(), 100*vec[0].Y())

        self.gbox.Draw("lfsame")

        #label
        if self.no_label: return
        #lx = (self.center_x + self.rad2)*100 + 4
        lx = (self.center_x + (self.rad1+self.rad2)/2)*100 + 4
        if lx < 30: lx = 30
        align = 12
        #left down
        if (self.center_z < 0 and not self.is_electron) or self.label_down:
            lx = (self.center_x - self.rad2)*100 - 4
            align = 32
        #right down
        if self.center_z > 0 and self.is_electron:
            lx = (self.center_x - self.rad2)*100 - 4
            if lx > -25: lx = -25
            align = 32
            #label above the magnet
            if self.center_x < -0.4:
                lx = (self.center_x + self.rad2)*100 + 4
                align = 12
        if self.label == "":
            self.label = self.name
        #self.glabel = TText(self.center_z, lx, self.label)
        self.glabel = TLatex(self.center_z, lx, self.label)
        self.glabel.SetTextSize(0.03)
        #self.glabel.SetTextSize(0.02)
        self.glabel.SetTextAngle(90)
        self.glabel.SetTextAlign(align)
        self.glabel.Draw("same")

    #_____________________________________________________________________________
    def draw_box(self):

        z1 = self.center_z - self.length/2
        z2 = z1 + self.length
        x1 = self.center_x - self.rad2
        x2 = x1 + 2*self.rad2

        #to cm
        x1 *= 100
        x2 *= 100

        #representation as a box
        self.box = TFrame(z1, x1, z2, x2)
        self.box.SetBorderMode(0)
        self.box.SetFillColor(rt.kGray+1)
        col = rt.kRed
        if self.is_electron == True: col = rt.kBlue
        self.box.SetLineColor(col)
        self.box.SetLineWidth(2)
        #self.box.Draw("same")

        #label
        lx = x2 + 2
        align = 11
        if lx < 0 and lx > -62: 
            lx = x1 - 5 # negative lx
            align = 31
        if self.center_z < 0 and self.center_x < 0.1:
            lx = x1 - 2 # negative z and x
            align = 31
        if lx > 0 and lx < 22: lx = 22 # small positive lx
        self.label = TText(z2, lx, self.name)
        self.label.SetTextSize(0.03)
        self.label.SetTextAngle(90)
        self.label.SetTextAlign(align)
        #self.label.Draw("same")
















