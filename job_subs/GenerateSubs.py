import argparse

def main1():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('model1')
    parser.add_argument('model2')
    parser.add_argument('NUM_TOYS')
    parser.add_argument('sig')
    parser.add_argument('N_SEED')
    parser.add_argument('study_title')
    args = parser.parse_args()

    m1     = args.model1
    m2     = args.model2
    ntoy   = args.NUM_TOYS
    sig    = args.sig
    nseed  = args.N_SEED
    stitle = args.study_title



    script = open('job_subs/scripts/%s/fit_%s_%s_%s_%s.sh' %(stitle,stitle,m1,m2,sig), 'w')
    script.write('#!/bin/bash\n\n')
    script.write('run_dir="/afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/src/bias_study"\n')
    script.write('cd ${run_dir}\n')
    script.write('eval `scramv1 runtime -sh`\n')
    script.write('\n')
    script.write('\n')
    script.write('. bash_scripts/toy_things.sh # load toy_gen(), toy_fit(), temp_cleanup()\n')
    script.write('\n')
    script.write('for rs in {1..%s}; do\n' %nseed)
    script.write("    cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')\n")
    script.write("    echo ${cmb_num}\n")
    script.write("    while [[ ${cmb_num} -gt 3 ]]; do\n")
    script.write("      cmb_num=$(ps -o comm|sort|uniq -c | awk '/combine/ {print $1}')\n")
    script.write("      sleep 2s\n")
    script.write("    done\n")
    script.write("    toy_fit %s %s %s %s ${rs} %s\n" %(m1, m2, ntoy, sig, stitle))
    script.write("done\n")
    script.write("wait\n")
    script.write("\n")


    submit = open('job_subs/condor/%s/sub_%s_%s_%s_%s.sub' %(stitle,stitle,m1,m2,sig), 'w')
    submit.write("run_dir = /afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/src/bias_study\n")
    submit.write("out_dir = /afs/cern.ch/work/x/xzuo/combine/CMSSW_8_1_0/src/bias_study/condor_out/%s\n" %stitle )
    submit.write("RequestCpus = 4\n")
    submit.write("executable      = $(run_dir)/job_subs/scripts/%s/fit_%s_%s_%s_%s.sh\n" %(stitle,stitle,m1,m2,sig))
    submit.write("output          = $(out_dir)/out/sub_%s_%s_%s_%s.out\n" %(stitle,m1,m2,sig))
    submit.write("error           = $(out_dir)/err/sub_%s_%s_%s_%s.err\n" %(stitle,m1,m2,sig))
    submit.write("log             = $(out_dir)/log/sub_%s_%s_%s_%s.log\n" %(stitle,m1,m2,sig))
    submit.write("+MaxRuntime = 36000\n")
    submit.write("queue\n")


    sub_all = open('sub_all_%s.sh' %stitle, 'a')
    sub_all.write("condor_submit ${run_dir}/job_subs/condor/%s/sub_%s_%s_%s_%s.sub\n" %(stitle,stitle,m1,m2,sig))


    return None
   
if __name__ == '__main__':
    main1()
