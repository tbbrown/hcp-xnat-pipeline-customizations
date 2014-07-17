#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="673455"

python ../launchHCP.py \
-Debug \
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
-LaunchTaskAnalysis 1 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7
