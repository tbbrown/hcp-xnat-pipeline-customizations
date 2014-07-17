#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid


stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo


subjList="100307,100408,101006,101107,101309,101410,101915,102008,102311,102816"

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



