# By: Javad KAZEM
#
import numpy as np 
import os

'''
(1) This module is developed for extracting the results from Abaqus ODB files

(2) The main script must be executed in Abaqus environment but this module should be imported in the main script.

Example:
import sys
sys.path.append('d://_CL_Python//') # adding the directory to the path
from CL_Abaqus_ODB_Reader import *
CL_ODBR_Say_Hello() # calling say hello function

(3) Be careful. Every time this module is modified, Abaqus should be restarted.

'''
#====================================================================
def CL_ODBR_Say_Hello():
    # This function just prints a hello message
    #
    print('******************')
    print('*** HELLO ODBR ***')
    print('******************')
    return None
#====================================================================
def CL_ODBR_OpenODB(session, FName):
    # this function returns the ODB object
    # session : abaqus session (just available in Abaqus environment)
    # FName   : full path of the ODB file
    #
    # Example: ODB = CL_ODBR_OpenODB(session, ODBFName)
    #
    ODB = session.openOdb(name=FName)
    return ODB
#====================================================================
def CL_ODBR_InsNames(ODB):
    # this function returns a list of instances names
    # ODB : The ODB object
    #
    InsNames = ODB.rootAssembly.instances.keys()
    return InsNames
#====================================================================
def CL_ODBR_StepNames(ODB):
    # this function returns step names as a list of strings
    # ODB : The ODB object
    #
    StepNames = ODB.steps.keys()
    return StepNames
#====================================================================
def CL_ODBR_FramesTime(ODB,StepName):
    # this function returns a 1D array contains the time corresponding to each frame
    # ODB      : The ODB object
    # StepName : (string), the name of the step
    #
    Frames = ODB.steps[StepName].frames
    NF     = len(Frames)
    FTime  = np.zeros(NF)
    for i,f in enumerate(Frames):
        FTime[i] = f.frameValue
    return FTime
#====================================================================
def CL_ODBR_ELM(ODB,InsName):
    # This function returns:
    #       ELM    (2D array) connectivity matrix for each instance
    #       ELabel (1D array) element labels
    #       EType  (list) element types
    #
    # ODB      : The ODB object
    # InsName  : (string), the name of the instance
    #
    Ins    = ODB.rootAssembly.instances[InsName]
    NE     = len(Ins.elements)
    ELM    = np.zeros((NE,30),np.int32)
    ELabel = np.zeros(NE,np.int32)
    EType  = [None]*NE
    NPEmax = 0
    for i,e in enumerate(Ins.elements):
        n = e.connectivity
        NPE = len(n)
        NPEmax = max(NPE,NPEmax)
        ELM[i,0:NPE] = n
        ELabel[i] = e.label
        EType[i] = e.type
    ELM = ELM[:,0:NPEmax]
    return ELM, ELabel, EType
#====================================================================
def CL_ODBR_NOD(ODB,InsName):
    # This function returns:
    #       NOD    : (2D array) Nodal coordinate table as a 2D array
    #       NLabel : (1D array) Node labels
    #
    # ODB      : The ODB object
    # InsName  : (string), the name of the instance
    #
    Ins    = ODB.rootAssembly.instances[InsName]
    NN     = len(Ins.nodes)
    NOD    = np.zeros((NN,3))
    NLabel = np.zeros(NN,np.int32)
    for i,n in enumerate(Ins.nodes):
        NOD[i,:]  = n.coordinates
        NLabel[i] = n.label
    return NOD, NLabel
#====================================================================
def CL_ODBR_FieldOutputNames(ODB,StepName,Frame):
    # This function returnes all field output names
    #
    # ODB       : The ODB object
    # StepName  : (string), the name of the step
    # Frame     : Frame number (-1 for the last frame)
    #
    FO = ODB.steps[StepName].frames[Frame].fieldOutputs
    FNames = FO.keys()
    return FNames
#====================================================================
def CL_ODBR_FieldOutput(ODB, InsName, StepName, Frame, FieldName, SubFieldNames):
    # This function returns the field outputs as a dictionary
    #
    # ODB           : The ODB object
    # InsName       : (string), the name of the instance
    # StepName      : (string), the name of the step
    # Frame         : Frame number (-1 for the last frame)
    # FieldName     : (string) the name of the field (for example: 'S' 'U' 'UT' 'PEEQ')
    # SubFieldNames : ('ALL' or a list of strings) the name of the components (see below).
    #
    Ins  = ODB.rootAssembly.instances[InsName]
    FO   = ODB.steps[StepName].frames[Frame].fieldOutputs[FieldName]
    FO   = FO.getSubset(region=Ins)
    Vals = FO.values
    n    = len(Vals)
    #------------------------
    if SubFieldNames == 'All':
        SubFieldNames = [
                         'conjugateData'       ,
                         'data'                ,
                         'elementLabel'        ,
                         'face'                ,
                         'instance'            ,
                         'integrationPoint'    ,
                         'inv3'                ,
                         'localCoordSystem'    ,
                         'magnitude'           ,
                         'maxInPlanePrincipal' ,
                         'maxPrincipal'        ,
                         'midPrincipal'        ,
                         'minInPlanePrincipal' ,
                         'minPrincipal'        ,
                         'mises'               ,
                         'nodeLabel'           ,
                         'outOfPlanePrincipal' ,
                         'position'            ,
                         'precision'           ,
                         'press'               ,
                         'sectionPoint'        ,
                         'tresca'              ,
                         'type '               ]
    #------------------------
    F = {}
    #------------------------
    f_baseElementType = False
    if 'baseElementType' in SubFieldNames:
        f_baseElementType = True
        F['baseElementType'] = [None]*n
    #------------------------
    f_conjugateData = False
    if 'conjugateData' in SubFieldNames:
        f_conjugateData = True
        F['conjugateData'] = [None]*n
    #------------------------
    f_data = False
    if 'data' in SubFieldNames:
        f_data = True
        F['data'] = [None]*n
    #------------------------
    f_elementLabel = False
    if 'elementLabel' in SubFieldNames:
        f_elementLabel = True
        F['elementLabel'] = [None]*n
    #------------------------
    f_face = False
    if 'face' in SubFieldNames:
        f_face = True
        F['face'] = [None]*n
    #------------------------
    f_instance = False
    if 'instance' in SubFieldNames:
        f_instance = True
    F['instance'] = [None]*n
    #------------------------
    f_integrationPoint = False
    if 'integrationPoint' in SubFieldNames:
        f_integrationPoint = True
        F['integrationPoint'   ] = [None]*n
    #------------------------
    f_inv3 = False
    if 'inv3' in SubFieldNames:
        f_inv3 = True
        F['inv3'] = [None]*n
    #------------------------
    f_localCoordSystem = False
    if 'localCoordSystem' in SubFieldNames:
        f_localCoordSystem = True
        F['localCoordSystem'] = [None]*n
    #------------------------
    f_magnitude = False
    if 'magnitude' in SubFieldNames:
        f_magnitude = True
        F['magnitude'] = [None]*n
    #------------------------
    f_maxInPlanePrincipal = False
    if 'maxInPlanePrincipal' in SubFieldNames:
        f_maxInPlanePrincipal = True
        F['maxInPlanePrincipal'] = [None]*n
    #------------------------
    f_maxPrincipal = False
    if 'maxPrincipal' in SubFieldNames:
        f_maxPrincipal = True
        F['maxPrincipal'] = [None]*n
    #------------------------
    f_midPrincipal = False
    if 'midPrincipal' in SubFieldNames:
        f_midPrincipal = True
        F['midPrincipal'] = [None]*n
    #------------------------
    f_minInPlanePrincipal = False
    if 'minInPlanePrincipal' in SubFieldNames:
        f_minInPlanePrincipal = True
        F['minInPlanePrincipal'] = [None]*n
    #------------------------
    f_minPrincipal = False
    if 'minPrincipal' in SubFieldNames:
        f_minPrincipal = True
        F['minPrincipal'] = [None]*n
    #------------------------
    f_mises = False
    if 'mises' in SubFieldNames:
        f_mises = True
        F['mises'] = [None]*n
    #------------------------
    f_nodeLabel = False
    if 'nodeLabel' in SubFieldNames:
        f_nodeLabel = True
        F['nodeLabel'] = [None]*n
    #------------------------
    f_outOfPlanePrincipal = False
    if 'outOfPlanePrincipal' in SubFieldNames:
        f_outOfPlanePrincipal = True
        F['outOfPlanePrincipal'] = [None]*n
    #------------------------
    f_position = False
    if 'position' in SubFieldNames:
        f_position = True
        F['position'] = [None]*n
    #------------------------
    f_precision = False
    if 'precision' in SubFieldNames:
        f_precision = True
        F['precision'] = [None]*n
    #------------------------
    f_press = False
    if 'press' in SubFieldNames:
        f_press = True
        F['press'] = [None]*n
    #------------------------
    f_sectionPoint = False
    if 'sectionPoint' in SubFieldNames:
        f_sectionPoint = True
        F['sectionPoint'] = [None]*n
    #------------------------
    f_tresca = False
    if 'tresca' in SubFieldNames:
        f_tresca = True
        F['tresca'] = [None]*n
    #------------------------
    f_type = False
    if 'type' in SubFieldNames:
        f_type = True
        F['type'] = [None]*n
    #------------------------
    for i,V in enumerate(Vals):
        if f_baseElementType:
            F['baseElementType'    ][i] = str(V.baseElementType)         if V.baseElementType     is not None else None
        if f_conjugateData:
            F['conjugateData'      ][i] = np.array(V.conjugateData)      if V.conjugateData       is not None else None
        if f_data:
            F['data'               ][i] = np.array(V.data)               if V.data                is not None else None
        if f_elementLabel:
            F['elementLabel'       ][i] = int(V.elementLabel)            if V.elementLabel        is not None else None
        if f_face:
            F['face'               ][i] = int(V.face)                    if V.face                is not None else None
        if f_instance:
            F['instance'           ][i] = str(V.instance.name)           if V.instance.name       is not None else None
        if f_integrationPoint:
            F['integrationPoint'   ][i] = int(V.integrationPoint)        if V.integrationPoint    is not None else None
        if f_inv3:
            F['inv3'               ][i] = float(V.inv3)                  if V.inv3                is not None else None
        if f_localCoordSystem:
            F['localCoordSystem'   ][i] = V.localCoordSystem             if V.localCoordSystem    is not None else None
        if f_magnitude:
            F['magnitude'          ][i] = float(V.magnitude)             if V.magnitude           is not None else None
        if f_maxInPlanePrincipal:
            F['maxInPlanePrincipal'][i] = float(V.maxInPlanePrincipal)   if V.maxInPlanePrincipal is not None else None
        if f_maxPrincipal:
            F['maxPrincipal'       ][i] = float(V.maxPrincipal)          if V.maxPrincipal        is not None else None
        if f_midPrincipal:
            F['midPrincipal'       ][i] = float(V.midPrincipal)          if V.midPrincipal        is not None else None
        if f_minInPlanePrincipal:
            F['minInPlanePrincipal'][i] = float(V.minInPlanePrincipal)   if V.minInPlanePrincipal is not None else None
        if f_minPrincipal:
            F['minPrincipal'       ][i] = float(V.minPrincipal)          if V.minPrincipal        is not None else None
        if f_mises:
            F['mises'              ][i] = float(V.mises)                 if V.mises               is not None else None
        if f_nodeLabel:
            F['nodeLabel'          ][i] = int(V.nodeLabel)               if V.nodeLabel           is not None else None
        if f_outOfPlanePrincipal:
            F['outOfPlanePrincipal'][i] = float(V.outOfPlanePrincipal)   if V.outOfPlanePrincipal is not None else None
        if f_position:
            F['position'           ][i] = str(V.position)                if V.position            is not None else None
        if f_precision:
            F['precision'          ][i] = str(V.precision)               if V.precision           is not None else None
        if f_press:
            F['press'              ][i] = float(V.press)                 if V.press               is not None else None
        if f_sectionPoint:
            F['sectionPoint'       ][i] = int(V.sectionPoint)            if V.sectionPoint        is not None else None
        if f_tresca:
            F['tresca'             ][i] = float(V.tresca)                if V.tresca              is not None else None
        if f_type:
            F['type'               ][i] = str(V.type)                    if V.type                is not None else None
    return F





