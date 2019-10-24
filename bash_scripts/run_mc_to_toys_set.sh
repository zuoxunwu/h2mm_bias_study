#!/bin/bash
#
# Perform bias studies for multiple config files

. ./bash_scripts/run_bias_study.sh
#run_study_pull ./Configs/WH_inclusive.txt
#wait 
#run_study_pull ./Configs/WH_BDT_n10_n02.txt
#wait
#run_study_pull ./Configs/WH_BDT_n02_p02.txt
#wait
#run_study_pull ./Configs/WH_BDT_p02_p06.txt
#wait
#run_study_pull ./Configs/WH_BDT_p06_p10.txt
#wait
run_study_pull ./Configs/WH6cats/mc_to_toys/WH_BDT_p060_p068.txt
mv ./OutputFiles/*.root ./OutputFiles/cat4
wait
run_study_pull ./Configs/WH6cats/mc_to_toys/WH_BDT_p068_p076.txt
mv ./OutputFiles/*.root ./OutputFiles/cat5
wait
run_study_pull ./Configs/WH6cats/mc_to_toys/WH_BDT_p076_p10.txt
mv ./OutputFiles/*.root ./OutputFiles/cat6
