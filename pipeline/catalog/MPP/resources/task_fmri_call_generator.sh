#!/bin/bash -x
set -e

#This script will generate a job file for TaskfMRIHCP processing

#DB Structural Processing pipeline Job File Generator
#Author: Mohana Ramaratnam (mohanakannan9@gmail.com)
#Version 0.1 Date: April 14, 2014

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

ARGS=6
program="$0"

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $program` Path_to_paramsFile XNAT_Password Path_to_outFile"
  exit 1
fi


paramsFile=$1
mpp_pipelineparamsFile=$2
passwd=$3
outDir=$4
mppParamsFile=$5
jsession=$6

PIPELINE_NAME="TaskfMRIHCP/TaskfMRIHCP.xml"

dirname=`dirname "$program"`
configdir="${dirname}/config"


source $paramsFile
source $mpp_pipelineparamsFile
source $mppParamsFile


#Default to CHPC
if [ X$compute_cluster = X ] ; then
  compute_cluster=CHPC
fi

if [ $compute_cluster = CHPC ] ; then
   configurationForJobFile=$configdir/CHPC/taskfMRIHCP.pbs.config
   putConfigurationForJobFile=$configdir/CHPC/taskfMRIHCP_put.pbs.config
   taskfMRI_paramsFile=$configdir/CHPC/taskfMRIHCP.pbs.param
   logDirectiveFile=$configdir/CHPC/log.pbs.config	
elif [ $compute_cluster = NRG ] ; then
   configurationForJobFile=$configdir/NRG/taskfMRIHCP.sge.config
   putConfigurationForJobFile=$configdir/NRG/taskfMRIHCP_put.sge.config
   taskfMRI_paramsFile=$configdir/NRG/taskfMRIHCP.pbs.param
   logDirectiveFile=$configdir/NRG/log.sge.config	
fi

if [ ! -f $configurationForJobFile ] ; then
  echo "File at $configurationForJobFile doesnt exist. Aborting!"
  exit 1;
fi

if [ ! -f $putConfigurationForJobFile ] ; then
  echo "File at $putConfigurationForJobFile doesnt exist. Aborting!"
  exit 1;
fi

if [ ! -f $logDirectiveFile ] ; then
  echo "File at $logDirectiveFile doesnt exist. Aborting!"
  exit 1;
fi

if [ ! -f $taskfMRI_paramsFile ] ; then
  echo "File at $taskfMRI_paramsFile doesnt exist. Aborting!"
  exit 1;
fi

source $taskfMRI_paramsFile


###########################################################
# Check if the variables expected are defined
#
###########################################################

isSet taskfMRI_functroot[0]

isSet taskfMRI_lowresmesh1
isSet taskfMRI_origsmoothingFWHM1
isSet taskfMRI_finalsmoothingFWHM1
isSet taskfMRI_grayordinates1
isSet taskfMRI_confound1
isSet taskfMRI_vba1

isSet taskfMRI_lowresmesh2
isSet taskfMRI_origsmoothingFWHM2
isSet taskfMRI_finalsmoothingFWHM2
isSet taskfMRI_grayordinates2
isSet taskfMRI_confound2
isSet taskfMRI_vba2

isSet taskfMRI_lowresmesh3
isSet taskfMRI_origsmoothingFWHM3
isSet taskfMRI_finalsmoothingFWHM3
isSet taskfMRI_grayordinates3
isSet taskfMRI_confound3
isSet taskfMRI_vba3

isSet taskfMRI_lowresmesh4
isSet taskfMRI_origsmoothingFWHM4
isSet taskfMRI_finalsmoothingFWHM4
isSet taskfMRI_grayordinates4
isSet taskfMRI_confound4
isSet taskfMRI_vba4

###########################################################
# Continue - looks good
#
###########################################################

index=0
for tscan in "${taskfMRI_functroot[@]}"
do

        echo "Creating command file to launch Functional Task Analysis for subject: ${subject} and scan ${tscan}"
  #For each scan create the outfile of command to launch the Functional Task Analysis  pipeline

	outFile=${outDir}/${subject}_${tscan}_taskanalysis.sh
	putFile=${outDir}/${subject}_${tscan}_taskanalysis_put.sh

	echo "Creating: $outFile"
	touch $outFile

	echo "Creating: $putFile"
	touch $putFile

	if [ ! -f $outFile ] ; then
	  echo "File at $outFile doesnt exist. Aborting!"
	  exit 1;
	fi
	if [ ! -f $putFile ] ; then
	  echo "File at $putFile doesnt exist. Aborting!"
	  exit 1;
	fi

	cat $configurationForJobFile > $outFile
	cat $logDirectiveFile >> $outFile	

	cat $putConfigurationForJobFile > $putFile
	cat $logDirectiveFile >> $putFile	



	workflowID=`source $SCRIPTS_HOME/epd-python_setup.sh; python $PIPELINE_HOME/catalog/ToolsHCP/resources/scripts/workflow.py -User $user -Password $passwd -Server $host -ExperimentID $xnat_id -ProjectID $project -Pipeline $PIPELINE_NAME -Status Queued -JSESSION $jsession`
	if [ $? -ne 0 ] ; then
		echo "Fetching workflow for functional failed. Aborting!"
		exit 1
	fi 

	commandStr="$PIPELINE_HOME/bin/XnatPipelineLauncher -pipeline TaskfMRIHCP/TaskfMRIHCP.xml -project $project -id $xnat_id -dataType $dataType -host $xnat_host -parameter xnatserver=$xnatserver -parameter project=$project -parameter xnat_id=$xnat_id -label $label -u $user -pwd $passwd -supressNotification -notify $useremail -notify $adminemail -parameter adminemail=$adminemail -parameter useremail=$useremail -parameter mailhost=$mailhost -parameter userfullname=$userfullname -parameter builddir=$builddir -parameter sessionid=$sessionId -parameter subjects=$subject -parameter functroot=$tscan -parameter lowresmesh1=$taskfMRI_lowresmesh1 -parameter grayordinates1=$taskfMRI_grayordinates1 -parameter origsmoothingFWHM1=$taskfMRI_origsmoothingFWHM1 -parameter finalsmoothingFWHM1=$taskfMRI_finalsmoothingFWHM1 -parameter temporalfilter1=$taskfMRI_temporalfilter1 -parameter confound1=$taskfMRI_confound1 -parameter vba1=$taskfMRI_vba1 -parameter lowresmesh2=$taskfMRI_lowresmesh2 -parameter grayordinates2=$taskfMRI_grayordinates2 -parameter origsmoothingFWHM2=$taskfMRI_origsmoothingFWHM2 -parameter finalsmoothingFWHM2=$taskfMRI_finalsmoothingFWHM2 -parameter temporalfilter2=$taskfMRI_temporalfilter2 -parameter confound2=$taskfMRI_confound2 -parameter vba2=$taskfMRI_vba2 -parameter lowresmesh3=$taskfMRI_lowresmesh3 -parameter grayordinates3=$taskfMRI_grayordinates3 -parameter origsmoothingFWHM3=$taskfMRI_origsmoothingFWHM3 -parameter finalsmoothingFWHM3=$taskfMRI_finalsmoothingFWHM3 -parameter temporalfilter3=$taskfMRI_temporalfilter3 -parameter confound3=$taskfMRI_confound3 -parameter vba3=$taskfMRI_vba3 -parameter lowresmesh4=$taskfMRI_lowresmesh4 -parameter grayordinates4=$taskfMRI_grayordinates4 -parameter origsmoothingFWHM4=$taskfMRI_origsmoothingFWHM4 -parameter finalsmoothingFWHM4=$taskfMRI_finalsmoothingFWHM4 -parameter temporalfilter4=$taskfMRI_temporalfilter4 -parameter confound4=$taskfMRI_confound4 -parameter vba4=$taskfMRI_vba4 -parameter templatesdir=$templatesdir -parameter configdir=$configdir -parameter CaretAtlasDir=$CaretAtlasDir -parameter compute_cluster=$compute_cluster -parameter packaging_outdir=$packaging_outdir -parameter cluster_builddir_prefix=$cluster_builddir_prefix -parameter db_builddir_prefix=$db_builddir_prefix  -workFlowPrimaryKey $workflowID  "

	echo "Creating $outFile" 

	echo "echo \" \"" >> $outFile
	echo "$commandStr" >> $outFile
	echo "rc_command=\$?" >> $outFile

	echo "echo \$rc_command \" \"" >> $outFile
	echo "echo \"Job finished  at \`date\`\"" >> $outFile


	echo "exit \$rc_command" >> $outFile

###########################################################
# Create PUT JOB
#
###########################################################

	commandStr="$commandStr -startAt 14 "

	echo "Creating $putFile" 

	echo "echo \" \"" >> $putFile
	echo "$commandStr" >> $putFile
	echo "rc_command=\$?" >> $putFile

	echo "echo \$rc_command \" \"" >> $putFile
	echo "echo \"Job finished  at \`date\`\"" >> $putFile


	echo "exit \$rc_command" >> $putFile



	chmod +x $outFile
	chmod +x $putFile

	index=$((index+1))

done

exit 0