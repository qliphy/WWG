from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'DoubleMuon_Run2018C_2018'
config.General.transferLogs= False
config.General.workArea = 'crab2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = '../WWG_selector//WWG_crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py','../WWG_selector//WWG_postproc.py','../WWG_selector//WWG_Module.py','../WWG_selector//branches/WWG_keep_and_drop_2018.txt','../WWG_selector//branches/WWG_outbranch_data_2018.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=data','mode=crab','year=2018']
config.JobType.sendPythonFolder  = True

config.section_("Data")
config.Data.inputDataset = '/DoubleMuon/Run2018C-Nano1June2019-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Data.outLFNDirBase ='/store/user/guanz/WWG_2018_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'DoubleMuon_Run2018C_2018'

config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

