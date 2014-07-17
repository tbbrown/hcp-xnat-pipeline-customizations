#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="177746"

python ../launchHCP.py \
-Debug \
-User "${userid}" \
-Password "${password}" \
-Server db.humanconnectome.org \
-Project HCP_500 \
-Subjects "${subjList}" \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 1 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7



