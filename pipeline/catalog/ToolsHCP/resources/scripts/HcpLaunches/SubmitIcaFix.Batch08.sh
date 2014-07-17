#!/bin/bash

printf "Connectome DB User ID (e.g. tbbrown): "
read userid


stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo


subjList="441939,445543,448347,465852,473952,475855,479762,480141,485757,486759,497865,499566,500222,510326,519950,521331,522434,528446,530635,531536,540436,541640,541943,545345,547046,552544,559053,561242,562446,565452,566454,567052,567961,568963,570243,573249,573451,579665,580044,580347,581349,583858,585862,586460,592455,594156,598568,599065,599671"

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



