from MWD2 import WorkspaceAndDatacardMaker
# mcho = 'MKBwz'
#mcho = 'MKPower'
#mcho = 'MKLegendre'
#mcho = 'MKExp'
mcho = 'MKBernstein'
wdm = WorkspaceAndDatacardMaker('InputFiles/StackPlots.root', 'c_01_test', mcho)
wdm.makeShapeWorkspace()
wdm.makeShapeDatacard()

