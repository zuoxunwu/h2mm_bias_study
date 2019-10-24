#!/bin/bash
#
# Perform bias study

# imported 
# toy_things.sh


#######################################
# Perform bias study 
# Arguments:
#   $1 config file for each category
#######################################
run_study_pull(){
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
    # 
    ##################

    echo "################"
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
    wait
    echo "config file parsing complete!"
    echo "################"
    sleep 2s

    # create directories
    mkdir -p OutputFiles/${study_title}
    mkdir -p logs/${study_title}
    
    ##########################################
    # Create workspaces for background models
    # Arguments:
    #   $1 infile , $2 model, $3 h_sig, $4 h_bkg, $5 title(category) $6 runmode(whether to use mc or toy as data_obs 
    ##########################################
    for i in "${arr_models[@]}"; do
        python python_files/make_ws_dc.py ${arr_infile[0]} $i ${arr_sig_bkg[0]} ${arr_sig_bkg[1]} ${study_title} ${RUNMODE} &
    done 
    wait
    echo "workspace creation complete!"
    sleep 2s

    ###############
    # Generate toys
    # Arguments:
    #   toy_model, signal_strength, num of toys
    ###############
    NUM_TOYS=900
    . bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()
    # toy generation
    for i in "${arr_models[@]}"; do
        for j_ss in {0..1}; do
            for rs in {1..3}; do
                toy_gen $i $j_ss $NUM_TOYS ${rs} ${study_title} &> logs/${study_title}/log_toy_gen_${i}${j_ss}_seed${rs}.txt &
            done
        done
    done
    wait
    echo "toy generation complete!"
    sleep 2s

    if [ "${RUNMODE}" = "mc_to_toys" ]; then
        echo "toy gen only so it stops here"
    else
        echo "what's going on here?"
        ##########
        # fit toys
        # Arguments:
        # toy_model, fit_model, num_toys, signal_strength
        ##########
        for i in "${arr_models[@]}"; do
            for j in "${arr_models[@]}"; do
                for k in {0..1}; do
                    for rs in {1..3}; do
                        echo $i $j $k
                        cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
                        echo ${cmb_num}
                        while [[ ${cmb_num} -gt 20 ]]; do
                            cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')
                            sleep 2s
                        done
                        toy_fit $i $j $NUM_TOYS $k ${rs} ${study_title} &> logs/${study_title}/log_toy_fit_${i}_${j}_${k}_seed${rs}.txt &
                    done
                done
            done
        done
        wait
        #######################
        # hadd different seeds
        #######################
        echo "hadd different seeds"
        for i in "${arr_models[@]}"; do
            for j in "${arr_models[@]}"; do
                for k in {0..1}; do
                    toy_fit_hadd $i $j $NUM_TOYS $k ${study_title} &> logs/${study_title}/log_toy_fit_hadd_${i}_${j}_${k}.txt &
                done
            done
        done
        wait
        echo "toy fitting complete!"
        sleep 2s
        temp_cleanup ${study_title}
        wait
        rm -f OutputFiles/pulls_${study_title}0.txt
        rm -f OutputFiles/pulls_${study_title}1.txt
        wait

        ###################
        # pull distribution
        # Arguments:
        #   toy_model, fit_model, signal_strength, title
        ###################
        for i in "${arr_models[@]}"; do
            for j in "${arr_models[@]}"; do
                for k_ssf in {0..1}; do
                    python python_files/histo_pull.py $i $j $k_ssf ${study_title} &
                done
            done
        done
        wait
        sleep 2s
        echo "pulls for signal strength 0"
        cat OutputFiles/pulls_${study_title}0.txt
        echo "pulls for signal strength 1"
        cat OutputFiles/pulls_${study_title}1.txt

        ##########################
        # Plot the bias scan table
        # Arguments:
        #   pull_values.txt files
        # Produce:
        #   table.png
        ##########################
        python python_files/create_pull_table.py 
        
    fi
}
