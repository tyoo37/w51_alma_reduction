#!/bin/bash
#SBATCH --mail-type=BEGIN,END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=t.yoo@ufl.edu     # Where to send mail	
#SBATCH --ntasks=16
#SBATCH --mem=128gb # Job memory request PER NODE
#SBATCH --nodes=1 # exactly 1 node
#SBATCH --time=96:00:00               # Time limit hrs:min:sec
#SBATCH --qos=astronomy-dept-b
#SBATCH --account=astronomy-dept
#SBATCH --output=w51e_b6_spw9_19_linefree_%j.log
#SBATCH --job-name=w51e_b6_spw9_19_linefree
#SBATCH --export=ALL

export FIELD_ID="W51"
export BAND_TO_IMAGE=B6
export LOGFILENAME="casa_log_w51e2lbcont_sm_${FIELD_ID}_${BAND_TO_IMAGE}_12M_$(date +%Y-%m-%d_%H_%M_%S).log"

WORK_DIR='/orange/adamginsburg/w51/2017.1.00293.S/uvdata'
WORK_DIR='/orange/adamginsburg/w51/2017.1.00293.S/may2021_imaging'
WORK_DIR='/orange/adamginsburg/w51/TaehwaYoo/w51e_b6_imaging_family_spw9_19_linefree/'

export CASA=/orange/adamginsburg/casa/casa-release-5.6.0-60.el7/bin/casa
export CASA=/orange/adamginsburg/casa/casa-release-5.7.0-134.el7/bin/casa

module load git

which python
which git

git --version
echo $?

# not useing almaimf pipeline for this
#export ALMAIMF_ROOTDIR="/orange/adamginsburg/ALMA_IMF/reduction/reduction"
#cd ${ALMAIMF_ROOTDIR}
#python getversion.py
#export PYTHONPATH=$ALMAIMF_ROOTDIR

imaging_script=/orange/adamginsburg/w51/TaehwaYoo/w51e_b6_imaging_family_spw9_19_linefree/script_for_imaging_selfcal_starfromALMAIMF_spw9_19_linefree.py
cd ${WORK_DIR}
echo ${WORK_DIcR}

pycode="field='w51e2'; cleanmask='cleanmask_e2_new_tight.crtf'; cleanmask2='cleanmask_e2_new_tight_step1.crtf';"

pycode="$pycode startmodel=['/orange/adamginsburg/w51/TaehwaYoo/w51e_b6_imaging_2025/W51-E_B6_uid___A001_X1296_X213_continuum_merged_12M_robust0_selfcal7_finaliter.model.tt0', "

pycode="$pycode '/orange/adamginsburg/w51/TaehwaYoo/w51e_b6_imaging_2025/W51-E_B6_uid___A001_X1296_X213_continuum_merged_12M_robust0_selfcal7_finaliter.model.tt1']"
#pycode="$pycode startmodel=['/orange/adamginsburg/ALMA_IMF/2017.1.01355.L/imaging_results/W51-E_B6_uid___A001_X1296_X213_continuum_merged_12M_robust0_selfcal7_finaliter.model.tt0', "
#pycode="$pycode '/orange/adamginsburg/ALMA_IMF/2017.1.01355.L/imaging_results/W51-E_B6_uid___A001_X1296_X213_continuum_merged_12M_robust0_selfcal7_finaliter.model.tt1']"

echo $pycode

#xvfb-run -d ${CASA} --nogui --nologger --logfile=split_${LOGFILENAME} -c "execfile('$ALMAIMF_ROOTDIR/split_windows.py')"
echo "Logfilename is ${LOGFILENAME}"
echo xvfb-run -d ${CASA} --nogui --nologger --logfile=${LOGFILENAME} -c "${pycode}; execfile('${imaging_script}')"

xvfb-run -d ${CASA} --nogui --nologger --logfile=${LOGFILENAME} -c "${pycode}; execfile('${imaging_script}')"
