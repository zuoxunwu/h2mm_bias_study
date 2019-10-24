import argparse

def main1():
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('model')
    parser.add_argument('h_sig')
    parser.add_argument('h_bkg')
    parser.add_argument('title')
    args = parser.parse_args()
    # workspac and datacard maker
    #from MWD2 import WorkspaceAndDatacardMaker
    #wdm = WorkspaceAndDatacardMaker('InputFiles/StackPlots.root', 'c_01_test', args.model) 
    #from MWD_tth_wh import WorkspaceAndDatacardMaker
    #from MWD_wh_data import WorkspaceAndDatacardMaker
    from MWD_wh_MC import WorkspaceAndDatacardMaker
    wdm = WorkspaceAndDatacardMaker(args.infile, 'c_01_test', args.model, args.h_sig, args.h_bkg) 
    #print(wdm.infilename, wdm.category)
    wdm.makeShapeWorkspace()
    #wdm.makeShapeDatacard()
    return None
   
if __name__ == '__main__':
    main1()
