hcp-xnat-pipeline-customizations
================================

<code>pipeline/catalog/ToolsHCP/resources/scripts</code> directory

Some of the scripts in this directory are not used by the pipelines in the sense that a pipeline invokes 
the script but are instead used to launch pipelines. Examples of this include <code>launchHCP.py</code> and 
<code>launchMPP.py</code>.

To be used this way, they need to be deployed not only to the directory in which the pipeline is being run,
(e.g. <code>/home/HCPpipeline/pipeline</code> within the <code>HCPpipeline</code> account home directory on a CHPC login node), 
but also must be deployed to the <code>hcpexternal</code> account's home directory (<code>/data/hcpdb/home</code>) in the 
<code>HCP_PYTHON/db_pipeline_customizations/templates/misc/catalog/ToolsHCP/resources/scripts</code> subdirectory on the system 
from which launching will occur. (e.g. <code>hcpx-fs01.nrg.mir</code>)
