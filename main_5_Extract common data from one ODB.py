'''
* This script should be executed in the Abaqus environment

* this script extract common data from the first sample of the DOE

'''

import numpy as np
import sys
sys.path.append('d://_CL_Python//')
from CL_Abaqus_ODB_Reader import *
CL_ODBR_Say_Hello()


#---------------------------------------------------------- BEGIN
print('='*10 + '> BEGIN <' + '='*10 + '\n')
#---------------------------------------------------------- Options
ExtDir     = 'D:\Rolling\Case-2-Two Rollers\DOE-Results'           # The directort where the extracted data will be saved
ODBDir     = 'D:\Rolling\Case-2-Two Rollers\DOE-Simulations\\0'     # The directory contains ODB file
print(ODBDir)
ODBFName   = 'Jobnew.odb'                                # Name of the ODB file
InsName1   = 'PART-SPECIMEN-1'
InsName2   = 'PART-ROLLER-VERTICAL-1'
InsName3   = 'PART-ROLLER-HORIZONTAL-1'
StepName   = 'Step-Rolling'
Frame      = -1                                       # frame number (-1 means the last frame)
#---------------------------------------------------------- open ODB file
ODBFName = os.path.join(ODBDir, ODBFName)
print('-'*80 + ' Reading ODB ...')
print(ODBFName)
ODB = CL_ODBR_OpenODB(session, ODBFName)
#---------------------------------------------------------- print all instance names
print('-'*80 + ' Instance names:')
print(CL_ODBR_InsNames(ODB))
#---------------------------------------------------------- print all step names
print('-'*80 + ' Step names:')
print(CL_ODBR_StepNames(ODB))
#---------------------------------------------------------- Nodal coordinate tables
print('-'*80 + ' Reading nodal coordinates')
NOD1,_    = CL_ODBR_NOD(ODB,InsName1)
NOD2,_    = CL_ODBR_NOD(ODB,InsName2)
NOD3,_    = CL_ODBR_NOD(ODB,InsName3)
#---------------------------------------------------------- Connectivity tables
print('-'*80 + ' Reading element connectivities')
ELM1,_,_  = CL_ODBR_ELM(ODB,InsName1)
ELM2,_,_  = CL_ODBR_ELM(ODB,InsName2)
ELM3,_,_  = CL_ODBR_ELM(ODB,InsName3)
#---------------------------------------------------------- save common data
print('-'*80 + ' Saving data')
np.savez_compressed(os.path.join(ExtDir,'Specimen-NOD.npz'), NOD1)   # Nodal coordinates
np.savez_compressed(os.path.join(ExtDir,'Roll-Hor-NOD.npz'), NOD2)   # Nodal coordinates
np.savez_compressed(os.path.join(ExtDir,'Roll-Ver-NOD.npz'), NOD3)   # Nodal coordinates
np.savez_compressed(os.path.join(ExtDir,'Specimen-ELM.npz'), ELM1)   # Connectivity table
np.savez_compressed(os.path.join(ExtDir,'Roll-Hor-ELM.npz'), ELM2)   # Connectivity table
np.savez_compressed(os.path.join(ExtDir,'Roll-Ver-ELM.npz'), ELM3)   # Connectivity table
#---------------------------------------------------------- END
print('='*10 + '> END <' + '='*10 + '\n')





