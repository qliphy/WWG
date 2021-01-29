exit_on_error() {
    result=$1
    code=$2
    message=$3

    if [ $1 != 0 ]; then
        echo $3
        exit $2
    fi
}

#### FRAMEWORK SANDBOX SETUP ####
# Load cmssw_setup function
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/cmssw_setup.sh . || exit_on_error $? 150 "Could not download sandbox1."
#cp /etc/ciconnect/templates/cmssw_setup.sh .
source cmssw_setup.sh

# Setup CMSSW Base
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh


xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/new1/SMP-RunIIFall18wmLHEGS-00053_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/new1/SMP-RunIIAutumn18DRPremix-00011_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/new1/SMP-RunIIAutumn18DRPremix-00011_2_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/new1/SMP-RunIIAutumn18MiniAOD-00011_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/new1/SMP-RunIIAutumn18NanoAODv7-00125_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
#cmsrel CMSSW_10_2_18
#cd CMSSW_10_2_18/src
#cmsenv
#cd -
# Download sandbox, replace it when you have different sandbox_name
sandbox_name1="sandbox-CMSSW_10_2_6-e33be22.tar.bz2"
sandbox_name2="sandbox-CMSSW_10_2_18-441666a.tar.bz2"
sandbox_name3="sandbox-CMSSW_10_6_1-441666a.tar.bz2"
#sandbox_name4="sandbox-CMSSW_10_6_14-2376b2a.tar.bz2"
sandbox_name5="sandbox-CMSSW_10_5_0-b138232.tar.bz2"
sandbox_name4="sandbox-CMSSW_10_2_22-13ae64e.tar.bz2"
# Change to your own http
#wget --no-check-certificate --progress=bar "http://stash.osgconnect.net/+zguan/Wjets/condor/${sandbox_name1}"  || exit_on_error $? 150 "Could not download sandbox1."
#wget --no-check-certificate --progress=bar "http://stash.osgconnect.net/+zguan/Wjets/condor/${sandbox_name2}"  || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/gridpack/${sandbox_name4} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/gridpack/${sandbox_name5} . || exit_on_error $? 150 "Could not download sandbox1."

pushd .
# Setup framework from sandbox
#cmsrel CMSSW_10_6_14
#cd CMSSW_10_6_14/src
#eval `scramv1 runtime -sh`
#cmsenv
#git cms-init
#git cms-merge-topic kdlong:CMSSW_10_6_14_NanoGenWeights
#scramv1 b
#eval `scramv1 runtime -sh`
#tar -xf $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
#tar -vxf ${sandbox_name4} || exit_on_error $? 151 "Could not unpack sandbox"
#cd CMSSW_10_6_14/src
#scramv1 b
#eval `scramv1 runtime -sh`
#cmsenv
#eval `scramv1 runtime -sh`
popd
sandbox_name="$1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz"
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/gridpack/${sandbox_name} . || exit_on_error $? 150 "Could not download sandbox1."
sed -i "s/^.*tarball.tar.xz.*$/     args = cms.vstring(\'..\/$sandbox_name\'),/" -i SMP-RunIIFall18wmLHEGS-00053_1_cfg.py
seed_time=$(($(date +%s) % 100 + 1))
sed -i "s/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(15)/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int($seed_time)/g" -i SMP-RunIIFall18wmLHEGS-00053_1_cfg.py
rm -rf *.root
cmsRun SMP-RunIIFall18wmLHEGS-00053_1_cfg.py || exit_on_error $? 151 "ERROR GS"
cmsRun SMP-RunIIAutumn18DRPremix-00011_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
rm *inLHE.root *wmLHEGS-00053.root
cmsRun SMP-RunIIAutumn18DRPremix-00011_2_cfg.py
cmsRun SMP-RunIIAutumn18MiniAOD-00011_1_cfg.py
rm *DR*.root
#rm -rf cmssw-tmp
# Setup framework from sandbox
#pushd .
#cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
#popd
cmsRun SMP-RunIIAutumn18NanoAODv7-00125_1_cfg.py
rm *MiniAOD*.root
#rm $sandbox_name
#cmsRun SMP-RunIIAutumn18DRPremix-00048_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
#cmsRun SMP-RunIIAutumn18DRPremix-00048_2_cfg.py
#rm SMP-RunIIAutumn18DRPremix-00048_step1.root
#cmsRun SMP-RunIIAutumn18MiniAOD-00048_1_cfg.py
#rm SMP-RunIIAutumn18DRPremix-00048.root
rm -rf cmssw-tmp
# Setup framework from sandbox
#pushd .
#cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
#popd
#cmsRun SMP-RunIIAutumn18NanoAODv6-00019_1_cfg.py
#rm SMP-RunIIAutumn18MiniAOD-00048.root
# clean
#rm -rf cmssw-tmp
rm *py
rm *pyc
rm $sandbox_name4
#rm $sandbox_name2
