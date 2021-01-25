# WWG Analysis
Based on NanoAOD Tools: <https://github.com/cms-nanoAOD/nanoAOD-tools>

Dedicated for WWG analysis on cms-connect environment

--------------
## content

- [Download and setup](#Download-and-setup)
- [Baseline selection](#Baseline-selection)
- [Condor mode](#Condor-mode)

--------------
<br>

## <span id="Download-and-setup"> Download and setup </span> 

```bash
cmsrel CMSSW_10_6_0
cd CMSSW_10_6_0/src
cmsenv
git clone https://github.com/Senphy/nanoAOD-WVG.git PhysicsTools/NanoAODTools 
cd PhysicsTools/NanoAODTools
scram b
```
<br>

## <span id="Baseline-selection"> Baseline selection </span>
In WZG_seletor, `WZG_Module.py` is designed for basic selection (e.g. pt cut). Use `WZG_postproc.py` to test.

```bash
python WWG_postproc.py -h
```


<br>

## <span id="Condor-mode"> Condor mode </span>
In condor folder, `condor_for_postproc.py` is designed for preparing codes and submitting them to HTcondor. The purpose is to run over samples on DAS in parallel. Similarly, it has `-f` and `-n` arguments.

First you need to setup grid certification
```bash
voms-proxy-info -voms cms -valid 192:00
```
Modify `Proxy_path` in `condor_for_post.py` according to you own settings

```bash
python condor_for_postproc.py -y 2016 -n WZ
```

