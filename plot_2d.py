
import ROOT as rt
from ROOT import gROOT, gPad, gStyle, TCanvas
from ROOT import TIter, TText, TH1, TFrame

#_____________________________________________________________________________
class plot_2d:
    #_____________________________________________________________________________
    def __init__(self, zmin, xmin, zmax, xmax):
        self.zmin = zmin
        self.xmin = xmin
        self.zmax = zmax
        self.xmax = xmax

    #_____________________________________________________________________________
    def draw(self, elements):

        gROOT.SetBatch()

        gStyle.SetPadTickY(1)
        gStyle.SetPadTickX(1)

        c1 = TCanvas("c1","c1",1000,700)
        frame = gPad.DrawFrame(self.zmin, self.xmin, self.zmax, self.xmax) # xmin, ymin, xmax, ymax in ROOT
        frame.SetTitle(";Length #it{z} (m);Horizontal #it{x} (cm)")
        siz = 0.035
        frame.SetTitleSize(siz)
        frame.SetLabelSize(siz)
        frame.SetTitleSize(siz, "Y")
        frame.SetLabelSize(siz, "Y")

        frame.GetYaxis().SetTitleOffset(1)
        frame.GetXaxis().SetTitleOffset(1.2)
        frame.GetYaxis().CenterTitle()
        frame.GetXaxis().CenterTitle()
        gPad.SetLeftMargin(0.07)
        gPad.SetRightMargin(0.01)
        gPad.SetTopMargin(0.02)
        gPad.SetBottomMargin(0.09)

        #loop over elements
        for el in elements.itervalues():
            if not hasattr(el, "draw_2d"): continue
            el.draw_2d()

        #redraw these elements on the top
        draw_top = ["Q0EF", "beam_electron", "beam_hadron"]
        for i in draw_top:
            el = elements.get(i)
            if el is not None: el.draw_2d()

        gPad.SetGrid()

        self.invert_col(gPad)

        c1.SaveAs("01fig.pdf")

    #_____________________________________________________________________________
    def invert_col(self, pad):

        bgcol=rt.kBlack
        fgcol = rt.kOrange-3

        pad.SetFillColor(bgcol)
        pad.SetFrameLineColor(fgcol)

        next = TIter( pad.GetListOfPrimitives() )
        obj = next()
        while obj != None:

            #TText
            if obj.InheritsFrom( TText.Class() ) == True:
                if obj.GetTextColor() == rt.kBlack:
                    obj.SetTextColor( fgcol )

            #H1
            if obj.InheritsFrom( TH1.Class() ) == True:
                if obj.GetLineColor() == rt.kBlack:
                    obj.SetLineColor(fgcol)
                    obj.SetFillColor(bgcol)
                if obj.GetMarkerColor() == rt.kBlack: obj.SetMarkerColor(fgcol)
                obj.SetAxisColor(fgcol, "X")
                obj.SetAxisColor(fgcol, "Y")
                obj.SetLabelColor(fgcol, "X")
                obj.SetLabelColor(fgcol, "Y")
                obj.GetXaxis().SetTitleColor(fgcol)
                obj.GetYaxis().SetTitleColor(fgcol)

            #TFrame
            if obj.InheritsFrom( TFrame.Class() ) == True:
                if obj.GetLineColor() == rt.kBlack:
                    obj.SetLineColor(fgcol)
                    obj.SetFillColor(bgcol)

            #print obj.GetName(), obj.ClassName()

            #move to the next item
            obj = next()



































