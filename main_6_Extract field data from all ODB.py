'''
* This script should be executed in the Abaqus environment

* This script extract the field data from the *.odb file for each case
'''
#---------------------------- Add to path
import sys
sys.path.append('d://_CL_Python//')
#-------------------------------------------------------------------- Import modules
from CL_Abaqus_ODB_Reader import *
import numpy as np 
import os
#-------------------------------------------------------------------- BEGIN
print('='*10 + '> BEGIN <' + '='*10 + '\n')
CL_ODBR_Say_Hello()
#-------------------------------------------------------------------- Options
SimDir     = 'D:\Rolling\Case-2-Two Rollers\DOE-Simulations'       # Simulation directory
ExtDir     = 'D:\Rolling\Case-2-Two Rollers\DOE-Results'           # The directort where the extracted data will be saved
Index_from = 0
Index_to   = 0
InsName    = 'PART-SPECIMEN-1'
StepName   = 'Step-Rolling'
Frame      = -1
#-------------------------------------------------------------------- List of indices
Indices = [i for i in range(Index_from,Index_to+1)]
#-------------------------------------------------------------------- Extract and save the fields
for Index in Indices:
    print('-'*80, 'Loading ODB')
    ODBFName  = os.path.join(SimDir, str(Index), 'Jobnew.odb')
    print('ODBFName:', ODBFName)
    #---------------------------------- open ODB file
    ODB = CL_ODBR_OpenODB(session, ODBFName)
    #---------------------------------- extract the fields
    U    = np.array(CL_ODBR_FieldOutput(ODB, InsName, StepName, Frame, 'U'   ,'data' )['data' ])
    Svm  = np.array(CL_ODBR_FieldOutput(ODB, InsName, StepName, Frame, 'S'   ,'mises')['mises'])
    PEEQ = np.array(CL_ODBR_FieldOutput(ODB, InsName, StepName, Frame, 'PEEQ','data' )['data' ])
    #---------------------------------- save the fields
    np.savez_compressed(os.path.join(ExtDir, 'Specimen-U-'   +str(Index)+'.npz'), U   )
    np.savez_compressed(os.path.join(ExtDir, 'Specimen-Svm-' +str(Index)+'.npz'), Svm )
    np.savez_compressed(os.path.join(ExtDir, 'Specimen-PEEQ-'+str(Index)+'.npz'), PEEQ)
#--------------------------------------------------------------------
print('='*10 + '> END <' + '='*10 + '\n')


