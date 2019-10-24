alias combine-gen='combine c_01_test_s.txt -M GenerateOnly -S 0 -t 1000 --expectSignal 1 --saveToys'
alias combine-diag='combine -d c_01_test_s.txt -M FitDiagnostics --toysFile higgsCombineTest.GenerateOnly.mH120.123456.root -t 1000'

combine-fitdiag(){
    combine -d c_01_test_s.txt -M FitDiagnostics --toysFile "$1" -t 1000 --rMin -20 --rMax 20

}
