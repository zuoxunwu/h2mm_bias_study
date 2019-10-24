run_dir=$PWD

# generate toys for bkg model $1, signal strenght $2, number of toys $3, random seed $4, study_title $5
toy_gen(){
    echo ${run_dir}
    # I don't know how to set name of output files of generated toys
    # this is work around
    cd temps
    mkdir -p ${5}/$1$2
    cd ${5}/$1$2
    combine -d ${run_dir}/OutputFiles/${5}/c_01_test_s$1'.txt' -M GenerateOnly --toysFrequentist -t $3 -s ${4}000 --expectSignal $2 --saveToys
    # default file name of toys; change
    mv higgsCombineTest.GenerateOnly.mH120.${4}000'.root' ${run_dir}/OutputFiles/${5}/toy_$1$2_seed$4'.root'
    cd $run_dir
    # error? typo?
    rm -rf temps/${5}/$1
}

# fit toys for toy model $1, fit model $2, number of toys $3, signal strength $4, random seed $5, study_title $6
toy_fit(){
    echo ${run_dir}
    # outputs go in this directory
    mkdir -p temps/${6}/nbyn$1$2$4_seed$5
    cd temps/${6}/nbyn$1$2$4_seed$5
    # fit model2 to toy1
    combine $run_dir/OutputFiles/${6}/c_01_test_s$2'.txt' -M FitDiagnostics --toysFile $run_dir/OutputFiles/${6}/toy_$1$4_seed$5'.root' -t $3 --rMin -60 --rMax 60 --robustFit 1
}

# Input: toy_model $1, fit_model $2, dummpy $3, signal_strength $4, study_title $5
toy_fit_hadd(){
    mkdir -p temps/${5}/nbyn$1$2$4
    hadd temps/${5}/nbyn$1$2$4/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed1/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed2/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed3/fitDiagnostics.root
    cd temps/${5}/nbyn$1$2$4
}

# input: study_title $1
temp_cleanup(){
    cp -r temps/${1}/* OutputFiles/${1}
    rm -rf temps/${1}/* 
}
