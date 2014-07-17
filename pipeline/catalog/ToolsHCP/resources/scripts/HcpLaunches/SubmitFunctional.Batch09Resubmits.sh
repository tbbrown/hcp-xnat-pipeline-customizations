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
-Subjects "627549,645551,672756,673455,677968,680957,683256,685058,690152,695768,704238,705341,715647,729557,732243,742549,751348,756055,782561" \
-LaunchDiffusion 0 \
-LaunchFunctional 1 \
-LaunchStructural 0 \
-LaunchMPP 1 \
-Launch 1 \
-Compute CHPC \
-LaunchTaskAnalysis 0 \
-LaunchICAAnalysis 0 \
-Shadow 1,2,3,4,5,6,7
