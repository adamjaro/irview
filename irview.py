#!/usr/bin/python

import ROOT as rt

from interaction_region import interaction_region

#_____________________________________________________________________________
if __name__ == "__main__":

    ir = interaction_region()

    ir.load_magnets("data/magnets_electron_forward_18GeV_20190617.txt")
    ir.load_magnets("data/magnets_electron_rear_18GeV_20190617.txt")

    ir.load_magnets("data/magnets_hadron_forward_275GeV_20190617.txt", is_electron=False)
    ir.load_magnets("data/magnets_hadron_rear_275GeV_20190617.txt", is_electron=False)

    ir.read_survey_lepton("data/lepton-survey-ir6.18GeV.dat")
    ir.read_survey_hadron("data/Hadron-275GeV.surveyRear")
    ir.read_survey_hadron("data/Hadron-275GeV.surveyForward")

    #put beams
    ir.add_beam(-31, 32)
    ir.add_beam(-31, 32, is_electron=False)

    #electron beampipe on the rear side
    ir.add_bpipe_el_rear()

    #photon detector
    ir.add_photon_detector()

    # 17 mrad for hadron beam,  25 mrad beam crossing angle
    ir.rotate(0.017)
    #ir.rotate(0.025)

    ir.draw_2d(-35, -90, 36, 104) # zmin, xmin, zmax, xmax
    #ir.draw_2d(-35, -20, -2, 50)

    #ir.analysis()


