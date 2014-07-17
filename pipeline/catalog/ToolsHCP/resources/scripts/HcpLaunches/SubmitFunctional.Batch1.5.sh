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
-Subjects "116120,116524,117122,117324,118528,118730,118932,119833,120111,120212" \
-LaunchDiffusion 0 \
-LaunchFunctional 1 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7
