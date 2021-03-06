#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="788876,789373,792564,802844,814649,826353,826454,833148,833249,837560,837964,845458,849971,856766,857263,859671,861456,865363,871762,872158,872764,877168,877269,885975,887373,889579,894673,896778,896879,898176,899885,901038,901139,901442,904044,907656,910241,912447,917255,922854,930449,932554,951457,958976,959574,965367,965771,978578,937160"

python ../launchHCP.py \
-User "${userid}" \
-Password "${password}" \
-Server db.humanconnectome.org \
-Project HCP_Staging \
-Subjects "${subjList}" \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 1 \
-Shadow 1,2,3,4,5,6,7



