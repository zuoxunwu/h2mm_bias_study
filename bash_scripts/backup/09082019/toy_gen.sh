run_dir=$PWD

toy_gen(){
    cd temps
    mkdir -p $1
    cd $1
    combine -d ../../OutputFiles/c_01_test_s$1'.txt' -M GenerateOnly --toysFrequentist -t $3 --expectSignal $2 --saveToys
    mv higgsCombineTest.GenerateOnly.mH120.123456.root ../../OutputFiles/toy_$1'.root'
    cd $run_dir
    rm -rf temps/$1
}


# $1 bkg model
# $2 signal strength
# $3 num toys
