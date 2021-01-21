# WWG selector
Based on NanoAOD Tools: <https://github.com/cms-nanoAOD/nanoAOD-tools>

Dedicated for WWG analysis on cms-connect environment

--------------

<br>

## <span id="Download-and-setup"> Download and setup </span> 

```bash
FOR EXAMPLE:
source /cvmfs/cms.cern.ch/cmsset_default.sh

initial_path=${PWD}
scramv1 project CMSSW CMSSW_10_2_22
cd CMSSW_10_2_22/src
eval `scramv1 runtime -sh`

git clone https://github.com/phy-guanzh/WWG.git
scram b -j4

cd PhysicsTools/NanoAODTools/WWG_selector
python WWG_postproc.py -m local -n ZGJ -y 2021 -f root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAODv7/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/270000/AE6064CB-3F5C-DD45-AF59-4B22669A8E7D.root
```
<br>

## <span id="Baseline-selection"> Baseline selection </span>
In WZG_seletor, `WZG_Module.py` is designed for basic selection (e.g. pt cut). Use `WZG_postproc.py` to test.

```bash
python WZG_postproc.py -h
```

arguments:
- `-f`  specify the input file. For local file e.g. `/afs/xxx.root`. For DAS file e.g. `root://xxx`
- `-n`  dataset name in short. Use this option if you don't specify the `-f` option and it will automatically specify the input for supported dataset. **DO NOT** use this option with ```-f``` together
- `-y`  Used with `-n` option to specify which year to use
- `-m`  Run mode. Normally use `local`. `condor` mode is designed as an interface for `condor_for_postproc.py` in condor folder


`DAS_filesearch.py` is designed for returning LFN from given dataset. And store LFN into given filepath_GIVENFILENAME.txt. Then it will call `test_ValidSite_cfy.py` to search the valid site which can get access to the LFN.

<br>

## <span id="Condor-mode"> Condor mode </span>
In condor folder, `condor_for_postproc.py` is designed for preparing codes and submitting them to HTcondor. The purpose is to run over samples on DAS in parallel. Similarly, it has `-f` and `-n` arguments.

First you need to setup grid certification
```bash
voms-proxy-info -voms cms -valid 192:0
```
Modify `Proxy_path` in `condor_for_post.py` according to you own settings

```bash
python condor_for_postproc.py -y 2016 -n WZ
```


