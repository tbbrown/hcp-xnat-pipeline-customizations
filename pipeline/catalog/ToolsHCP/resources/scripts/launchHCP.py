'''
Created on Dec 6, 2013

@author: Mohana Ramaratnam (based on script - getPipelineParamsRun.py by Tony Wilson)
'''
import argparse
import datetime
import os
import random
import socket
import subprocess
import sys
import time

import xml.etree.ElementTree as ET

import numpy

from workflow import Workflow
from parameters import XNATPipelineParameters
from pyHCP import pyHCP, getHCP, writeHCP




#===============================================================================
# Description
#===============================================================================
# This script will generate the parameters required to launch the MPP pipeline
# Based on the inputs. 
# This script would work against DB. 


#===============================================================================
# PARSE INPUT
#===============================================================================
# Examples:
#python launchHCP.py -User USER_NAME -Password PASSWORD_HERE -LaunchStructural 1 -LaunchFunctional 1 -LaunchDiffusion 1 -LaunchTaskAnalysis 0 -LaunchICAAnalysis 0 -LaunchMPP 1 -Launch 1 -Subjects 100307 -Server https://db.humanconnectome.org -Project PipelineTest -Compute CHPC -Shadow 1
#
#OLD_USAGE
#
#
#===============================================================================
parser = argparse.ArgumentParser(description="Script to generate proper command for XNAT pipeline launching ...")

# MANDATORY....
parser.add_argument("-User", "--User", dest="User", default=None, type=str)
parser.add_argument("-Password", "--Password", dest="Password", default=None, type=str)
parser.add_argument("-LaunchStructural", "--LaunchStructural", dest="launchStructural", default='1', type=int)
parser.add_argument("-LaunchFunctional", "--LaunchFunctional", dest="launchFunctional", default='1', type=int)
parser.add_argument("-LaunchDiffusion", "--LaunchDiffusion", dest="launchDiffusion", default='1', type=int)
parser.add_argument("-LaunchTaskAnalysis", "--LaunchTaskAnalysis", dest="launchTaskAnalysis", default='0', type=int)
parser.add_argument("-LaunchICAAnalysis", "--LaunchICAAnalysis", dest="launchICAAnalysis", default='0', type=int)
parser.add_argument("-LaunchMPP", "--LaunchMPP", dest="launchMPP", default='0', type=int)

parser.add_argument("-Subjects", "--Subjects", dest="Subjects", default='00', type=str)
parser.add_argument("-Server", "--Server", dest="Server", default='http://hcpi-dev-cuda00.nrg.mir/', type=str)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument("-FunctSeries", "--FunctSeries", dest="FunctSeries", default=None, type=str)
# END MANDATORY....
parser.add_argument("-Project", "--Project", dest="Project", default='HCP_Phase2', type=str)
parser.add_argument("-Shadow", "--Shadow", dest="Shadow", default=None, type=str)
parser.add_argument("-Build", "--Build", dest="Build", default=None, type=str)
parser.add_argument("-SleepTime", "--SleepTIme", dest="SleepTime", default=3, type=int)
parser.add_argument("-Compute", "--Compute", dest="Compute", default='NRG', type=str)

# FOR SAFETY...
parser.add_argument("-Launch", "--Launch", dest="Launch", default='0', type=int)


args = parser.parse_args()
#MANDATORY....
User = args.User
Password = args.Password

LaunchStructural=args.launchStructural
LaunchFunctional=args.launchFunctional
LaunchDiffusion=args.launchDiffusion
LaunchTask=args.launchTaskAnalysis
LaunchICA=args.launchICAAnalysis
LaunchMPP=args.launchMPP

Subjects = args.Subjects
Server = args.Server
FunctSeries = args.FunctSeries

#END MANDATORY....START ALT
Project = args.Project
Shadow = args.Shadow
Build = args.Build
Compute = args.Compute
Launch = args.Launch
SleepTime = args.SleepTime

dbStr = 'hcpdb'
JobSubmitter = '/data/%s/pipeline/bin/schedule ' % (dbStr)
PipelineLauncher = '/data/%s/pipeline/bin/XnatPipelineLauncher ' % (dbStr)

#===============================================================================
# Pipeline Names
#===============================================================================
structuralPipelineName = 'StructuralHCP/StructuralHCP.xml'
functionalPipelineName = 'FunctionalHCP/FunctionalHCP.xml'
diffusionPipelineName = 'DiffusionHCP/DiffusionHCP.xml'
taskPipelineName = 'TaskfMRIHCP/TaskfMRIHCP.xml'
icaPipelineName = ''
mppPipelineName = 'MPP/MPP.xml'
Pipeline = mppPipelineName



#===============================================================================
# STATIC PARMS...
#===============================================================================
SupressNotify = '-supressNotification '

DataTypeStr = 'xnat:mrSessionData'
DataType = '-dataType %s ' % (DataTypeStr)
NotifyUserStr = 'hilemanm@mir.wustl.edu'
NotifyAdminStr = 'db-admin@humanconnectome.org'
MailHostStr = 'mail.nrg.wustl.edu'
UserFullNameStr = 'MPPUser'
XnatServerStr = 'ConnectomeDB'

NotifyUser = ' -notify %s ' % (NotifyUserStr) 
NotifyAdmin = ' -notify %s ' % (NotifyAdminStr)
MailHost = ' -parameter mailhost=%s ' % (MailHostStr)
UserEmail = ' -parameter useremail=%s ' % (NotifyUserStr)
UserFullName = ' -parameter userfullname=%s ' % (UserFullNameStr)
XnatServer = ' -parameter xnatserver=%s ' % (XnatServerStr)
AdminEmail = ' -parameter adminemail=%s' % (NotifyAdminStr)



#===============================================================================
# Functional Types...
#===============================================================================
   
FunctionalRoots = ['tfMRI_LANGUAGE', 'tfMRI_SOCIAL', 'tfMRI_RELATIONAL', 'tfMRI_MOTOR', 'tfMRI_GAMBLING', 'tfMRI_WM', 'tfMRI_EMOTION']


#===============================================================================
# pyHCP INTERFACE...
#===============================================================================
pyHCP = pyHCP(User, Password, Server)
getHCP = getHCP(pyHCP)
getHCP.Project = Project
#===============================================================================

SubjectsList = Subjects.split(',')
if (Shadow != None):
    ShadowList = Shadow.split(',')
else:
    ShadowList = ('')
    
if (Build != None) and (Build != 'ssd'):
    BuildList = Build.split(',')
elif(Build == 'ssd'):
    BuildList = Build
else:
    BuildList = ('')
    
#===============================================================================
# Set up ShadowArray and BuildArray...
#===============================================================================
ShadowArray = map(str, (numpy.tile( map(int, ShadowList), (int(numpy.ceil(len(SubjectsList))), 1) ).ravel()))
random.shuffle(ShadowArray)

BuildArray = numpy.tile(BuildList, (numpy.ceil(len(SubjectsList))))

    
PipelineSubString = None
    
UsableList = ['good', 'excellent', 'usable', 'undetermined']



linIdx = 0
BuildIdx = 0
ShadowIdx = 0
FunctionalN = 0
for h in xrange(0, len(SubjectsList)): 
    getHCP.Subject = SubjectsList[h]
    SubjectSessions = getHCP.getSubjectSessions()
    
    # find correct session...
    for i in xrange(0, len(SubjectSessions.get('Sessions'))):
        getHCP.Session = SubjectSessions.get('Sessions')[i]
        sessionMeta = getHCP.getSessionMeta()
        if (FunctSeries != None) and (FunctSeries in sessionMeta.get('Series')):
            break
        else: 
            try:
                getHCP.Session = SubjectSessions.get('Sessions')[SubjectSessions.get('Types').index(PipelineSubString[0])]
            except:
                break
            
    sessionMeta = getHCP.getSessionMeta()
    seriesList = sessionMeta.get('Series')
    typeList = sessionMeta.get('Types')
    idList = sessionMeta.get('IDs')
    qualityList = sessionMeta.get('Quality')
    
    if (Build == 'hds'):
        BuildDirRoot = '/data/%s/build_hds/%s/' % (dbStr, Project)
    elif (Build == 'sds'):
        BuildDirRoot = '/data/%s/build_sds/%s/' % (dbStr, Project)
    else:
        BuildDirRoot = '/data/%s/build/%s/' % (dbStr, Project)
        
#===============================================================================
# Params XML...
#===============================================================================
    Parameters=XNATPipelineParameters()

    launcherHCPid = ' -id %s ' % sessionMeta.get('XNATID')[0]
    launcherUser = ' -u %s ' % User 
    launcherPassword = ' -pwd %s ' % Password 
    launcherLabel = getHCP.Session
    launcherExternalProject = ' -project %s ' % Project
    launcherProject = Project
    launcherSubject =  getHCP.Subject
    launcherXnatId = sessionMeta.get('XNATID')[0]
    launcherSession = getHCP.Session
    
    Parameters.addUniqueParameter('xnat_id',sessionMeta.get('XNATID')[0])
    Parameters.addUniqueParameter('subject',getHCP.Subject)
    Parameters.addUniqueParameter('sessionId',getHCP.Session)

    sTime = time.time()
    currBuildDir = BuildDirRoot + str(numpy.asarray(round(sTime), dtype=numpy.uint64)) + '_' + getHCP.Subject

    BuildDir = ' -parameter builddir=%s ' % (currBuildDir)

    if sys.platform == 'win32':
        ParameterFilePath='%s\%s.xml' % (BuildDirRoot,getHCP.Subject)
    else:
        ParameterFilePath='%s/%s.xml' % (currBuildDir,getHCP.Subject)
        
    #=======================================================================
    # Shadow server stuff...
    # TODO: Figure out how CHPC shadows will be handled...
    #=======================================================================
    if (socket.gethostname() == 'intradb.humanconnectome.org') and (Shadow != None):
        Host = ' -host http://intradb-shadow%s.nrg.mir:8080 '  % ShadowArray[i] 
        ShadowIdx += 1
    elif ((socket.gethostname() == 'db.humanconnectome.org') or (socket.gethostname() == 'hcpx-fs01.nrg.mir')) and (Shadow != None):
        Host = ' -host http://db-shadow%s.nrg.mir:8080 ' % ShadowArray[ShadowIdx]
        ShadowIdx += 1
    elif (Shadow != None):
        Host = '-host http://db-shadow%s.nrg.mir:8080 ' % ShadowArray[ShadowIdx]
        ShadowIdx += 1
    else: 
        Host = ' -host %s ' % (pyHCP.Server)

                
    #===============================================================================
    # DiffusionHCP....
    #===============================================================================
    if (LaunchDiffusion == 1):
        #===================================================================
        # grab a dummy scan id to feed to XML if scan does not exist.  XML must have scan id, else it will break...
        #===================================================================
        DummyScanId = sessionMeta.get('IDs')[0]
        EchoSpacingList = list()
        PhaseEncodingDirList = list() 

        
        # if intradb...
        if (dbStr == 'intradb'):
            DiffusionSeriesList = ['DWI_RL_dir95','DWI_RL_dir96','DWI_RL_dir97','DWI_LR_dir95','DWI_LR_dir96','DWI_LR_dir97']
        elif (dbStr == 'hcpdb'):
            DiffusionSeriesList = ['DWI_dir95_RL','DWI_dir96_RL','DWI_dir97_RL','DWI_dir95_LR','DWI_dir96_LR','DWI_dir97_LR']
        
        DiffusionScanIdList = ['RL_1ScanId', 'RL_2ScanId', 'RL_3ScanId', 'LR_1ScanId', 'LR_2ScanId', 'LR_3ScanId']
        DiffusionScanIdDict = {'RL_1ScanId' : None, 'RL_2ScanId' : None, 'RL_3ScanId' : None, 'LR_1ScanId' : None, 'LR_2ScanId' : None, 'LR_3ScanId' : None}
        DiffusionDirList = ['RL_Dir1', 'RL_Dir2', 'RL_Dir3', 'LR_Dir1', 'LR_Dir2', 'LR_Dir3']
        DiffusionDirDict = {'RL_Dir1' : '95', 'RL_Dir2' : '96', 'RL_Dir3' : '97', 'LR_Dir1' : '95', 'LR_Dir2' : '96', 'LR_Dir3' : '97' }
        
#            DiffusionSeriesIntersectList = list(set(DiffusionSeriesList) & set(SeriesList))


        for j in xrange(0, len(DiffusionSeriesList)):
            currDiffDesc = DiffusionSeriesList[j]
            if (sessionMeta.get('Series').count(currDiffDesc) > 0):
                currDiffIdx = sessionMeta.get('Series').index(currDiffDesc)
                currScanId = sessionMeta.get('IDs')[currDiffIdx]
                currQuality = sessionMeta.get('Quality')[currDiffIdx]
                getHCP.Scan = currScanId
                scanParms = getHCP.getScanParms()
                scanMeta = getHCP.getScanMeta()
                
                EchoSpacingList.append(float(scanParms.get('EchoSpacing')) * 1.0e+3)
                PhaseEncodingDirList.append(scanParms.get('PhaseEncodingDir'))
                
                # ScanIdDict['LR_2ScanId'] = '-parameter LR_2ScanId=%s ' % str(currScanId)
                if (currQuality in UsableList):
#                    DiffusionScanIdDict[DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)]] = '-parameter %s=%s ' % (DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)], currScanId)
                    DiffusionScanIdDict[DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)]] = '%s' % (currScanId)
                else:
#                    DiffusionScanIdDict[DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)]] = '-parameter %s=%s ' % (DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)], DummyScanId)
#                    DiffusionDirDict[DiffusionDirList[DiffusionSeriesList.index(currDiffDesc)]] = 'EMPTY'
                    DiffusionScanIdDict[DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)]] = '%s' % (DummyScanId)
                    DiffusionDirDict[DiffusionDirList[DiffusionSeriesList.index(currDiffDesc)]] = 'EMPTY'
                
            else:
                DiffusionScanIdDict[DiffusionScanIdList[DiffusionSeriesList.index(currDiffDesc)]] = '%s' % (DummyScanId)
                DiffusionDirDict[DiffusionDirList[DiffusionSeriesList.index(currDiffDesc)]] = 'EMPTY'
        
        EchoSpacing = '%s' % (sum(EchoSpacingList) / float(len(EchoSpacingList)))
 
         # 1 for RL/LR phase encoding and 2 for AP/PA phase encoding
        PhaseEncodingDir = '1'          
 
        Parameters.addUniqueParameter('launchDiffusion','1')
        Parameters.addUniqueParameter('diffusion_EchoSpacing',EchoSpacing)
        Parameters.addUniqueParameter('diffusion_PhaseEncodingDir',PhaseEncodingDir)

        #Make a list of keys and values from the DiffusionDirDict
    
        Parameters.addListParameters('diffusion_DiffusionDirDictNames',DiffusionDirDict.keys())
        Parameters.addListParameters('diffusion_DiffusionDirDictValues',DiffusionDirDict.values())

        #Make a list of keys and values from the DiffusionScanIdDict
        Parameters.addListParameters('diffusion_DiffusionScanDictNames',DiffusionScanIdDict.keys())
        Parameters.addListParameters('diffusion_DiffusionScanDictValues',DiffusionScanIdDict.values())
            
    else:
          Parameters.addUniqueParameter('launchDiffusion','0')

    #=======================================================================
    # StructuralHCP
    #=======================================================================
    if (LaunchStructural == 1):
            
            PathMatch = list()
            ScanIdList = list()
            StructResources = ['T1w_MPR1_unproc', 'T1w_MPR2_unproc', 'T2w_SPC1_unproc', 'T2w_SPC2_unproc']
            getHCP.Resource = StructResources[0]
            resourceMeta = getHCP.getSubjectResourceMeta()
            

            StructuralSeriesDescDict = {'T1w_MPR1' : 'T1w_MPR1', 'T1w_MPR2' : 'T1w_MPR2', 'T2w_SPC1' : 'T2w_SPC1', 'T2w_SPC2' : 'T2w_SPC2'}
            StructuralSeriesDescScanIdDict = {'T1w_MPR1' : None, 'T1w_MPR2' : None, 'T2w_SPC1' : None, 'T2w_SPC2' : None}
            StructuralSeriesQualityDict = {'T1w_MPR1' : None, 'T1w_MPR2' : None, 'T2w_SPC1' : None, 'T2w_SPC2' : None}
            StructuralSeriesList = ['T1w_MPR1', 'T1w_MPR2', 'T2w_SPC1', 'T2w_SPC2']
            

            # grab the fieldmap ids...
            try:
                fieldmapMagIdx = seriesList.index('FieldMap_Magnitude')
                filedmapPhaIdx = seriesList.index('FieldMap_Phase')
            except:
                fieldmapMagIdx = 0
                filedmapPhaIdx = 0
            
            if (typeList[fieldmapMagIdx] == 'FieldMap') and (qualityList[fieldmapMagIdx] in UsableList): 
                MagScanId = idList[fieldmapMagIdx]
                getHCP.Scan = MagScanId
                magScanParms = getHCP.getScanParms()
            else:
                MagScanId = 1
                magScanParms = {'GEFieldMapGroup': 'NA'}
                
            if (typeList[filedmapPhaIdx] == 'FieldMap') and (qualityList[filedmapPhaIdx] in UsableList):
                PhaScanId = idList[filedmapPhaIdx]
                getHCP.Scan = PhaScanId
                phaScanParms = getHCP.getScanParms()
            else:
                PhaScanId = 1
                phaScanParms = {'GEFieldMapGroup': 'NA'}
                
                    
            # collect quality, series descriptions, and scan ids...
            for j in xrange(0, len(seriesList)):
                currSeriesDesc = seriesList[j]
                currTypeList = typeList[j]
                currQuality = qualityList[j]
                if (currSeriesDesc in StructuralSeriesList) and (qualityList[j] in UsableList): 
                    StructuralSeriesDescScanIdDict[currSeriesDesc] = idList[j]
                    StructuralSeriesQualityDict[currSeriesDesc] = qualityList[j]
                    

                
            # this should check for absence and quality of scans and swap if bad or absent...
            for j in xrange(0, len(StructuralSeriesList)):
                currSeries = StructuralSeriesList[j]
                if (StructuralSeriesDescScanIdDict.get(currSeries) == None):
                    if (currSeries == 'T1w_MPR1'):
                        if (StructuralSeriesDescScanIdDict.get('T1w_MPR2') != None): # or (StructuralSeriesQualityDict.get('T1w_MPR2') not in UsableList):
                            StructuralSeriesDescScanIdDict['T1w_MPR1'] = StructuralSeriesDescScanIdDict.get('T1w_MPR2')
                            StructuralSeriesDescDict['T1w_MPR1'] = 'T1w_MPR2'
                    elif (currSeries == 'T1w_MPR2'):
                        if (StructuralSeriesDescScanIdDict.get('T1w_MPR1') != None): # or (StructuralSeriesQualityDict.get('T1w_MPR1') not in UsableList):
                            StructuralSeriesDescScanIdDict['T1w_MPR2'] = StructuralSeriesDescScanIdDict.get('T1w_MPR1')
                            StructuralSeriesDescDict['T1w_MPR2'] = 'T1w_MPR1'
                    elif (currSeries == 'T2w_SPC1'):
                        if (StructuralSeriesDescScanIdDict.get('T2w_SPC2') != None): # or (StructuralSeriesQualityDict.get('T2w_SPC2') not in UsableList):
                            StructuralSeriesDescScanIdDict['T2w_SPC1'] = StructuralSeriesDescScanIdDict.get('T2w_SPC2')
                            StructuralSeriesDescDict['T2w_SPC1'] = 'T2w_SPC2'
                    elif (currSeries == 'T2w_SPC2'):
                        if (StructuralSeriesDescScanIdDict.get('T2w_SPC1') != None): # or (StructuralSeriesQualityDict.get('T2w_SPC1') not in UsableList):
                            StructuralSeriesDescScanIdDict['T2w_SPC2'] = StructuralSeriesDescScanIdDict.get('T2w_SPC1')
                            StructuralSeriesDescDict['T2w_SPC2'] = 'T2w_SPC1'
                            
        
            # Collect scan ids for later testing...
            ScanIdList.append(MagScanId)
            ScanIdList.append(PhaScanId)
            ScanIdList.append(StructuralSeriesDescScanIdDict.get('T1w_MPR1'))
            ScanIdList.append(StructuralSeriesDescScanIdDict.get('T1w_MPR2'))
            ScanIdList.append(StructuralSeriesDescScanIdDict.get('T2w_SPC1'))
            ScanIdList.append(StructuralSeriesDescScanIdDict.get('T2w_SPC2'))
            ScanIdList = list(set(ScanIdList))
            
            
            
            if (MagScanId == 1) and (PhaScanId == 1):
                TE = 'NONE'
                sampleSpacingT1w = 'NONE'
                sampleSpacingT2w = 'NONE'
                unwarpdir = 'NONE'
                avgrdcmethod = 'NONE'
                scanParms = {'GEFieldMapGroup': 'NA'}
                
                T1wSampleSpacing = sampleSpacingT1w
                T2wSampleSpacing = sampleSpacingT2w
            else:
                getHCP.Scan = StructuralSeriesDescScanIdDict.get('T1w_MPR1')
                scanParms = getHCP.getScanParms( )
                sampleSpacingT1w = scanParms.get('SampleSpacing')
                
                getHCP.Scan = StructuralSeriesDescScanIdDict.get('T2w_SPC1')
                sampleSpacingT2w = getHCP.getScanParms( ).get('SampleSpacing')
            
                TE = magScanParms.get('DeltaTE')
                unwarpdir = 'z'
                avgrdcmethod = 'FIELDMAP'
                
                T1wSampleSpacing = float(sampleSpacingT1w)/1.0e+9
                T2wSampleSpacing = float(sampleSpacingT2w)/1.0e+9
            
            
        #Set the parameters for Structural pipeline
         
 
            if (scanParms.get('GEFieldMapGroup') == magScanParms.get('GEFieldMapGroup') == phaScanParms.get('GEFieldMapGroup')):
                    # do T1w and T2w path test...
                    for j in xrange(0, len(StructResources)):
                        getHCP.Resource = StructResources[j]
                        resourcePath = getHCP.getSubjectResourceMeta().get('RealPath')
                        getHCP.Scan = StructuralSeriesDescScanIdDict.get(StructuralSeriesList[j])
                        # this is a hack to account for archive1,2,3 and the discrepancy in the DB...
                        scanPathSplit = getHCP.getScanMeta().get('Path')[0].split('/')
                        scanPathSub = '/'.join(scanPathSplit[scanPathSplit.index(Project):])
                        if resourcePath:
                           if sys.platform != 'win32':
                                try:
                                    if (' '.join(resourcePath).index(scanPathSub) != -1): 
                                        PathMatch.append(True)
                                    else: 
                                        PathMatch.append(False)
                                except ValueError, e:
                                        PathMatch.append(False)    
                           else:
                                PathMatch.append(True)            
                    if all(PathMatch):
                            Parameters.addUniqueParameter('launchStructural','1')
                            Parameters.addUniqueParameter('structural_magscanid',MagScanId)
                            Parameters.addUniqueParameter('structural_phascanid',PhaScanId)
                            try: 
                                Parameters.addUniqueParameter('structural_t1scanid_1',StructuralSeriesDescScanIdDict.get('T1w_MPR1'))
                                Parameters.addUniqueParameter('structural_t1seriesdesc_1',StructuralSeriesDescDict.get('T1w_MPR1'))
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'No T1w_MPR1 scan found for %s' %(getHCP.Subject)
                            try:
                                Parameters.addUniqueParameter('structural_t1scanid_2',StructuralSeriesDescScanIdDict.get('T1w_MPR2'))
                                Parameters.addUniqueParameter('structural_t1seriesdesc_2',StructuralSeriesDescDict.get('T1w_MPR2'))
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'No T1w_MPR2 scan found for %s' %(getHCP.Subject)
                            try:
                                Parameters.addUniqueParameter('structural_t2scanid_1',StructuralSeriesDescScanIdDict.get('T2w_SPC1'))
                                Parameters.addUniqueParameter('structural_t2seriesdesc_1',StructuralSeriesDescDict.get('T2w_SPC1'))
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'No T1w_SPC1 scan found for %s' %(getHCP.Subject)
                            try:
                                Parameters.addUniqueParameter('structural_t2scanid_2',StructuralSeriesDescScanIdDict.get('T2w_SPC2'))
                                Parameters.addUniqueParameter('structural_t2seriesdesc_2',StructuralSeriesDescDict.get('T2w_SPC2'))
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'No T1w_SPC2 scan found for %s' %(getHCP.Subject)
                            
                            Parameters.addUniqueParameter('structural_TE',TE)
                            Parameters.addUniqueParameter('structural_UnwarpDir',unwarpdir)
                            Parameters.addUniqueParameter('structural_Avgrdcmethod',avgrdcmethod)
                            formattedSpacing='%1.9f' % T1wSampleSpacing
                            Parameters.addUniqueParameter('structural_T1wSampleSpacing',formattedSpacing)
                            formattedSpacing='%1.9f' % T2wSampleSpacing
                            Parameters.addUniqueParameter('structural_T2wSampleSpacing',formattedSpacing)
                            Parameters.addUniqueParameter('structural_T1wTemplate','MNI152_T1_0.7mm.nii.gz')
                            Parameters.addUniqueParameter('structural_T2wTemplate','MNI152_T2_0.7mm.nii.gz')
                            Parameters.addUniqueParameter('structural_T1wTemplateBrain','MNI152_T1_0.7mm_brain.nii.gz')
                            Parameters.addUniqueParameter('structural_T2wTemplateBrain','MNI152_T2_0.7mm_brain.nii.gz')
                            Parameters.addUniqueParameter('structural_TemplateMask','MNI152_T1_0.7mm_brain_mask.nii.gz')
                            Parameters.addUniqueParameter('structural_FinalTemplateSpace','MNI152_T1_0.7mm.nii.gz')
                            Parameters.addUniqueParameter('structural_fs_assessor_ext','3T')
    
                    else:
                            print 'ERROR: file paths mismatch for subject %s, session %s, structural pipeline, on server %s.' % (getHCP.Subject, getHCP.Session,  getHCP.Server)
            else:
                print 'ERROR: GEFieldMapGroup mismatch for subject %s, session %s, structural pipeline, on server %s.' % (getHCP.Subject, getHCP.Session, getHCP.Server) 
    else:
        Parameters.addUniqueParameter('launchStructural','0')

                
    #=======================================================================
    # FunctionalHCP
    #=======================================================================
    if (LaunchFunctional == 1):
        # build the subject specific functional lists...
        if (FunctSeries == None):
            FunctionalList = list()
            for i in xrange(0, len(sessionMeta.get('Types'))):
                if (sessionMeta.get('Types')[i] == 'tfMRI') or (sessionMeta.get('Types')[i] == 'rfMRI'):
                    FunctionalList.append(sessionMeta.get('Series')[i])
        else:
            FunctionalList = FunctSeries.split(',')
            
        FunctionalN += len(FunctionalList) 
        if (set(SubjectSessions.get('Types')) == 0):
            print 'ERROR: No  session could be found for subject ' +getHCP.Subject
            
        functionalScanParamsList = list()
        functionalSeriesParamsList = list()
        dwellTimesParamsList = list()
        unwarpDirParamsList = list()
        # MG: The TE parameter is actually Delta TE and is for the field map, not the T1w or T2w scans.  If you look for delta TE under the field map in the DB you will find it: 2.46ms.  This will change for 7T vs 3T but will otherwise always be the same.
        # NOTE: also important for functionalHCP is distortion correction is TOPUP, so fieldmap distortion correction is not even used.  TE could be anything and it would not matter.

        Parameters.addUniqueParameter('functional_TE','2.46')
        Parameters.addUniqueParameter('functional_DistortionCorrection','TOPUP')
        Parameters.addUniqueParameter('functional_lr_fieldmapseries','SpinEchoFieldMap_LR')
        Parameters.addUniqueParameter('functional_rl_fieldmapseries','SpinEchoFieldMap_RL')
        
        for i in xrange(0, len(FunctionalList)):
            linIdx += 1
            
            currSeries = FunctionalList[i]
    
            if (currSeries in sessionMeta.get('Series')):
                currUsability = sessionMeta.get('Quality')[sessionMeta.get('Series').index(currSeries)]
            else:
                print 'Current usability could not be determined for subject %s, session %s...' % (getHCP.Subject, getHCP.Session)

            print 'CurrSeries=%s' % (currSeries)
            if (FunctionalList.count(currSeries) == 1):
                FuncScanId = idList[sessionMeta.get('Series').index(currSeries)]
                FuncQuality = qualityList[sessionMeta.get('Series').index(currSeries)]
                getHCP.Scan = FuncScanId
                FuncScanParms = getHCP.getScanParms()
                getHCP.Scan = FuncScanId
                fucntScanMeta = getHCP.getScanMeta()
                functScanParms = getHCP.getScanParms()
                functionalScanParamsList.append(FuncScanId)
                functionalSeriesParamsList.append(currSeries)
                dwellTimesParamsList.append(str( float(FuncScanParms.get('EchoSpacing')) ))
                unwarpDirParamsList.append(FuncScanParms.get('PhaseEncodingDir'))    
            else:
                print 'OOPS, FunctionalHCP mismatch with FunctionalList and FunctSeries'

        #-------------------------------------------
        if (len(functionalScanParamsList)>0): 
            Parameters.addUniqueParameter('launchFunctional','1') 
            Parameters.addListParameters('functional_scanid',functionalScanParamsList)
            Parameters.addListParameters('functional_functionalseries',functionalSeriesParamsList)
            Parameters.addListParameters('functional_DwellTimes',dwellTimesParamsList)
            Parameters.addListParameters('functional_UnwarpDir',unwarpDirParamsList)
                
        else:
             Parameters.addUniqueParameter('launchFunctional','0')
    else:
         Parameters.addUniqueParameter('launchFunctional','0')

    #===============================================================================
    # FIX HCP....
    #===============================================================================
    if(LaunchICA == 1):
    	  RestingStateFunctionalSeriesList = list()	
          # build the subject specific RESTing state functional lists...
          for i in xrange(0, len(sessionMeta.get('Types'))):
              if (sessionMeta.get('Types')[i] == 'rfMRI'):
                  RestingStateFunctionalSeriesList.append(sessionMeta.get('Series')[i])

	  Parameters.addListParameters('icafix_functseries',RestingStateFunctionalSeriesList)
          Parameters.addUniqueParameter('icafix_bp','2000')
          Parameters.addUniqueParameter('launchICAFIX','1')
    else:
    	  Parameters.addUniqueParameter('launchICAFIX','0')

    #===============================================================================
    # TaskfMRIHCP....
    #===============================================================================
    if (LaunchTask == 1):

            #===================================================================
            # <parameter> functroot
            # <parameter> functseries
            # <parameter> lowresmesh
            # <parameter> grayordinates
            # <parameter> origsmoothingFWHM
            # <parameter> finalsmoothingFWHM
            # <parameter> confound
            # <parameter> vba
            #===================================================================
            LowResMesh = 32
            GrayOrdinates = 2
            OrigSmoothingFWHM = 2
            FinalSmoothingFWHM = 4
            TemporalFilter = 200
            Confound = 'NONE'
            VolumeBasedAnal = 'YES'
            
            
    	    TaskFunctionalSeriesRootList = list()
    	    
            # build the subject specific RESTing state functional lists...
            for i in xrange(0, len(sessionMeta.get('Types'))):
              if (sessionMeta.get('Types')[i] == 'tfMRI'):
                  seriesName = sessionMeta.get('Series')[i]
                  seriesParts = seriesName.split('_') 
                  TaskFunctionalSeriesRootList.append(seriesParts[0]+'_'+seriesParts[1])

	    Parameters.addListParameters('taskfMRI_functroot',TaskFunctionalSeriesRootList)

            Parameters.addUniqueParameter('taskfMRI_lowresmesh',LowResMesh)
            Parameters.addUniqueParameter('taskfMRI_grayordinates',GrayOrdinates)
            Parameters.addUniqueParameter('taskfMRI_origsmoothingFWHM',OrigSmoothingFWHM)
            Parameters.addUniqueParameter('taskfMRI_finalsmoothingFWHM',FinalSmoothingFWHM)
            Parameters.addUniqueParameter('taskfMRI_temporalfilter',TemporalFilter)
            Parameters.addUniqueParameter('taskfMRI_confound',Confound)
            Parameters.addUniqueParameter('taskfMRI_vba',VolumeBasedAnal)

            Parameters.addUniqueParameter('launchTask','1')
    else:
    	    Parameters.addUniqueParameter('launchTask','0')

    #===============================================================================
    # Launch MPP....
    #===============================================================================
    if (LaunchStructural == 1 or LaunchFunctional == 1 or  LaunchDiffusion == 1 or LaunchMPP == 1 or LaunchICA == 1 or  LaunchTask == 1):            
            #Since the wrk:xml field is exceeding 10000 characters, the following are supplied on commandline
            Parameters.addUniqueParameter('mailhost',MailHostStr)
            Parameters.addUniqueParameter('useremail',NotifyUserStr)
            Parameters.addUniqueParameter('userfullname',UserFullNameStr)
            Parameters.addUniqueParameter('xnatserver',XnatServerStr)
            Parameters.addUniqueParameter('adminemail',NotifyAdminStr)
            Parameters.addUniqueParameter('dataType','xnat:mrSessionData')   
            Parameters.addUniqueParameter('project',Project)
            Parameters.addUniqueParameter('label',getHCP.Session)

            Parameters.saveParameters(ParameterFilePath)       
            
    if (LaunchMPP == 1):
        
        launcherPipeline=' -pipeline %s '  %(mppPipelineName)
        launcherParameterFile=' -parameter paramfile=%s ' % (ParameterFilePath)
        launcherComputeCluster='-parameter compute_cluster=%s ' % (Compute)
        launcherSubjectParameter=' -parameter subject=%s ' %(launcherSubject)
        
        currentJSESSION=getHCP.getCurrentJSESSION()
        
        workflowObj=Workflow(pyHCP.User,pyHCP.Password,pyHCP.Server, currentJSESSION)
        workflowID=workflowObj.createWorkflow(sessionMeta.get('XNATID')[0], getHCP.Project, 'MPP/MPP.xml','Queued')
        launcherWorkFlowPrimaryKey=' -workFlowPrimaryKey %s ' % workflowID
        
        SubmitStr = JobSubmitter + PipelineLauncher + launcherPipeline + launcherHCPid + DataType + Host + XnatServer +  launcherExternalProject + launcherUser + launcherPassword + \
         SupressNotify + NotifyUser + NotifyAdmin + AdminEmail + UserEmail + MailHost + UserFullName + BuildDir + launcherSubjectParameter + launcherParameterFile + launcherComputeCluster + launcherWorkFlowPrimaryKey  

        if sys.platform == 'win32':
            print SubmitStr
        else:
            print SubmitStr
            if (Launch == 1):
                subprocess.call(SubmitStr, shell=True)
        
            
    print 'Sleeping for %s seconds with %s ...' % (str(SleepTime), getHCP.Subject)  
    time.sleep(SleepTime)     
print 'Done...total launch time was %s seconds for %s jobs with a sleep time of %s seconds per job...' % ( (time.time() - sTime), ( FunctionalN ), str(SleepTime) ) 
    
if __name__ == '__main__':
    pass
