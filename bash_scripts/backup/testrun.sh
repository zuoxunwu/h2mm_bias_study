
# run bias study for background models  

# program flow
# run_study.sh
# load models to study and data histogram
# 
# create workspaces for different models
# 
# generate toys using workspaces
# 
# fit diagnostic toys using workspaces
# 
# run root script for gaussian fitting
# 
# save numbers to text file

# Loading configuration and generating workspaces for differnt models
# configuration file to load; parsing the text file

input1="Configs/file1.txt"

unset arr_models
declare -a arr_models
let i=0
while IFS="," read f1 f2; do
    [[ "$f1" = "#".* ]] && continue
    # path for histogram file
    if [ "$f1" = "datafile" ]; then
        echo "the $f1 is $f2"
    fi
    # models for background
    if [ "$f1" = "model" ]; then
        echo "the $f1 is $f2"
        arr_models[i]="$f2"
        ((++i))
    fi
    # signal strength
    if [ "$f1" = "signal_strength" ]; then
        echo "the $f1 is $f2"
        signal_strength=$f2
    fi
done < "$input1"
wait
echo "config file parsing complete!"
# sleep 2s
# 
# for i in "${arr_models[@]}"; do
#     python python_files/run_WD_com.py $i &
# done 
# wait
# echo "workspace creation complete!"
# sleep 2s
# 
# 
# . bash_scripts/toy_gen.sh
# for i in "${arr_models[@]}"; do
#     toy_gen $i $signal_strength &
# done
# wait
# echo "toy generation complete!"
# sleep 2s
# . bash_scripts/toy_fit.sh
# for i in "${arr_models[@]}"; do
#     for j in "${arr_models[@]}"; do
#         toy_fit $i $j &
#     done
# done
# wait
# echo "toy fitting complete!"
# sleep 2s
# toy_fit_cleanup
# wait
# 
# 
# rm -f OutputFiles/pulls.txt
# wait
# 
# sleep 2s
# for i in "${arr_models[@]}"; do
#     for j in "${arr_models[@]}"; do
#         python python_files/histo_pull.py $i $j $signal_strength &
#     done
# done
# wait
# 
# sleep 2s
# cat OutputFiles/pulls.txt




unset arr_models
