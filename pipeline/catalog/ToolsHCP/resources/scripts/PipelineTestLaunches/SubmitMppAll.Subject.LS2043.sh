printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../launchHCP.py \
--Debug \
-User ${userid} \
-Password ${password} \
-Server db.humanconnectome.org \
-Project PipelineTest \
-Subjects "LS2043" \
-LaunchDiffusion 1 \
-LaunchFunctional 1 \
-LaunchStructural 1 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 1 \
-LaunchICAAnalysis 1 \
-Shadow 4,5,6,7,8
