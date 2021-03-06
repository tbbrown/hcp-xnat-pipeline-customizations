#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="250932,255639,256540,268850,280739,284646,285345,285446,289555,290136,293748,298051,298455,303119,303624,307127,308331,310621,316633,329440,334635,351938,352132,352738,355239,356948,365343,366042,366446,371843,377451,380036,385450,386250,395958,397154,397760,397861,412528,414229,415837,422632,433839,436239,436845"

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
-Shadow 1,2,3,4,5,6,7,8
