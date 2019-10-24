run_dir=$PWD

# generate toys for bkg model $1, signal strenght $2, number of toys $3
toy_gen(){
    # I don't know how to set name of output files of generated toys
    # this is work around
    cd temps
    mkdir -p $1$2
    cd $1$2
    combine -d ../../OutputFiles/c_01_test_s$1'.txt' -M GenerateOnly --toysFrequentist -t $3 --expectSignal $2 --saveToys
    # default file name of toys; change
    mv higgsCombineTest.GenerateOnly.mH120.123456.root ../../OutputFiles/toy_$1$2'.root'
    cd $run_dir
    rm -rf temps/$1
}

# fit toys for toy model $1, fit model $2, number of toys $3, signal strength $4
toy_fit(){
    # outputs go in this directory
    mkdir -p temps/nbyn$1$2$4
    cd temps/nbyn$1$2$4
    # fit model2 to toy1
    combine $run_dir/OutputFiles/c_01_test_s$2'.txt' -M FitDiagnostics --toysFile $run_dir/OutputFiles/toy_$1$4'.root' -t $3 --rMin -60 --rMax 60 --robustFit 1
}
# --robustFit 1

temp_cleanup(){
    cp -r temps/* OutputFiles/
    rm -rf temps/* 
}
