#!/bin/bash -x


#This script will submit jobs to the PBS managed CHPC cluster for a subject taking care of the job dependencies

#DB Data Processing pipeline Job submittor
#Author: Mohana Ramaratnam (mohanakannan9@gmail.com)
#Version 0.1 Date: November 15, 2013

#Inputs: 
# path of param file


############################################################################
#
# Convenience Methods
#
############################################################################

get_jobid() {
  #$1: Series Description of the scan
  index=0
  found=-1
  for fseries in ${functional_functionalseries[@]}
  do
    if [ $fseries = $1 ]; then
      found=1
      break
    fi
    index=$((index+1))
  done
  
  
  #Did we find the series description
  if [ "$found" == "-1" ]; then
    echo $found
  else
   echo ${functionalJobIds[$index]}  
  fi
  
}


isQueuedFSF() {
  #$1: Series Description of the scan
  isQueued=0
  for fseries in "${queued[@]}"
  do
    if [ $fseries = $1 ] ; then
      isQueued=1
      break
    fi
  done
  echo $isQueued
}

isRestingStateScan() {
  #$1: Series Description of the scan
  isRestingScan=0
  for restingSeries in "${restSeriesDescription[@]}"
  do
    if [ $restingSeries = $1 ] ; then
      isRestingScan=1
      break
    fi
  done
  echo $isRestingScan
 
}

paramsFile=$1
passwd=$2
path_to_scripts=$3

declare -a functionalJobIds

declare -a queued

declare -a restSeriesDescription


functionalJobIds=()
queued=()

restSeriesDescription=("rfMRI_REST1" "rfMRI_REST2")

source $paramsFile

############################################################################
#
#Submit the structural job
#
############################################################################

queueLogFile=$path_to_scripts/queue.log

if [ -e $queueLogFile ] ; then
   \rm $queueLogFile
fi

touch $queueLogFile





if [ $launchStructural -eq 1 ] ; then	
     STRUCTURAL_START_JOB_ID=`qsub -V $path_to_scripts/${subject}_structural.sh`
     if [ $? -ne 0 ] ; then
        echo "Submission of  $path_to_scripts/${subject}_structural.sh failed. Aborting!"
        exit 1
     else 
        dependencyControl=" -W depend=afterok:${STRUCTURAL_START_JOB_ID} "
 	STRUCTURAL_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_structural_put.sh`
 	echo "Structural Processing job submitted for subject $subject. JOB ID = $STRUCTURAL_START_JOB_ID"
 	echo "Structural PUT job submitted for subject $subject. JOB ID = $STRUCTURAL_JOB_ID"
 	echo "Structural Processing job submitted for subject $subject. JOB ID = $STRUCTURAL_START_JOB_ID" >> $queueLogFile
 	echo "Structural PUT job submitted for subject $subject. JOB ID = $STRUCTURAL_JOB_ID" >> $queueLogFile
     fi
fi

############################################################################
#
#Now submit the functional jobs - these cannt be run unless the Structural are done
#
############################################################################

if [ $launchFunctional -eq 1 ] ; then
     index=0
     for fscan in "${functional_scanid[@]}"
     do
	fseries=${functional_functionalseries[$index]}
	fseriesRoot=`echo $fseries | awk '{gsub(/_LR/,""); gsub(/_RL/,""); print}'`

	dependencyControl=" "
	if [ $launchStructural -eq 1 ] ; then
           dependencyControl=" -W depend=afterok:${STRUCTURAL_JOB_ID} "
	fi
	FUNCTIONAL_START_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${fseries}_functional.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_${fseries}_functional.sh failed. Aborting!"
	  exit 1
	else 
	   echo "Functional job for $subject scan $fscan has been queued. JOB ID = $FUNCTIONAL_START_JOB_ID"
	   echo "Functional job for $subject scan $fscan has been queued. JOB ID = $FUNCTIONAL_START_JOB_ID" >> $queueLogFile
	fi
        
        dependencyControl=" -W depend=afterok:${FUNCTIONAL_START_JOB_ID} "

	FUNCTIONAL_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${fseries}_functional_put.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_${fseries}_functional_end.sh failed. Aborting!"
	  exit 1
	else 
	   echo "Functional job for $subject scan $fscan has been queued. JOB ID = $FUNCTIONAL_JOB_ID"
	   echo "Functional PUT job for $subject scan $fscan has been queued. JOB ID = $FUNCTIONAL_JOB_ID" >> $queueLogFile
	fi

	functionalJobIds[$index]=$FUNCTIONAL_JOB_ID
	let index=index+1;
#	index=$((index+1))
      done
fi



############################################################################
#
#Now submit the FSF creation job - these cannt be run unless the Functionals are done
#
############################################################################


if [ $launchFunctional -eq 1 ] ; then

     index=0
     j=0
     for fscan in "${functional_scanid[@]}"
     do
	fseries=${functional_functionalseries[$index]}
	fseriesRoot=`echo $fseries | awk '{gsub(/_LR/,""); gsub(/_RL/,""); print}'`

	isQueuedFSF=`isQueuedFSF $fseriesRoot` #We see fseriesRoot twice hence we need to keep track
	if [ $isQueuedFSF -eq 0 ]; then 
		lr_task_series=${fseriesRoot}_LR
		rl_task_series=${fseriesRoot}_RL
		lr_job_id=`get_jobid $lr_task_series`
		rl_job_id=`get_jobid $rl_task_series`
		dependencyControl=" "

		if [ $lr_job_id != "-1" ] || [ $rl_job_id != "-1" ] ; then
		   dependencyControl=" -W depend=afterok"
		fi 

		if [  $lr_job_id != "-1"  ] ; then
		  dependencyControl="${dependencyControl}:${lr_job_id}"
		  
		fi
		if [  $rl_job_id != "-1"  ] ; then
		  dependencyControl="${dependencyControl}:${rl_job_id}"
		fi
		dependencyControl="${dependencyControl} "

		echo "FSF DEPENDENCY $fseriesRoot $dependencyControl" >> $queueLogFile

		FUNCTIONAL_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${fseriesRoot}_end.sh`
		if [ $? -ne 0 ] ; then
		  echo "Submission of  $path_to_scripts/${subject}_${fseriesRoot}_end.sh failed. Aborting!"
		  exit 1
		else 
		   echo "FSF job for $subject scan $fseriesRoot has been queued. JOB ID = $FUNCTIONAL_JOB_ID"
		   echo "FSF job for $subject scan $fseriesRoot has been queued. JOB ID = $FUNCTIONAL_JOB_ID" >> $queueLogFile
		fi
		queued[$j]=$fseriesRoot
		j=$((j+1))
		echo ${queued[@]}
	fi
	index=$((index+1))
      done
fi


############################################################################
#
#Now submit the diffusion job - depends on structural 
#
############################################################################

if [ $launchDiffusion -eq 1 ] ; then
	dependencyControl=" "
	if [ $launchStructural -eq 1 ] ; then
	   dependencyControl=" -W depend=afterok:$STRUCTURAL_JOB_ID " 	
	fi
	PRE_EDDY_DIFFUSION=`qsub -V $dependencyControl $path_to_scripts/${subject}_pre_eddy.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_pre_eddy.sh failed. Aborting!"
	  exit 1
	else 
	  echo "Diffusion job for $subject has been queued. JOB ID = $PRE_EDDY_DIFFUSION"
	  echo "Diffusion PRE-EDDY job for $subject has been queued. JOB ID = $PRE_EDDY_DIFFUSION" >> $queueLogFile
	fi
	dependencyControl=" -W depend=afterok:$PRE_EDDY_DIFFUSION " 	
	EDDY_DIFFUSION=`qsub -V $dependencyControl $path_to_scripts/${subject}_eddy.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_eddy.sh failed. Aborting!"
	  exit 1
	else 
	  echo "Diffusion job for $subject has been queued. JOB ID = $EDDY_DIFFUSION"
	  echo "Diffusion EDDY job for $subject has been queued. JOB ID = $EDDY_DIFFUSION" >> $queueLogFile
	fi
	dependencyControl=" -W depend=afterok:$EDDY_DIFFUSION " 	
	POST_EDDY_DIFFUSION=`qsub -V $dependencyControl $path_to_scripts/${subject}_post_eddy.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_post_eddy.sh failed. Aborting!"
	  exit 1
	else 
	  echo "Diffusion job for $subject has been queued. JOB ID = $POST_EDDY_DIFFUSION"
	  echo "Diffusion POST-DIFFUSION job for $subject has been queued. JOB ID = $POST_EDDY_DIFFUSION" >> $queueLogFile
	fi
	dependencyControl=" -W depend=afterok:$POST_EDDY_DIFFUSION " 	

	DIFFUSION=`qsub -V $dependencyControl $path_to_scripts/${subject}_diffusion_put.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_diffusion.sh failed. Aborting!"
	  exit 1
	else 
	  echo "Diffusion PUT job for $subject has been queued. JOB ID = $DIFFUSION"
	  echo "Diffusion PUT job for $subject has been queued. JOB ID = $DIFFUSION" >> $queueLogFile
	fi

fi

############################################################################
#
#Now submit the Task-fMRI Analysis pipeline
#
############################################################################

#These cannt be run unless the corresponding Functional is done - and hence Structural 
if [ $launchTask -eq 1 ] ; then
	index=0
	for tscan in "${taskfMRI_functroot[@]}"
	do
	lr_job_id=" "
	rl_job_id=" "
	dependencyControl=" "
	if [ $launchFunctional -eq 1 ] ; then
	  lr_task_series=${tscan}_LR
	  rl_task_series=${tscan}_RL
	  lr_job_id=`get_jobid $lr_task_series`
	  rl_job_id=`get_jobid $rl_task_series`
	  dependencyControl=" "

	  if [ $lr_job_id != "-1" ] || [ $rl_job_id != "-1" ] ; then
	     dependencyControl=" -W depend=afterok"
	  fi 

	  if [  $lr_job_id != "-1"  ] ; then
	     dependencyControl="${dependencyControl}:${lr_job_id}"
	  fi
	  if [  $rl_job_id != "-1"  ] ; then
	     dependencyControl="${dependencyControl}:${rl_job_id}"
	  fi
	  dependencyControl="${dependencyControl} "
	fi  
	  #Now submit the task job
	  TASK_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${tscan}_taskanalysis.sh`  
	  if [ $? -ne 0 ] ; then
	    echo "Submission of  $path_to_scripts/${subject}_${tscan}_taskanalysis.sh failed. Aborting!"
	    exit 1
	  else 
	    if [ $launchFunctional -eq 1 ]; then
	      echo "Task Analysis job (id: $TASK_JOB_ID) for $subject task $tscan has been queued. It depends on completion of jobs = ${lr_job_id}, ${rl_job_id}"  >> $queueLogFile
            else
	      echo "Task Analysis job (id: $TASK_JOB_ID) for $subject task $tscan has been queued." >> $queueLogFile
            fi
	  fi
	  #Now submit the PUT job
	  dependencyControl=" -W depend=afterok:$TASK_JOB_ID"

	  TASK_PUT_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${tscan}_taskanalysis_put.sh`  
	  if [ $? -ne 0 ] ; then
	    echo "Submission of $path_to_scripts/${subject}_${tscan}_taskanalysis_put.sh failed. Aborting!"
	    exit 1
	  else 
	    echo "Task Analysis PUT job (id: $TASK_PUT_JOB_ID) for $subject task $tscan has been queued. It depends on completion of job = $TASK_JOB_ID"  >> $queueLogFile
	  fi

	done
	
fi

######################################################################################################################
#
#Now submit the ICA+FIX Analysis pipeline 
#
# ICAFIX Pipeline should be executed only for rfMRI_REST1_LR, rfMRI_REST1_RL, rfMRI_REST2_LR, rfMRI_REST2_RL. 
# This pipeline should be executed only PUT for the above scans is complete. 
#
######################################################################################################################

if [ $launchICAFIX -eq 1 ] ; then
     index=0
     fix_packaging_dependency_control=" -W depend=afterok:"
     for fscan in "${icafix_functseries[@]}"
     do
	fseries=${icafix_functseries[$index]}
	fseriesRoot=`echo $fseries | awk '{gsub(/_LR/,""); gsub(/_RL/,""); print}'`
	
	dependencyControl=" "
	if [ $launchFunctional -eq 1 ] ; then
	   functional_put_job_id=`get_jobid $fseries`
	   dependencyControl=" -W depend=afterok:${functional_put_job_id} "
	fi
	FIX_JOB_ID=`qsub -V $dependencyControl $path_to_scripts/${subject}_${fseries}_icafix.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_${fseries}_icafix.sh failed. Aborting!"
	  exit 1
	else 
	   echo "ICAFIX job for $subject scan $fseries has been queued. JOB ID = $FIX_JOB_ID"
	   echo "ICAFIX job for $subject scan $fseries has been queued. JOB ID = $FIX_JOB_ID" >> $queueLogFile
	fi
	dependencyControl=" -W depend=afterok:$FIX_JOB_ID " 	

	FIX_PUT=`qsub -V $dependencyControl $path_to_scripts/${subject}_${fseries}_icafix_put.sh`
	if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_${fseries}_icafix_put.sh failed. Aborting!"
	  exit 1
	else 
	  echo "ICAFIX PUT job for $subject has been queued. JOB ID = $FIX_PUT"
	  echo "ICAFIX PUT job for $subject has been queued. JOB ID = $FIX_PUT" >> $queueLogFile
	  fix_packaging_dependency_control="${fix_packaging_dependency_control}${FIX_PUT}:"
	fi

	index=$((index+1))
      done
      
      
      ##Now queue the FIX packaging script
      #Remove the last colon
      fix_packaging_dependency_control=`echo $fix_packaging_dependency_control | sed 's/:$//'`
      fix_packaging_dependency_control="${fix_packaging_dependency_control=} "
      echo "PACKGING DEPENDS ON $fix_packaging_dependency_control " >> $queueLogFile
      FIX_PACKAGING_JOB_ID=`qsub -V $fix_packaging_dependency_control $path_to_scripts/${subject}_icafix_package.sh`
      if [ $? -ne 0 ] ; then
	  echo "Submission of  $path_to_scripts/${subject}_icafix_package.sh failed. Aborting!"
	  exit 1
      else 
	  echo "ICAFIX PACKAGE job for $subject has been queued. JOB ID = $FIX_PACKAGING_JOB_ID"
	  echo "ICAFIX PACKAGE job for $subject has been queued. JOB ID = $FIX_PACKAGING_JOB_ID" >> $queueLogFile
      fi
       	

fi



exit 0