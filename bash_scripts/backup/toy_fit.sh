run_dir=$PWD

toy_fit(){
    mkdir -p temps/nbyn$1$2
    cd temps/nbyn$1$2
    # fit model2 to toy1
    combine $run_dir/OutputFiles/c_01_test_s$2'.txt' -M FitDiagnostics --toysFile $run_dir/OutputFiles/toy_$1'.root' -t $3 --rMin -60 --rMax 60 --robustFit 1
}
# --robustFit 1
# $3 num toys

toy_fit_cleanup(){
    cp -r temps/* OutputFiles/
    rm -rf temps/* 
}


# arg1 arg2 = toy, fit
# toy_fit MKLegendre bernstein3 &
