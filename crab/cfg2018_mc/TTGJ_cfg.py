from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'TTGJ_2018'
config.General.transferLogs= False
config.General.workArea = 'crab2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = './WWG/WWG_selector//WWG_crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py','./WWG/WWG_selector//WWG_postproc.py','./WWG/WWG_selector//WWG_Module.py','./WWG/WWG_selector//branches/WWG_keep_and_drop_2018.txt','./WWG/WWG_selector//branches/WWG_outbranch_mc_2018.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=MC','mode=crab','year=2018']
config.JobType.sendPythonFolder  = True

config.section_("Data")
config.Data.inputDataset = '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1

config.Data.outLFNDirBase ='/store/user/guanz/WWG_2018_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'TTGJ_2018'

config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

