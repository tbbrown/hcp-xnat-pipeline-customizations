printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subj="660951"

python ../launchHCP.py \
-User ${userid} \
-Password ${password} \
-Server db.humanconnectome.org \
-Project HCP_Staging \
-Subjects ${subj} \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 1 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7,8
