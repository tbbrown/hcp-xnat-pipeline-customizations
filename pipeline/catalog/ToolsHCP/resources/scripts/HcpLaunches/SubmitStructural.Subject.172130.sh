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
-Subjects "172130" \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 1 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 5
