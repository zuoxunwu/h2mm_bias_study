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
    cd ${run_dir}
    # outputs go in this directory
    mkdir -p temps/${6}/nbyn$1$2_$4
    cd temps/${6}/nbyn$1$2_$4
    # fit model2 to toy1
    combine $run_dir/OutputFiles/${6}/c_01_test_s$2'.txt' -M FitDiagnostics --name _seed$5 --toysFile $run_dir/OutputFiles/${6}/toy_$1$4_seed$5'.root' --toysFrequentist -t $3 --forceRecreateNLL --rMin -60 --rMax 60 --robustFit 1
}

# Input: toy_model $1, fit_model $2, dummpy $3, signal_strength $4, study_title $5
toy_fit_hadd(){
    cd ${run_dir}
    mkdir -p temps/${5}/nbyn$1$2_$4
    hadd temps/${5}/nbyn$1$2_$4/fitDiagnostics.root temps/${5}/nbyn$1$2_$4/fitDiagnostics_seed*.root
#    hadd temps/${5}/nbyn$1$2$4/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed1/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed2/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed3/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed4/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed5/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed6/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed7/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed8/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed9/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed10/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed11/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed12/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed13/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed14/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed15/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed16/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed17/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed18/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed19/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed20/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed21/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed22/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed23/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed24/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed25/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed26/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed27/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed28/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed29/fitDiagnostics.root temps/${5}/nbyn$1$2$4_seed30/fitDiagnostics.root
#    cd temps/${5}/nbyn$1$2_$4
    cd ${run_dir}
}

# input: study_title $1
temp_cleanup(){
    cp -r temps/${1}/* OutputFiles/${1}
#    rm -rf temps/${1}/* 
}
