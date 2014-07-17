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

The <code>hcp_constants.py</code> file needs to hold contents that are appropriate for the system on which the pipelines are running.
For example, on a "standard" XNAT installation (like that on fs01), the XNAT database is located in <code>/data/hcpdb/</code>.
On the CHPC systems at Washington University, the XNAT database is located in <code>/HCP/hcpdb/</code>. Some scripts are 
written with the assumption that the XNAT database is at <code>/data/hcpdb/</code> and then does a path substitution using
the contents of <code>hcp_constants.py</code> as a substitution guide.  

The file <code>hcp_constants.fs01.py</code> contains the correct substitution to use on the <code>hcpx-fs01.nrg.mir</code> system. 
That is to simply replace <code>/data/</code> with <code>/data/</code> (no change).  The file <code>hcp_constants.CHPC.py</code>
contains the correct substitution to use on the CHPC cluster nodes. It indicates that <code>/data/</code> should be replaced by 
<code>/HCP/</code>.

The file <code>hcp_constants.py</code> can be copied from one of those files as appropriate or created as a link to one of those
files. 