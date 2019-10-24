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

input1="Configs/h2mumu_inclusive.txt"

# initialization
unset arr_models
unset arr_sig_bkg
unset arr_infile
declare -a arr_models
declare -a arr_sig_bkg
declare -a arr_infile

# parse config file
let i=0
while IFS="," read f1 f2; do
    [[ "$f1" = "#".* ]] && continue
    # path for histogram file
    if [ "$f1" = "datafile" ]; then
        echo "the $f1 is $f2"
        arr_infile[0]="$f2"
    fi
    # histogram name for signal
    if [ "$f1" = "signal" ]; then
        echo "the $f1 is $f2"
        arr_sig_bkg[0]="$f2"
    fi
    # histogram name for background
    if [ "$f1" = "background" ]; then
        echo "the $f1 is $f2"
        arr_sig_bkg[1]="$f2"
    fi
    # title of this analysis
    if [ "$f1" = "title" ]; then
        echo "the $f1 is $f2"
        arr_sig_bkg[2]="$f2"
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
sleep 2s

# workspace creation for background models
for i in "${arr_models[@]}"; do
    python python_files/run_WD_com.py ${arr_infile[0]} $i ${arr_sig_bkg[0]} ${arr_sig_bkg[1]} &
done 
wait
echo "workspace creation complete!"
sleep 2s

## PART - toys
NUM_TOYS=1000
. bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()
# toy generation
for i in "${arr_models[@]}"; do
    for j_ss in {0..1}; do
        toy_gen $i $j_ss $NUM_TOYS &> toy_gen_${i}${j_ss}.txt &
    done
done
wait
echo "toy generation complete!"
sleep 2s

# toy fitting
for i in "${arr_models[@]}"; do
    for j in "${arr_models[@]}"; do
        for k in {0..1}; do
            echo $i $j $k
            cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
            echo ${cmb_num}
            while [ ${cmb_num} -gt 20 ]; do
                cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
                sleep 2s
            done
            toy_fit $i $j $NUM_TOYS $k &> fit_log_${i}_${j}_${k}.txt &
        done
    done
done
wait
echo "toy fitting complete!"
sleep 2s
temp_cleanup
wait
rm -f OutputFiles/pulls_${arr_sig_bkg[2]}0.txt
rm -f OutputFiles/pulls_${arr_sig_bkg[2]}1.txt
wait
# pull distribution
for i in "${arr_models[@]}"; do
    for j in "${arr_models[@]}"; do
        for k_ssf in {0..1}; do
            python python_files/histo_pull.py $i $j $k_ssf ${arr_sig_bkg[2]} &
        done
    done
done
wait
sleep 2s
echo "pulls for signal strength 0"
cat OutputFiles/pulls_${arr_sig_bkg[2]}0.txt
echo "pulls for signal strength 1"
cat OutputFiles/pulls_${arr_sig_bkg[2]}1.txt
