#!/bin/bash

#
#
#Mohana Ramaratnam 11-28-2013
#
#Script to copy the EV and Physio files
#
############################################################
#
# Pre-requisites - Environment variable XNAT_ARCHIVE_ROOT
#
############################################################

############################################################
#
# ARGUMENTS:
# 
# 1. Session ID
# 2. Project
# 3. Subject
# 4. Scan Id
# 5. Series Descripion
#
############################################################


ARGS=6
program="$0"

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $program` SessionID Project Subject ScanID SeriesDescription"
  exit 1
fi

sessionId=$1
project=$2
subject=$3
scanId=$4
series=$5
outDirRoot=$6

if [ -z $XNAT_ARCHIVE_ROOT ] ; then
  echo "Environment variable XNAT_ARCHIVE_ROOT not set. Aborting"
  exit 1
fi


############################################################
#Rules
#
# If the LINKED_DATA/EPRIME/EV exists, copy it to [SERIES_DESCRIPTION]_preproc/MNINonLinear/Results/[SERIES_DESCRIPTION]/EVs
#
#./SCANS/216/LINKED_DATA/PHYSIO/Physio_log_1a0b5750-dbfa-4846-b471-7eb34c4cfb37.txt 
#maps to ./RESOURCES/tfMRI_WM_LR_preproc/MNINonLinear/Results/tfMRI_WM_LR/tfMRI_WM_LR_Physio_log.txt
#
#./SCANS/216/LINKED_DATA/EPRIME/100307_3T_REC_run2_TAB.txt
#
#./SCANS/216/LINKED_DATA/EPRIME/100307_3T_WM_run2_TAB.txt
#maps to ./RESOURCES/tfMRI_WM_LR_preproc/MNINonLinear/Results/tfMRI_WM_LR/REC_run2_TAB.txt
# 
#./RESOURCES/tfMRI_WM_LR_preproc/MNINonLinear/Results/tfMRI_WM_LR/WM_run2_TAB.txt
############################################################

scanDir=$XNAT_ARCHIVE_ROOT/$project/arc001/$sessionId/SCANS/$scanId
physioDir=$scanDir/LINKED_DATA/PHYSIO
eprimeDir=$scanDir/LINKED_DATA/EPRIME
evDir=$scanDir/LINKED_DATA/EPRIME/EVs

outEVDir=$outDirRoot/EVs

if [ ! -d "$scanDir" ] ; then
   echo "Something is horribly wrong. No scan directory found. Aborting!"
   exit 1
fi

if [  -d "$physioDir" ] ; then
  for physioTxtFile in $(ls $physioDir/Physio_log_*.txt)
  do
     echo "cp $physioTxtFile $outDirRoot/${series}_Physio_log.txt"	
     cp $physioTxtFile $outDirRoot/${series}_Physio_log.txt
  done	
fi

undersc="_"

if [  -d "$eprimeDir" ] ; then
  pushd $eprimeDir
  for tabTxtFile in $(ls *_TAB.txt)
  do
     newTabTxtName=`echo $tabTxtFile | sed  "s|^$sessionId$undersc\(.*\)\.txt|\1.txt|"`
     echo "cp $tabTxtFile $outDirRoot/$newTabTxtName"
     cp $tabTxtFile $outDirRoot/$newTabTxtName
  done
  popd
fi

if [  -d "$evDir" ] ; then
  mkdir -p $outEVDir
  echo "cp -r $evDir/* $outEVDir"
  cp -r $evDir/* $outEVDir
fi

exit 0