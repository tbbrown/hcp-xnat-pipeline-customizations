printf "Connectome DB Username: "
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../launchHCP.py \
-User ${username} \
-Password ${password} \
-Server db.humanconnectome.org \
-Project HCP_500 \
-Subjects "125525" \
-LaunchDiffusion 1 \
-LaunchFunctional 0 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 3,4,5,6,7



