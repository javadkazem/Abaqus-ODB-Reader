'''
* This script should be executed in the Abaqus environment

* this script extract some basic informations from one ODB file

'''

import numpy as np
import sys
sys.path.append('d://_CL_Python//') # add the directory to the path
from CL_Abaqus_ODB_Reader import *
CL_ODBR_Say_Hello()

#---------------------------------------------------------- BEGIN
print('='*10 + '> BEGIN <' + '='*10 + '\n')
#---------------------------------------------------------- Options
ODBDir     = 'D:\Rolling'                                # The directory contains ODB file
ODBFName   = 'Jobnew.odb'                                # Name of the ODB file
#---------------------------------------------------------- open ODB file
ODBFName = os.path.join(ODBDir, ODBFName)
print('-'*80 + ' ODB File name:')
print(ODBFName)
ODB = CL_ODBR_OpenODB(session, ODBFName)
#---------------------------------------------------------- All instance names
InsNames = CL_ODBR_InsNames(ODB)
print('-'*80 + ' Instance names:')
for InsName in InsNames:
    print(InsName)
#---------------------------------------------------------- All step names
StepNames = CL_ODBR_StepNames(ODB)
print('-'*80 + ' Step names:')
for StepName in StepNames:
    print(StepName)
#---------------------------------------------------------- All field output names for all steps
print('-'*80 + ' Field outputs:')
for StepName in StepNames:
    FieldOutputNames = CL_ODBR_FieldOutputNames(ODB,StepName,-1)
    print('-'*20 + ' ' + StepName)
    for FieldOutputName in FieldOutputNames:
        print(FieldOutputName)
#---------------------------------------------------------- END
print('='*10 + '> END <' + '='*10 + '\n')





