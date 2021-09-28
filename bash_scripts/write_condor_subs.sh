#!/bin/bash
# Perform bias study
#######################################
# Perform bias study 
# Arguments:
#   $1 config file for each category
#######################################
write_subs(){
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

    NUM_TOYS=100
    N_SEED=30

    # create directories
    mkdir -p OutputFiles/${study_title}
    mkdir -p logs/${study_title}
    . bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()
    
    if [ "${RUNMODE}" = "mc_to_toys" ]; then
        echo "toy gen only so it stops here"
    else
        echo "fitting toys."
        ##########
        # fit toys
        # Arguments:
        # toy_model, fit_model, num_toys, signal_strength
        ##########
	python job_subs/PrepareSub.py ${study_title}
        for i in "${arr_models[@]}"; do
            for j in "${arr_models[@]}"; do
                for k in {0..1}; do
		    python job_subs/GenerateSubs.py $i $j $NUM_TOYS $k $N_SEED ${study_title}
                done
            done
        done

    fi
}
