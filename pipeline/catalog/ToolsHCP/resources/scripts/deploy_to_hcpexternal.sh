#!/bin/bash

#~ND~FORMAT~MARKDOWN
#~ND~START~
#
# # Script Description
#
# Deploy this <code>scripts</code> directory so the scripts are usuable from 
# the hcpexternal account for launching pipelines.
#
# Uses a simple rsync approach to update the 
# 
#  <code>/data/hcpdb/home/HCP_PYTHON/db_pipeline_customizations/templates/misc/catalog/ToolsHCP/resource/scripts</code>
#
# directory based on the contents of the current directory.
#
# Thus, editing of source can be done here and then "deployed" for use in actually submitting pipeline
# processing jobs.
#
# # Author(s)
# 
#   * Timothy B. Brown (tbbrown at wustl dot edu)
#
#~ND_END~

DEPLOY_DIRECTORY=/data/hcpdb/home/HCP_PYTHON/db_pipeline_customizations/templates/misc/catalog/ToolsHCP/resources/scripts/

# rsync -avz . ${DEPLOY_DIRECTORY}
rsync --archive --verbose --compress . ${DEPLOY_DIRECTORY}
