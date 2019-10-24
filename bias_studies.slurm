#!/bin/sh


#SBATCH --account=avery
#SBATCH --job-name=bias_study
#SBATCH --qos=avery
#SBATCH --mail-type=ALL
#SBiTCH --ntasks=1
#SBATCH -N 1
#SBATCH -n 20
#SBATCH --mem=20gb
#SBATCH --time=20:00:00
#SBATCH --output=serial_test_%j.out
#SBATCH --mail-user=pq8556@ufl.edu
pwd; hostname; date
eval `scramv1 runtime -sh`
echo "Running bias studies using multiple CPU core"
. bash_scripts/run_bias_study_set.sh
date
