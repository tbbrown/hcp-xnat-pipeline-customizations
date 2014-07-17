#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="158035,158136,158540,159138,159239,159340,159441,160123,160830,161731,162026,162228,162329,162733,163129,163331,163432,163836,164030,164131,164939,165032,165840,167036,167743,168139,168341,169343,169444,170934,171431,171633,172029,172130,172332,172534,173132,173334,173435,173536,173940,175035,175439,176542,177645"

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
