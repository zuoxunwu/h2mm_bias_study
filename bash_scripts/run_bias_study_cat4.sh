#!/bin/bash
# Perform bias studies for multiple config files

# this define functions for biasstudy
. ./bash_scripts/run_bias_study.sh
# cat 4
run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_p060_p068.txt
