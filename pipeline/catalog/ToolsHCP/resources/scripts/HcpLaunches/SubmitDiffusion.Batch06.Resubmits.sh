#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../launchHCP.py \
-User "${userid}" \
-Password "${password}" \
-Server db.humanconnectome.org \
-Project HCP_Staging \
-Subjects "201818,205119,210415,211417,211720,212217,212419,214423,224022,233326" \
-LaunchDiffusion 1 \
-LaunchFunctional 0 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7



