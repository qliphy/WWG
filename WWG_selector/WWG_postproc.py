#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import *

# from WWG_Module import * 
import WWG_Module as WWG

import argparse
import re
import optparse



parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-k', dest='kind', default='MC', help='the kind for datasets (MC/data)')
parser.add_argument('-n', dest='name', default='test', help='dataset name in short, currently support' 
    '\n tZq_ll'
    '\n WZ'
    '\n TTWJetsToLNu'
    '\n ttZJets')
args = parser.parse_args()

print "mode: ", args.mode
print "year: ", args.year
print "dataset_name: ", args.name


jmeCorrections_ak4_2016 = createJMECorrector(True,2016,"A","Total","AK4PFchs",False,"MET",True,False,False,False)
jmeCorrections_ak4_2017 = createJMECorrector(True,2017,"A","Total","AK4PFchs",False,"METFixEE2017",True,False,False,False)
jmeCorrections_ak4_2018 = createJMECorrector(True,2018,"A","Total","AK4PFchs",False,"MET",True,False,True,False)
jmeCorrections_ak8_2016 = createJMECorrector(True,2016,"A","Total","AK8PFPuppi",False,"MET",True,False,False,False)
jmeCorrections_ak8_2017 = createJMECorrector(True,2017,"A","Total","AK8PFPuppi",False,"METFixEE2017",True,False,False,False)
jmeCorrections_ak8_2018 = createJMECorrector(True,2018,"A","Total","AK8PFPuppi",False,"MET",True,False,True,False)



#btag
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
btagSF_2018 = lambda: btagSFProducer("2018",'deepjet')
btagSF_2017 = lambda: btagSFProducer("2017",'deepjet')
btagSF_2016 = lambda: btagSFProducer("Legacy2016",'deepjet')

# prefiring
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
PrefCorr_2016 = lambda: PrefCorr("L1prefiring_jetpt_2016BtoH.root","L1prefiring_jetpt_2016BtoH","L1prefiring_photonpt_2016BtoH.root","L1prefiring_photonpt_2016BtoH")
PrefCorr_2017 = lambda: PrefCorr("L1prefiring_jetpt_2017BtoF.root","L1prefiring_jetpt_2017BtoF","L1prefiring_photonpt_2017BtoF.root","L1prefiring_photonpt_2017BtoF")




# classify input files
if args.file == '':
    print "no local file input, use DAS file"
    dataset = ''
    if 'crab' in args.mode:
        from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
        files = inputFiles()
        jsoninput = runsAndLumis()
        fwkjobreport = True

    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    elif 'condor' in args.mode:
        pass

else:    
    files = []
    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    # designed for single file here in order to run in parallel
    if 'condor' in args.mode:
        import DAS_filesearch as search
        files.append(search.getValidSite(args.file) + args.file)
        print 'input files: ',files
        print 'test'

    # local specific file input, also support root://xxx    
    else:
        import DAS_filesearch as search
        if not ',' in args.file:
            files.append(args.file)

        else:
            for i in args.file.split(','):
                files.append(i)

        print 'input files: ',files
if args.kind == 'data':
    p=PostProcessor(".",files,branchsel="WWG_keep_and_drop_2018.txt",modules=[countHistogramsProducer(),WWG.WWG_Producer()],provenance=True,fwkJobReport=fwkjobreport,jsonInput=jsoninput,outputbranchsel="WWG_outbranch_mc_2018.txt")
    p.run()
elif args.kind =='MC':
    if args.year=='2018':
        p=PostProcessor(".",files,branchsel="WWG_keep_and_drop_2018.txt",modules=[countHistogramsProducer(),muonScaleRes2018(),jmeCorrections_ak4_2018(),jmeCorrections_ak8_2018(),btagSF_2018(),WWG.WWG_Producer(),puWeight_2018()],provenance=True,fwkJobReport=fwkjobreport,jsonInput=jsoninput,outputbranchsel="WWG_outbranch_mc_2018.txt")
        p.run()
    elif args.year=='2017':
        p = PostProcessor(".", files, branchsel="WWG_keep_and_drop_2018.txt",modules=[countHistogramsProducer(), muonScaleRes2017(), jmeCorrections_ak4_2017(),jmeCorrections_ak8_2017(),btagSF_2017(),PrefCorr_2017(), WWG.WWG_Producer(), puWeight_2017()], provenance=True,fwkJobReport=fwkjobreport,jsonInput=jsoninput,outputbranchsel="WWG_outbranch_mc_2018.txt")
        p.run()
    elif args.year == '2016':
        p = PostProcessor(".", files, branchsel="WWG_keep_and_drop_2018.txt",modules=[countHistogramsProducer(), muonScaleRes2016(), jmeCorrections_ak4_2016(),jmeCorrections_ak8_2016(),btagSF_2016(), PrefCorr_2016(),WWG.WWG_Producer(), puWeight_2016()], provenance=True,fwkJobReport=fwkjobreport,jsonInput=jsoninput,outputbranchsel="WWG_outbranch_mc_2018.txt")
        p.run()
else:
    print "Unknown dataset kind "





print "MET_pass","\t","=","\t",WWG.MET_pass
print "muon_pass","\t","=","\t",WWG.muon_pass
print "electron_pass","\t","=","\t",WWG.electron_pass
print "photon_pass","\t","=","\t",WWG.photon_pass
print
print "none_photon_reject","\t","=","\t",WWG.none_photon_reject
print "none_lepton_reject","\t","=","\t",WWG.none_lepton_reject
print "none_2lepton_reject","\t","=","\t",WWG.none_2lepton_reject
print "different_charge_reject","\t","=","\t",WWG.different_charge_reject
print "minus_mll ","\t","=","\t",WWG.minus_mll
print "all reject",WWG.none_photon_reject+WWG.none_2lepton_reject+WWG.different_charge_reject+WWG.minus_mll+WWG.mll_reject+WWG.pt_reject+WWG.njet_reject


print "emu_pass","\t","=","\t",WWG.emu_pass
print "ee_pass","\t","=","\t",WWG.ee_pass
print "mumu_pass","\t","=","\t",WWG.mumu_pass
print "btagjet_reject","\t","=","\t",WWG.btagjet_reject
print "deltar_reject","\t","=","\t",WWG.deltar_reject
print "pt_reject","\t","=","\t",WWG.pt_reject
print "mll_reject","\t","=","\t",WWG.mll_reject
print "njet_reject","\t","=","\t",WWG.njet_reject
print "n_posi","\t","=","\t",WWG.n_posi
print "n_minus","\t","=","\t",WWG.n_minus
print "n_num","\t","=","\t",WWG.n_num

