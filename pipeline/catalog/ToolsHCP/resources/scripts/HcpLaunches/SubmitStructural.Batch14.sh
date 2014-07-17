stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../launchHCP.py \
-User tbbrown \
-Password ${password} \
-Server db.humanconnectome.org \
-Project HCP_Staging \
-Subjects "108323,151728,161327,161630,166438,172938,191336,194847,199554,208428,211215,231928,251833,339847,361941,382242,390645,571548,599469,749361,779370,792766,816653,957974,959069" \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 1 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7,8
