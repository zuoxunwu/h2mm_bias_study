#!/bin/bash
# Perform bias studies for multiple config files

# this define functions for biasstudy
. ./bash_scripts/write_condor_subs.sh
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_n10_n02.txt
#wait
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_n02_p02.txt
#wait
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_p02_p06.txt
#wait
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_p060_p068.txt
#wait
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_p068_p076.txt
#wait
#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_p076_p10.txt
#wait

#write_subs ./Configs/WH6cats_an/toyqdataq/WH_BDT_p06_p10.txt
#wait

#write_subs ./Configs/ZH2cats/ZH_BDT_n10_p04.txt
#wait
#write_subs ./Configs/ZH2cats/ZH_BDT_p04_p10.txt
#wait


write_subs ./Configs/ZH2cats/ZH_BDT_n10_n01.txt
#wait
#write_subs ./Configs/ZH2cats/ZH_BDT_n01_p10.txt
#wait
#write_subs ./Configs/ZH2cats/ZH_BDT_n10_p10.txt
#wait

#write_subs ./Configs/WH3cats_final/WH_BDT_n10_n01.txt
#wait
#write_subs ./Configs/WH3cats_final/WH_BDT_n01_p03.txt
#wait
#write_subs ./Configs/WH3cats_final/WH_BDT_p03_p10.txt
#wait
