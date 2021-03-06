#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="178142,178748,178849,178950,179346,179548,180129,180432,180836,180937,181131,181232,182739,182840,183034,185139,186141,187143,187547,187850,188347,189349,189450,190031,191033,191437,191841,192439,192540,192843,193239,194140,194645,195041,195647,195849,196144,196750,197348,197550,197651,198350,198451,198855,199150,199251,199453"

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
