#!/usr/bin/env python
# Analyzer for WWG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
import yaml
import argparse
#from pathlib import Path

#file_list = '~/new/wwgamma_5f_NLO_com_1310185_101.root'
#df=ROOT.RDataFrame("Events",file_list)
#column_list=df.GetColumnNames()
#branchList = []

#for i in range(0,len(column_list)):
#    branchList.append(column_list[i])
#print branchList
x='HLT'
point='.'
lead_pt_min = [20,25,30,50]
sublead_pt_min = []

#for elem in  branchList :
#    if x in elem and point not in elem:
#        filtered_list.append(elem)

N_init=0
N_pass = 0
N_rej = 0
eff_emu_ll=0
eff_emu_ls=0
eff_emu_ss=0
eff_emu_sl=0
eff_ee_ll=0
eff_ee_ls=0
eff_ee_ss=0
eff_ee_sl=0
eff_mumu_ll=0
eff_mumu_ls=0
eff_mumu_ss=0
eff_mumu_sl=0
ee_pass_lleta_sleta=0
ee_pass_lleta_sseta=0
ee_pass_lseta_sleta=0
ee_pass_lseta_sseta=0
emu_pass_lleta_sleta=0
emu_pass_lleta_sseta=0
emu_pass_lseta_sleta=0
emu_pass_lseta_sseta=0
mumu_pass_lleta_sleta=0
mumu_pass_lleta_sseta=0
mumu_pass_lseta_sleta=0
mumu_pass_lseta_sseta=0
ee_pass_hlt_lleta_sleta=0
ee_pass_hlt_lleta_sseta=0
ee_pass_hlt_lseta_sleta=0
ee_pass_hlt_lseta_sseta=0
emu_pass_hlt_lleta_sleta=0
emu_pass_hlt_lleta_sseta=0
emu_pass_hlt_lseta_sleta=0
emu_pass_hlt_lseta_sseta=0
mumu_pass_hlt_lleta_sleta=0
mumu_pass_hlt_lleta_sseta=0
mumu_pass_hlt_lseta_sleta=0
mumu_pass_hlt_lseta_sseta=0

class WWG_HLT(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "i")
        self.out.branch("HLT",  "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        global N_init
        global N_pass
        global N_rej
        global lpt_max
        global lpt_min
        global spt_max
        global spt_min
        global N_passnum
        global ee_pass_lleta_sleta
        global ee_pass_lleta_sseta
        global ee_pass_lseta_sleta
        global ee_pass_lseta_sseta
        global emu_pass_lleta_sleta
        global emu_pass_lleta_sseta
        global emu_pass_lseta_sleta
        global emu_pass_lseta_sseta
        global mumu_pass_lleta_sleta
        global mumu_pass_lleta_sseta
        global mumu_pass_lseta_sleta
        global mumu_pass_lseta_sseta
        global ee_pass_hlt_lleta_sleta
        global ee_pass_hlt_lleta_sseta
        global ee_pass_hlt_lseta_sleta
        global ee_pass_hlt_lseta_sseta
        global emu_pass_hlt_lleta_sleta
        global emu_pass_hlt_lleta_sseta
        global emu_pass_hlt_lseta_sleta
        global emu_pass_hlt_lseta_sseta
        global mumu_pass_hlt_lleta_sleta
        global mumu_pass_hlt_lleta_sseta
        global mumu_pass_hlt_lseta_sleta
        global mumu_pass_hlt_lseta_sseta
        N_init +=1
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")

        electrons_select = []
        muons_select = []
        leptons_select = []

        for i in range(0,len(muons)):
            if muons[i].mediumId == True:
                muons_select.append(i)
                leptons_select.append(i)
        for i in range(0, len(electrons)):
            if electrons[i].cutBased >= 3:
                electrons_select.append(i)
                leptons_select.append(i)
        if len(electrons_select)+len(muons_select) != 2:      #reject event if there are not exactly two leptons
            return False

        if len(muons_select) == 1 and len(electrons_select) == 1:
            if muons[muons_select[0]].pt > electrons[electrons_select[0]].pt:
                if (muons[muons_select[0]].pt < lpt_max) and (muons[muons_select[0]].pt >lpt_min) and (electrons[electrons_select[0]].pt < spt_max) and (electrons[electrons_select[0]].pt > spt_min):
                    if (muons[muons_select[0]].eta > 1.47) and (electrons[electrons_select[0]].eta>1.47):
                        emu_pass_lleta_sleta += 1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lleta_sleta +=1
                    if (muons[muons_select[0]].eta > 1.47) and (electrons[electrons_select[0]].eta < 1.47):
                        emu_pass_lleta_sseta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lleta_sseta += 1
                    if (muons[muons_select[0]].eta < 1.47) and (electrons[electrons_select[0]].eta > 1.47):
                        emu_pass_lseta_sleta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lseta_sleta += 1
                    if (muons[muons_select[0]].eta < 1.47) and (electrons[electrons_select[0]].eta < 1.47):
                        emu_pass_lseta_sseta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lseta_sseta += 1
            else:
                if (muons[muons_select[0]].pt < spt_max) and (muons[muons_select[0]].pt >spt_min) and (electrons[electrons_select[0]].pt < lpt_max) and (electrons[electrons_select[0]].pt > lpt_min):
                    if (muons[muons_select[0]].eta > 1.47) and (electrons[electrons_select[0]].eta>1.47):
                        emu_pass_lleta_sleta += 1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lleta_sleta +=1
                    if (muons[muons_select[0]].eta < 1.47) and (electrons[electrons_select[0]].eta > 1.47):
                        emu_pass_lleta_sseta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lleta_sseta += 1
                    if (muons[muons_select[0]].eta > 1.47) and (electrons[electrons_select[0]].eta < 1.47):
                        emu_pass_lseta_sleta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lseta_sleta += 1
                    if (muons[muons_select[0]].eta < 1.47) and (electrons[electrons_select[0]].eta < 1.47):
                        emu_pass_lseta_sseta +=1
                        if (event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL):
                            emu_pass_hlt_lseta_sseta += 1

        if len(muons_select) == 0 and len(electrons_select) == 2:
            if electrons[electrons_select[0]].pt > electrons[electrons_select[1]].pt:
                if (electrons[electrons_select[0]].pt <lpt_max) and (electrons[electrons_select[0]].pt>lpt_min) and (electrons[electrons_select[1]].pt<spt_max) and (electrons[electrons_select[1]].pt>spt_min):
                    if (electrons[electrons_select[0]].eta>1.47) and (electrons[electrons_select[1]].eta > 1.47):
                        ee_pass_lleta_sleta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lleta_sleta += 1
                    if (electrons[electrons_select[0]].eta>1.47) and (electrons[electrons_select[1]].eta < 1.47):
                        ee_pass_lleta_sseta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lleta_sseta += 1
                    if (electrons[electrons_select[0]].eta<1.47) and (electrons[electrons_select[1]].eta > 1.47):
                        ee_pass_lseta_sleta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lseta_sleta += 1
                    if (electrons[electrons_select[0]].eta<1.47) and (electrons[electrons_select[1]].eta < 1.47):
                        ee_pass_lseta_sseta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lseta_sseta += 1
            else:
                if (electrons[electrons_select[0]].pt < spt_max) and (electrons[electrons_select[0]].pt > spt_min) and (electrons[electrons_select[1]].pt < lpt_max) and (electrons[electrons_select[1]].pt > lpt_min):
                    if (electrons[electrons_select[0]].eta > 1.47) and (electrons[electrons_select[1]].eta > 1.47):
                        ee_pass_lleta_sleta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lleta_sleta += 1
                    if (electrons[electrons_select[0]].eta < 1.47) and (electrons[electrons_select[1]].eta > 1.47):
                        ee_pass_lleta_sseta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lleta_sseta += 1
                    if (electrons[electrons_select[0]].eta > 1.47) and (electrons[electrons_select[1]].eta < 1.47):
                        ee_pass_lseta_sleta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lseta_sleta += 1
                    if (electrons[electrons_select[0]].eta < 1.47) and (electrons[electrons_select[1]].eta < 1.47):
                        ee_pass_lseta_sseta += 1
                        if (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL):
                            ee_pass_hlt_lseta_sseta += 1
        if len(muons_select) == 2 and len(electrons_select) == 0:
            if muons[muons_select[0]].pt > muons[muons_select[1]].pt:
                if (muons[muons_select[0]].pt<lpt_max) and (muons[muons_select[0]].pt>lpt_min)and (muons[muons_select[1]].pt < spt_max) and (muons[muons_select[1]].pt >spt_min):
                    if (muons[muons_select[0]].eta>1.47) and (muons[muons_select[1]].eta>1.47):
                        mumu_pass_lleta_sleta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lleta_sleta += 1
                    if (muons[muons_select[0]].eta>1.47) and (muons[muons_select[1]].eta<1.47):
                        mumu_pass_lleta_sseta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lleta_sseta += 1
                    if (muons[muons_select[0]].eta<1.47) and (muons[muons_select[1]].eta>1.47):
                        mumu_pass_lseta_sleta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lseta_sleta += 1
                    if (muons[muons_select[0]].eta<1.47) and (muons[muons_select[1]].eta<1.47):
                        mumu_pass_lseta_sseta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lseta_sseta += 1
            else:
                if (muons[muons_select[0]].pt<spt_max) and (muons[muons_select[0]].pt>spt_min)and (muons[muons_select[1]].pt < lpt_max) and (muons[muons_select[1]].pt >lpt_min):
                    if (muons[muons_select[0]].eta>1.47) and (muons[muons_select[1]].eta>1.47):
                        mumu_pass_lleta_sleta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lleta_sleta += 1
                    if (muons[muons_select[0]].eta<1.47) and (muons[muons_select[1]].eta>1.47):
                        mumu_pass_lleta_sseta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lleta_sseta += 1
                    if (muons[muons_select[0]].eta>1.47) and (muons[muons_select[1]].eta<1.47):
                        mumu_pass_lseta_sleta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lseta_sleta += 1
                    if (muons[muons_select[0]].eta<1.47) and (muons[muons_select[1]].eta<1.47):
                        mumu_pass_lseta_sseta += 1
                        if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8):
                            mumu_pass_hlt_lseta_sseta += 1
        return True



	# Record the pass numbers for each cut. Noticed that for efficiency, those who can't pass the MET cut may not be counted because it will pass to next event directly.


    #if event.Generator_weight > 0 :
    #    n_posi +=1
    #else:
    #    n_minus +=1

files = ['~/new/15_4.root']
for k in lead_pt_min:
    sublead_pt_min = []
    if k == 20:
        lpt_max = 25
        lpt_min = k
        ns = (k - 10) / 5.
        for i in range(0, int(ns) + 1):
            sublead_pt_min.append(i * 5 + 10.0)
        print(sublead_pt_min)

    if k == 25:
        lpt_max = 30
        lpt_min = k
        ns = (k - 10) / 5.
        for i in range(0, int(ns) + 1):
            sublead_pt_min.append(i * 5 + 10)
        print(sublead_pt_min)
    if k == 30:
        lpt_max = 50
        lpt_min = k
        ns = (k - 10) / 5.
        for i in range(0, int(ns) + 1):
            sublead_pt_min.append(i * 5 + 10)
        print(sublead_pt_min)
    if k == 50:
        lpt_max = float('inf')
        lpt_min = k
        ns = (k - 10) / 5.
        for i in range(0, int(ns) + 1):
            sublead_pt_min.append(i * 5 + 10)
        print(sublead_pt_min)
    for m in sublead_pt_min:
        if m == 10:
            spt_max = 15
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True,outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47\n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll)+"\n")
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls)+"\n")
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll)+"\n")
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()
        if m == 15:
            spt_max = 20
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True,
                              outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47\n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll))
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls)+"\n")
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll))
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()
        if m == 20:
            spt_max = 25
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True,outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47\n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll))
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls)+"\n")
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll)+"\n")
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()
        if m == 25:
            spt_max = 30
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True, outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47\n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll)+"\n")
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls))+"\n"
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll)+"\n")
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()
        if m == 30:
            spt_max = 50
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True,outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47\n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll)+"\n")
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls)+"\n")
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll)+"\n")
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()
        if m == 50:
            spt_max = float("inf")
            spt_min = m
            print "lmax", lpt_max, "lmin", lpt_min, "smax", spt_max, "smin", spt_min
            p = PostProcessor(".", files, branchsel="WWG_input_branch.txt", modules=[WWG_HLT()], provenance=True,outputbranchsel="WWG_output_branch.txt1")
            p.run()
            print "example:ee_pass_lleta_sleta",ee_pass_lleta_sleta,"ee_pass_hlt_lleta_sleta",ee_pass_hlt_lleta_sleta
            print "please check the value"
            eff_ee_ll=float(ee_pass_hlt_lleta_sleta)/float(ee_pass_lleta_sleta)
            eff_ee_ls = float(ee_pass_hlt_lleta_sseta) / float(ee_pass_lleta_sseta)
            eff_ee_sl = float(ee_pass_hlt_lseta_sleta) / float(ee_pass_lseta_sleta)
            eff_ee_ss = float(ee_pass_hlt_lseta_sseta) / float(ee_pass_lseta_sseta)
            eff_emu_ll = float(emu_pass_hlt_lleta_sleta) / float(emu_pass_lleta_sleta)
            eff_emu_ls = float(emu_pass_hlt_lleta_sseta) / float(emu_pass_lleta_sseta)
            eff_emu_sl = float(emu_pass_hlt_lseta_sleta) / float(emu_pass_lseta_sleta)
            eff_emu_ss = float(emu_pass_hlt_lseta_sseta) / float(emu_pass_lseta_sseta)
            eff_mumu_ll = float(mumu_pass_hlt_lleta_sleta) / float(mumu_pass_lleta_sleta)
            eff_mumu_ls = float(mumu_pass_hlt_lleta_sseta) / float(mumu_pass_lleta_sseta)
            eff_mumu_sl = float(mumu_pass_hlt_lseta_sleta) / float(mumu_pass_lseta_sleta)
            eff_mumu_ss = float(mumu_pass_hlt_lseta_sseta) / float(mumu_pass_lseta_sseta)
            print "eff_ee_ll",eff_ee_ll
            with open("WWA_HLT"+"lptmax_"+str(lpt_max)+"_"+"lptmin_"+str(lpt_min)+"_"+"sptmax"+"_"+ str(spt_max)+"_"+"sptmin"+"_"+str(spt_min)+".log", "w+") as f:
                f.write("l means eta > 1.47 and s means eta < 1.47 \n")
                f.write("lptmax"+"\t"+str(lpt_max)+"\t"+ "lptmin"+"\t"+str(lpt_min)+"\t"+"sptmax"+"\t"+ str(spt_max)+"\t"+"sptmin"+"\t"+str(spt_min)+"\t"+":" +"\n")
                f.write("emu_ll:"+"\t"+str(emu_pass_lleta_sleta)+"\t"+"emu_hlt_ll:"+str(emu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_emu_ll)+"\n")
                f.write("emu_ls:" + "\t" + str(emu_pass_lleta_sseta) + "\t" + "emu_hlt_ls:" + str(emu_pass_hlt_lleta_sseta) + "\t" + "eff_emu_ls:" + "\t" + str(eff_emu_ls)+"\n")
                f.write("emu_sl:" + "\t" + str(emu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(emu_pass_hlt_lseta_sleta) + "\t" + "eff_emu_sl:" + "\t" + str(eff_emu_sl)+"\n")
                f.write("emu_ss:" + "\t" + str(emu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(emu_pass_hlt_lseta_sseta) + "\t" + "eff_emu_ss:" + "\t" + str(eff_emu_ss)+"\n")
                f.write("ee_ll:" + "\t" + str(ee_pass_lleta_sleta) + "\t" + "ee_hlt_ll:" + str(ee_pass_hlt_lleta_sleta) + "\t" + "eff_ee_ll:" + "\t" + str(eff_ee_ll)+"\n")
                f.write("ee_ls:" + "\t" + str(ee_pass_lleta_sseta) + "\t" + "ee_hlt_ls:" + str(ee_pass_hlt_lleta_sseta) + "\t" + "eff_ee_ls:" + "\t" +str(eff_ee_ls)+"\n")
                f.write("ee_sl:" + "\t" + str(ee_pass_lseta_sleta) + "\t" + "ee_hlt_sl:" + str(ee_pass_hlt_lseta_sleta) + "\t" + "eff_ee_sl:" + "\t" + str(eff_ee_sl)+"\n")
                f.write("ee_ss:" + "\t" + str(ee_pass_lseta_sseta) + "\t" + "ee_hlt_ss:" + str(ee_pass_hlt_lseta_sseta) + "\t" + "eff_ee_ss:" + "\t" + str(eff_ee_ss)+"\n")
                f.write("mumu_ll:"+"\t"+str(mumu_pass_lleta_sleta)+"\t"+"mumu_hlt_ll:"+str(mumu_pass_hlt_lleta_sleta)+"\t"+"eff_emu_ll:"+"\t"+str(eff_mumu_ll)+"\n")
                f.write("mumu_ls:" + "\t" + str(mumu_pass_lleta_sseta) + "\t" + "mumu_hlt_ls:" + str(mumu_pass_hlt_lleta_sseta) + "\t" + "eff_mumu_ls:" + "\t" + str(eff_mumu_ls)+"\n")
                f.write("mumu_sl:" + "\t" + str(mumu_pass_lseta_sleta) + "\t" + "emu_hlt_sl:" + str(mumu_pass_hlt_lseta_sleta) + "\t" + "eff_mumu_sl:" + "\t" + str(eff_mumu_sl)+"\n")
                f.write("mumu_ss:" + "\t" + str(mumu_pass_lseta_sseta) + "\t" + "emu_hlt_ll:" + str(mumu_pass_hlt_lseta_sseta) + "\t" + "eff_mumu_ss:" + "\t" + str(eff_mumu_ss)+"\n")
            f.close()



    
