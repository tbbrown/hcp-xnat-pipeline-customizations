printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

--Debug \
-User ${userid} \
-Password ${password} \
-Server db.humanconnectome.org \
-Project PipelineTest \
-Subjects "LS2043" \
-LaunchDiffusion 0 \
-LaunchFunctional 0 \
-LaunchStructural 1 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 4,5,6,7,8
