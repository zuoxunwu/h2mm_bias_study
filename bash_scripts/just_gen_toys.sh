#!/bin/bash
# Perform bias study
#######################################
# Perform bias study 
# Arguments:
#   $1 config file for each category
#######################################
gen_toys(){
    input1=$1
    # initialization
    unset arr_models
    unset arr_sig_bkg
    unset arr_infile
    unset study_title
    declare -a arr_models
    declare -a arr_sig_bkg
    declare -a arr_infile
    ###################
    # parse config file
    ##################
    let i=0
    while IFS="," read f1 f2; do
        [[ "$f1" = "#".* ]] && continue
        # path for histogram file
        if [ "$f1" = "datafile" ]; then
            echo "the $f1 is $f2"
            arr_infile[0]="$f2"
        fi
        if [ "$f1" = "runmode" ]; then
            echo "the $f1 is $f2"
            RUNMODE=$f2
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
            study_title="$f2" 
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
    echo "config file parsing complete!"
    echo "################"
    sleep 2s

    # create directories
    mkdir -p OutputFiles/${study_title}
    mkdir -p logs/${study_title}
    . bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()
    
    ##########################################
    # toy "data" generation sequence
    ##########################################

    ##########################################
    # Create workspaces for background models
    # Arguments:
    #   $1 infile , $2 model, $3 h_sig, $4 h_bkg, $5 title(category) $6 runmode(whether to use mc or toy as data_obs 
    ##########################################
    for i in "${arr_models[@]}"; do
        python python_files/make_ws_dc.py ${arr_infile[0]} $i ${arr_sig_bkg[0]} ${arr_sig_bkg[1]} ${study_title} mc_to_toys &
    done 
    wait
    echo "workspace creation complete!"
    sleep 2s

    ###############
    # Generate toys
    # Arguments:
    #   toy_model, signal_strength, num of toys
    ###############
    NUM_TOYS=100
    #. bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()
    # toy generation
    for i in "${arr_models[@]}"; do
        for j_ss in {0..1}; do
            for rs in {1..30}; do
		cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
                echo ${cmb_num}
                while [[ ${cmb_num} -gt 40 ]]; do
                  cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
                  sleep 2s
                done
                toy_gen $i $j_ss $NUM_TOYS ${rs} ${study_title} &> logs/${study_title}/log_toy_gen_${i}${j_ss}_seed${rs}.txt &
            done
        done
    done
    wait
    echo "toy generation complete!"
    sleep 2s

}
