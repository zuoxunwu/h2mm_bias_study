from MakeWorkspaceDatacard import WorkspaceAndDatacardMaker

print('program is running ...')
# Needs the file with the dimu_mass plots created by categorize.cxx
# also needs to know the category you want to make the root file and datacard for
#dir1 = '/home/pq8556/muffin/0303_bias/muPairs_mass/'
#filename = ''
wdm = WorkspaceAndDatacardMaker('muPairs_mass135_165_nb61_rescaled.root', 'c_01_test') #/home/pq8556/muffin/0303_bias/muPairs_mass 
print(wdm.infilename, wdm.category)
wdm.makeShapeWorkspace()
#wdm.makeShapeDatacard()

print('use higgs combine to combine the categories for the net limit, p-value, whatever')
