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
import DAS_filesearch as search


parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-n', dest='name', default='test', help='dataset name in short, currently support' 
    '\n tZq_ll'
    '\n WZ'
    '\n TTWJetsToLNu'
    '\n ttZJets')
args = parser.parse_args()

print "mode: ", args.mode
print "year: ", args.year
print "dataset_name: ", args.name


jmeCorrections_ak4_2018 = createJMECorrector(True,2018,"A","Total","AK4PFchs",False,"MET",True,False,True,False)
jmeCorrections_ak8_2018 = createJMECorrector(True,2018,"A","Total","AK8PFPuppi",False,"MET",True,False,True,False)



# classify input files
if args.file == '':

    print "no local file input, use DAS file"
    dataset = ''
    if args.name == 'TZQ':
        if args.year == '2021': dataset = "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
    elif args.name == 'WW':
        if args.year == '2021': dataset = "/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM"
    elif args.name == 'TTGJ':
        if args.year == '2021': dataset = "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM"
    elif args.name == 'WZ':
        if args.year == '2020': dataset = "/WZTo3LNu_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"
    elif args.name == 'SingleElectron':
        if args.year == '2021': dataset = "/SingleElectron/Run2016C-05Feb2018-v2/NANOAOD"
    elif args.name == 'MuonEG':
        if args.year == '2021': dataset = "/MuonEG/Run2018A-Nano1June2019-v1/NANOAOD"
    elif args.name == 'SingleMuon':
        if args.year == '2021': dataset = "/SingleMuon/Run2018A-Nano1June2019-v1/NANOAOD"
    elif args.name == 'EGamma':
        if args.year == '2021': dataset = "/EGamma/Run2018A-Nano1June2019-v1/NANOAOD"
    elif args.name == 'DoubleMuon':
        if args.year == '2021': dataset = "/DoubleMuon/Run2018A-Nano1June2019-v1/NANOAOD"
    elif args.name == 'TW':
        if args.year == '2021': dataset = "/TWJToLNuLNu_EWK_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    elif args.name == 'ZZ':
        if args.year == '2021': dataset = "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"
    elif args.name == 'DY':
        if args.year == '2021': dataset = "/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"
    elif args.name == 'ZGJ':
        if args.year == '2021': dataset = "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"
    elif args.name == 'ZGJ2':
        if args.year == '2021': dataset = "/ZGToLLG_01J_LoosePtlPtg_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM"
    else:
        print
        "unknown dataset name"
        sys.exit(0)
    files = []

    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    if 'condor' in args.mode:
        pass

    else:
        search.getLFN(dataset, args.name+"_"+args.year)
        with open ("filepath_"+args.name+"_"+args.year+".txt","r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n')
                files.append(search.getValidSite(line)+line)

    print 'from DAS input files: ',files
    p = PostProcessor(".", files, branchsel="WWG_input_branch.txt",
                      modules=[countHistogramsProducer(), muonScaleRes2018(), jmeCorrections_ak4_2018(),
                               jmeCorrections_ak8_2018(), WWG.WWG_Producer(), puWeight_2018()], provenance=True,
                      outputbranchsel="WWG_output_branch.txt")
    p.run()

else:    
    files = []
    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    # designed for single file here in order to run in parallel
    if 'condor' in args.mode:
        files.append(search.getValidSite(args.file) + args.file)
        print 'input files: ',files
        print 'test'

    # local specific file input, also support root://xxx    
    else:
        if not ',' in args.file:
            files.append(args.file)

        else:
            for i in args.file.split(','):
                files.append(i)

        print 'input files: ',files

    p=PostProcessor(".",files,branchsel="WWG_input_branch.txt",modules=[countHistogramsProducer(),muonScaleRes2018(),jmeCorrections_ak4_2018(),jmeCorrections_ak8_2018(),WWG.WWG_Producer(),puWeight_2018()],provenance=True,outputbranchsel="WWG_output_branch.txt")
    p.run()



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

