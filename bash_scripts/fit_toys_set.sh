#!/bin/bash
# Perform bias studies for multiple config files

# this define functions for biasstudy
. ./bash_scripts/just_fit_toys.sh
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_n10_n02.txt
#wait
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_n02_p02.txt
#wait
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_p02_p06.txt
#wait
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_p060_p068.txt
#wait
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_p068_p076.txt
#wait
#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_p076_p10.txt
#wait

#fit_toy_sets ./Configs/WH6cats_an/toyqdataq/WH_BDT_p06_p10.txt
#wait

fit_toy_sets ./Configs/ZH2cats/ZH_BDT_n10_p04.txt
wait
fit_toy_sets ./Configs/ZH2cats/ZH_BDT_p04_p10.txt
#wait
