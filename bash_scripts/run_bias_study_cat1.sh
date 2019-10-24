#!/bin/bash
# Perform bias studies for multiple config files

# this define functions for biasstudy
. ./bash_scripts/run_bias_study.sh
# cat1
run_study_pull ./Configs/WH6cats_an/toyqdataq/WH_BDT_n10_n02.txt
