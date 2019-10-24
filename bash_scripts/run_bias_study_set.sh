#!/bin/bash
# Perform bias studies for multiple config files

# this define functions for biasstudy
. ./bash_scripts/run_bias_study.sh
#run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_n10_n02.txt
#wait
#run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_n02_p02.txt
#wait
#run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_p02_p06.txt
#wait
#run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_p060_p068.txt
#wait
#run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_p068_p076.txt
#wait
run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_p076_p10.txt
wait
#run_study_pull ./Configs/WH6cats/toyqdataq/WH_BDT_p068_p076.txt
#wait
#run_study_pull ./Configs/WH6cats/toyqdataq/WH_BDT_p076_p10.txt
