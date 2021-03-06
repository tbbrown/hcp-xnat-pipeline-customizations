#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid


stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo


subjList="199655,200109,199958,200614,201111,201414,201818,203418,204016,204521,205119,205220,205725,205826,208024,208226,208327,209733,209834,209935,210011,210415,210617,211316,211417,211720,211922,212116,212217,212318,212419,214019,214221,214423,214726,217126,217429,219231,221319,224022,233326,239944,245333,246133,249947,250427"


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



