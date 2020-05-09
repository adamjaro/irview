#!/usr/bin/python

import ROOT as rt

from interaction_region import interaction_region

#_____________________________________________________________________________
if __name__ == "__main__":

    ir = interaction_region()

    #ir.load_magnets("data/magnets_electron_forward_18GeV_20190617.txt")
    #ir.load_magnets("data/magnets_electron_rear_18GeV_20190617.txt")

    #ir.load_magnets("data/magnets_hadron_forward_275GeV_20190617.txt", is_electron=False)
    #ir.load_magnets("data/magnets_hadron_rear_275GeV_20190617.txt", is_electron=False)

    #ir.read_survey_lepton("data/lepton-survey-ir6.18GeV.dat")
    #ir.read_survey_hadron("data/Hadron-275GeV.surveyRear")
    #ir.read_survey_hadron("data/Hadron-275GeV.surveyForward")

    ir.load_tab("data/200309-er-ip6-95832bb/er-95832bb.txt", -40)
    #ir.load_tab_sl("data/200309-er-ip6-95832bb/er-95832bb.txt", -40)

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
    #ir.rotate(0.018332)

    #default frame
    #ir.draw_2d(-40, -40, -2, 140)

    #central beam frame
    #ir.rotate(0.008)
    #ir.draw_2d(-40, -80, -2, 120)

    #outgoing beam frame
    ir.rotate_translateX(0.026332, 0.224548100304)
    ir.draw_2d(-40, -120, -2, 90)

    #ir.draw_2d(-35, -90, 36, 104) # zmin, xmin, zmax, xmax
    #ir.draw_2d(-35, -40, -2, 55)
    #ir.draw_2d(-20, -80, -2, -40)
    #ir.draw_2d(-40, -60, -2, 130)
    #ir.draw_2d(-40, -90, -2, 110)
    #ir.draw_2d(-110, -90, 2, 200)
    #ir.draw_2d(-110, -30, 2, 300)

    #ir.analysis()
    ir.print_magnets()



















