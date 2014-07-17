printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../launchMPP.py \
--debug \
--server=db.humanconnectome.org \
--username=${userid} \
--password=${password} \
--project=PipelineTest \
--subject=LS4043 \
--sessionsuffix=_3T \
--structural
