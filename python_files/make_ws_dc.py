import argparse

def main1():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('model')
    parser.add_argument('h_sig')
    parser.add_argument('h_bkg')
    parser.add_argument('title')
    parser.add_argument('runmode')
    args = parser.parse_args()

    # create workspace and datacard
    #from MWD_wh_MC import WorkspaceAndDatacardMaker
    from MWD_wh_cfg import WorkspaceAndDatacardMaker
    wdm = WorkspaceAndDatacardMaker(args.infile, 'c_01_test', args.model, args.h_sig, args.h_bkg, args.title, args.runmode) 
    wdm.makeShapeWorkspace()
    return None
   
if __name__ == '__main__':
    main1()
