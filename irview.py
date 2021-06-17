#!/usr/bin/python3

import math

import ROOT as rt

from interaction_region import interaction_region
from exit_window import exit_window

#_____________________________________________________________________________
if __name__ == "__main__":

    ir = interaction_region()

    ir.load_csv("data/v20210527/electron_18GeV.csv")

    #photon exit window
    #ew = exit_window("ew", -18.644, 0, 0.0026, 0.3, 0.25-math.pi/2)
    ew = exit_window("ew", -18.644, 0, 0.3, 0.0026, 0.25)
    ew.label = "Exit window"
    ir.add_element(ew)

    #put the beams
    #ir.add_beam(-31, 32)
    #ir.add_beam(-31, 32, is_electron=False)

    #electron beampipe on the rear side
    #ir.add_bpipe_el_rear()

    #photon detector
    #ir.add_photon_detector()

    # 17 mrad for hadron beam,  25 mrad beam crossing angle
    #ir.rotate(0.017)
    #ir.rotate(-0.025)
    #ir.rotate(-0.008)

    #central beam frame
    ir.draw_2d(-40, -60, 0, 100) # with ecal

    #outgoing beam frame
    #ir.rotate_translateX(0.026332, 0.224548100304)
    #ir.draw_2d(-40, -120, -2, 90)
    #ir.draw_2d(-40, -125, 0, 125) # with ecal

    #ir.analysis()
    ir.print_magnets()



















