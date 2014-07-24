#!/bin/bash 


#This script will generate a job file for a StructuralHCP pipeline processing

#DB Structural Processing pipeline Job File Generator
#Author: Mohana Ramaratnam (mohanakannan9@gmail.com)
#Version 0.1 Date: November 15, 2013

#Inputs: 
# path of param file
# path to location where the job file would be generated

#The PBS/SGE statements are picked from a config file for the specific cluster


isSet() {
   if [[ ! ${!1} && ${!1-_} ]] ; then
        echo "$1 is not set, aborting."
        exit 1
   elif [ -z ${!1} ] ; then	
        echo "$1 has no value, aborting."
        exit 1
   fi
}

ARGS=7
program="$0"

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $program` Path_to_paramsFile Path_to_mppPipelineParamsFile XNAT_Password Path_to_outFile Path_to_outPutJobFile MPP_PARAM_FILE_PATH"
  exit 1
fi

paramsFile=$1
mpp_pipelineparamsFile=$2
passwd=$3
outFile=$4
outPutJobFile=$5
mppParamsFile=$6
jsession=$7

source $paramsFile
source $mpp_pipelineparamsFile

source $mppParamsFile

PIPELINE_NAME="StructuralHCP/StructuralHCP.xml"

dirname=`dirname "$program"`
configdir="${dirname}/config"

#Default to CHPC
if [ X$compute_cluster = X ] ; then
  compute_cluster=CHPC
fi

config_root_name=structuralHCP

if [ $compute_cluster = CHPC ] ; then
   configurationForJobFile=$configdir/CHPC/${config_root_name}.pbs.config  
   configurationForPutJobFile=$configdir/CHPC/${config_root_name}_put.pbs.config  
   logDirectiveFile=$configdir/CHPC/log.pbs.config	

   processingParamsFile=$configdir/CHPC/structuralHCP.pbs.param   	
elif [ $compute_cluster = NRG ] ; then
   configurationForJobFile=$configdir/NRG/${config_root_name}.sge.config
   configurationForEndJobFile=$configdir/NRG/${config_root_name}_put.sge.config  
   logDirectiveFile=$configdir/NRG/log.sge.config	

   processingParamsFile=$configdir/NRG/structuralHCP.sge.param   	
fi

if [ ! -f $configurationForJobFile ] ; then
  echo "File at $configurationForJobFile doesnt exist. Aborting!"
  exit 1;
fi


if [ ! -f $configurationForPutJobFile ] ; then
  echo "File at $configurationForPutJobFile doesnt exist. Aborting!"
  exit 1;
fi


if [ ! -f $processingParamsFile ] ; then
  echo "File at $processingParamsFile doesnt exist. Aborting!"
  exit 1;
fi

if [ ! -f $logDirectiveFile ] ; then
  echo "File at $logDirectiveFile doesnt exist. Aborting!"
  exit 1;
fi


#The processing params file would contain path to the configdir, CaretAtlasDir, templatesdir
source $processingParamsFile

###########################################################
# Check if the variables expected are defined
#
###########################################################

isSet structural_t1scanid_1
isSet structural_t1scanid_2
isSet structural_t2scanid_1
isSet structural_t2scanid_2
isSet structural_t1seriesdesc_1
isSet structural_t1seriesdesc_2
isSet structural_t2seriesdesc_1
isSet structural_t2seriesdesc_2
isSet structural_magscanid
isSet structural_phascanid
isSet structural_T1wSampleSpacing
isSet structural_T2wSampleSpacing
isSet structural_Avgrdcmethod


###########################################################
# Continue - looks good
#
###########################################################


touch $outFile
touch $outPutJobFile


if [ ! -f $outFile ] ; then
  echo "File at $outFile doesnt exist. Aborting!"
  exit 1;
fi

if [ ! -f $outPutJobFile ] ; then
  echo "File at $outPutJobFile doesnt exist. Aborting!"
  exit 1;
fi


cat $configurationForJobFile > $outFile
cat $logDirectiveFile >> $outFile	

cat $configurationForPutJobFile > $outPutJobFile
cat $logDirectiveFile >> $outPutJobFile	


workflowID=`source $SCRIPTS_HOME/epd-python_setup.sh; python $PIPELINE_HOME/catalog/ToolsHCP/resources/scripts/workflow.py -User $user -Password $passwd -Server $host -ExperimentID $xnat_id -ProjectID $project -Pipeline $PIPELINE_NAME -Status Queued -JSESSION $jsession`
if [ $? -ne 0 ] ; then
	echo "Fetching workflow for structural failed. Aborting!"
	exit 1
fi 


commandStr="$PIPELINE_HOME/bin/XnatPipelineLauncher -pipeline $PIPELINE_NAME -project $project -id $xnat_id -dataType $dataType -host $xnat_host -parameter xnatserver=$xnatserver -parameter project=$project -parameter xnat_id=$xnat_id -label $label -u $user -pwd $passwd -supressNotification -notify $useremail -notify $adminemail -parameter adminemail=$adminemail -parameter useremail=$useremail -parameter mailhost=$mailhost -parameter userfullname=$userfullname -parameter bilddir=$builddir -parameter sessionid=$sessionId -parameter subjects=$subject -parameter magscanid=$structural_magscanid -parameter phascanid=$structural_phascanid -parameter t1scanid_1=$structural_t1scanid_1 -parameter t1scanid_2=$structural_t1scanid_2 -parameter t2scanid_1=$structural_t2scanid_1 -parameter t2scanid_2=$structural_t2scanid_2 -parameter t1seriesdesc_1=$structural_t1seriesdesc_1 -parameter t1seriesdesc_2=$structural_t1seriesdesc_2 -parameter t2seriesdesc_1=$structural_t2seriesdesc_1 -parameter t2seriesdesc_2=$structural_t2seriesdesc_2 -parameter TE=$structural_TE -parameter T1wSampleSpacing=$structural_T1wSampleSpacing -parameter T2wSampleSpacing=$structural_T2wSampleSpacing -parameter Avgrdcmethod=$structural_Avgrdcmethod -parameter T1wTemplate=$structural_T1wTemplate -parameter T1wTemplateBrain=$structural_T1wTemplateBrain -parameter T2wTemplate=$structural_T2wTemplate -parameter T2wTemplateBrain=$structural_T2wTemplateBrain -parameter TemplateMask=$structural_TemplateMask -parameter FinalTemplateSpace=$structural_FinalTemplateSpace -parameter templatesdir=$templatesdir  -parameter configdir=$configdir -parameter CaretAtlasDir=$CaretAtlasDir -parameter compute_cluster=$compute_cluster -parameter packaging_outdir=$packaging_outdir -parameter structural_fs_assessor_ext=$structural_fs_assessor_ext -parameter cluster_builddir_prefix=$cluster_builddir_prefix -parameter db_builddir_prefix=$db_builddir_prefix -workFlowPrimaryKey $workflowID"
putCommandStr="$commandStr -startAt 15"


echo "Creating $outFile" 

echo "echo \" \"" >> $outFile
echo "$commandStr" >> $outFile
echo "rc_command=\$?" >> $outFile

echo "echo \$rc_command \" \"" >> $outFile
echo "echo \"Job finished  at \`date\`\"" >> $outFile

echo "exit \$rc_command" >> $outFile

chmod +x $outFile

###########################################################
# Create PUT JOB
#
###########################################################


echo "Creating $outPutJobFile" 

echo "echo \" \"" >> $outPutJobFile
echo "$putCommandStr" >> $outPutJobFile
echo "rc_command=\$?" >> $outPutJobFile

echo "echo \$rc_command \" \"" >> $outPutJobFile
echo "echo \"Job finished  at \`date\`\"" >> $outPutJobFile

echo "exit \$rc_command" >> $outPutJobFile

chmod +x $outPutJobFile


exit 0;