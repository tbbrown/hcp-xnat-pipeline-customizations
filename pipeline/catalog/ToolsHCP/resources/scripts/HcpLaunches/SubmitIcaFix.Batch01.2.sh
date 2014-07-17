#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid


stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo


subjList="103111,103414,103515,103818,104820,105014,105115,105216,106016,106319,106521,107321,107422,108121,108525,108828,109123,109325,110411,111312,111413,111716,112819,113215,113619,113821,113922,114419,114924,115320,116120,116524,117122,117324,118528,118730,118932,119833,120111,120212"


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



