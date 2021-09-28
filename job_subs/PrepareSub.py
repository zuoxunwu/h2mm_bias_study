import argparse
import sys
import os
from shutil import rmtree

def main1():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('study_title')
    args = parser.parse_args()

    stitle = args.study_title


    if os.path.exists('job_subs/scripts/%s'%stitle): rmtree('job_subs/scripts/%s'%stitle)
    if os.path.exists('job_subs/condor/%s'%stitle):  rmtree('job_subs/condor/%s'%stitle)
    if os.path.exists('condor_out/%s'%stitle):       rmtree('condor_out/%s'%stitle)

    os.makedirs('job_subs/scripts/%s'%stitle)
    os.makedirs('job_subs/condor/%s'%stitle)
    os.makedirs('condor_out/%s'%stitle)
    os.makedirs('condor_out/%s/out'%stitle)
    os.makedirs('condor_out/%s/log'%stitle)
    os.makedirs('condor_out/%s/err'%stitle)

    sub_all = open('sub_all_%s.sh' %stitle, 'w')
    sub_all.write('pwd_cmd="/bin/pwd"\n')
    sub_all.write("run_dir=`${pwd_cmd}`\n")
    sub_all.write("\n")
    sub_all.write("\n")


    return None
   
if __name__ == '__main__':
    main1()
