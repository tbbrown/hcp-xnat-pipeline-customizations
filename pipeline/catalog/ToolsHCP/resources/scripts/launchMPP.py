'''
@author: Timothy B. Brown (tbbrown@wustl.edu) 
'''

PROGRAM_VERSION = '1.0.0'

# XNAT session type for the session which should be used for preprocessing
PROCESSING_SESSION_TYPE = 'xnat:mrSessionData'

# Info about the first usable T1w scan
FIRST_T1W_FILE_NAME_BASE = 'T1w_MPR1'
FIRST_T1W_UNPROC_RESOURCE_NAME = FIRST_T1W_FILE_NAME_BASE + '_unproc'

# Info about the second usable T1w scan
SECOND_T1W_FILE_NAME_BASE = 'T1w_MPR2'
SECOND_T1W_UNPROC_RESOURCE_NAME = SECOND_T1W_FILE_NAME_BASE + '_unproc'

# Info about the first usable T2w scan
FIRST_T2W_FILE_NAME_BASE = 'T2w_SPC1'
FIRST_T2W_UNPROC_RESOURCE_NAME = FIRST_T2W_FILE_NAME_BASE + '_unproc'

# Info about the second usable T2w scan
SECOND_T2W_FILE_NAME_BASE = 'T2w_SPC2'
SECOND_T2W_UNPROC_RESOURCE_NAME = SECOND_T2W_FILE_NAME_BASE + '_unproc'

COMPRESSED_NIFTI_EXTENSION = '.nii.gz'

# This CSV file exists in each _unproc resource to let us know what scan
# numbers correspond to each image file in the resource
SCAN_NUMBER_MAPPING_FILE_NAME = 'filescans.csv'

MAG_FIELDMAP_NAME = 'FieldMap_Magnitude'
PHASE_FIELDMAP_NAME = 'FieldMap_Phase'

SPIN_ECHO_FIELDMAP_NAME = 'SpinEchoFieldMap'
POSITIVE_SPIN_ECHO_FIELDMAP_NAME = SPIN_ECHO_FIELDMAP_NAME + '_RL'
NEGATIVE_SPIN_ECHO_FIELDMAP_NAME = SPIN_ECHO_FIELDMAP_NAME + '_LR'

import argparse # For parsing command line arguments
import StringIO # Read string buffers as if they were files (i.e. read in-memory files)
import csv      # Comma Separated Value (csv) reading

from xnat_access import XnatAccess        # The XnatAccess class allows us to interact with an XNAT instance
from mpp_parameters import MppParameters  # The MppParameters class manages parameters the must be specified to invoke MPP pipelines

def show_retrieved_params( args ):
    """
    Display (on stdout) user specified input parameters for this program.
    """
    print("\nInput Parameters")
    print("\tdebug: " + str(args.debug))
    print("\tserver: " + args.server)
    print("\tusername: " + args.username)
    print("\tproject: " + args.project)
    print("\tsubject: " + args.subject)
    print("\tsession_suffix: " + args.session_suffix)
    print("\tstructural: " + str(args.structural))
    print("\tfieldmaps: " + args.fieldmaps)

def retrieve_params( ):
    """
    Parse the user specified command-line parameters to create an args object containing the user specified values
    """
    parser = argparse.ArgumentParser(description="Script to generate proper command for XNAT Minimal Preprocessing (MPP) launching ...")

    parser.add_argument("-d",  "--debug",    dest="debug", action='store_true')
    parser.add_argument("-v",  "--version",  action='version', version="%(prog)s " + PROGRAM_VERSION)
    parser.add_argument("-s",  "--server",   dest="server", required=True, type=str,
                        help="e.g. db.humanconnectome.org")
    parser.add_argument("-u",  "--username", dest="username", required=True, type=str)
    parser.add_argument("-pw", "--password", dest="password", required=True, type=str)
    parser.add_argument("-pr", "--project",  dest="project", required=True, type=str,
                        help="e.g. PipelineTest, HCP_Staging, WU_L1A_Staging, etc.")
    parser.add_argument("-su", "--subject",  dest="subject", required=True, type=str)
    parser.add_argument("-ss", "--sessionsuffix", dest="session_suffix", default="_3T", type=str,
                        help="defaults to _3T")
    parser.add_argument("-st", "--structural", dest="structural", action='store_true',
                        help="specifying this argument means structural preprocessing is to be done")
    parser.add_argument("-fm", "--fieldmaps", dest="fieldmaps", required=True, choices=('GE', 'SE'), type=str, 
                        help="GE = use Gradient Echo FieldMaps; SE = use Spin Echo FieldMaps")

    args = parser.parse_args()
    return args

def create_resource_file_name_to_scan_number_map(xnat_access):
    """
    create a map/dict which when given a file name will return the scan number that corresponds 
    to that file name
    """

    file_name_to_scan_number = dict()
    file_name_list = xnat_access.get_resource_file_name_list()
    if SCAN_NUMBER_MAPPING_FILE_NAME in file_name_list:
        scan_mapping_str = xnat_access.get_named_resource_file_content(SCAN_NUMBER_MAPPING_FILE_NAME)
        f = StringIO.StringIO(scan_mapping_str)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            key = row[1].replace("'", "")
            val = row[0].replace("'", "")
            if val != 'Scan':
                file_name_to_scan_number[key] = val

    return file_name_to_scan_number

# Main functionality

# Initialize MPP processing parameters
mpp_parameters = MppParameters()

# Get and show the command line parameters
global args
args = retrieve_params()
show_retrieved_params(args)

# Use specified username and password to get token username and password
print("\nRequesting token username and password")
xnat_access = XnatAccess(args.server, args.username, args.password)
new_username, new_password = xnat_access.get_new_tokens()
args.username = new_username
args.password = new_password

# Establish connection to XNAT with token username and password
print("\nConnecting to: " + args.server)
xnat_access = XnatAccess(args.server, args.username, args.password)

# Establish project
xnat_access.project=args.project
print("\nEstablished current project: " + xnat_access.project)

# Establish subject
xnat_access.subject=args.subject
mpp_parameters.subject=xnat_access.subject

# Validate appropriate MR session exists and establish session
session_label_for_processing = xnat_access.subject + args.session_suffix
session_type = xnat_access.get_session_type(session_label_for_processing)

if session_type != PROCESSING_SESSION_TYPE:
    print("Session: " + session_label_for_processing + " is not of correct session type.")
    sys.exit(1)

xnat_access.session = session_label_for_processing
mpp_parameters.session = xnat_access.session
mpp_parameters.xnat_session_id = xnat_access.xnat_session_id

# Gather structural preprocessing parameters if required
if (args.structural):
    print("\nDetermining parameters for Structural Preprocessing")
    mpp_parameters.set_launch_structural()
    mpp_parameters.fieldmap_type = args.fieldmaps

    # Determine parameters related to first T1w scan
    if (xnat_access.does_resource_exist(FIRST_T1W_UNPROC_RESOURCE_NAME)) :
        xnat_access.resource = FIRST_T1W_UNPROC_RESOURCE_NAME
        file_name_to_scan_number = create_resource_file_name_to_scan_number_map(xnat_access)
        
        # Set parameter values for the first T1w scan
        file_name = xnat_access.session + '_' + FIRST_T1W_FILE_NAME_BASE + COMPRESSED_NIFTI_EXTENSION
        scan_number = file_name_to_scan_number[file_name]
        series_description = xnat_access.get_scan_data_field_value(scan_number, 'series_description')
        mpp_parameters.set_first_t1w(file_name, scan_number, series_description)

        if mpp_parameters.fieldmap_type == "GE":
            # Set parameter values for the magnitude field map for the first T1w scan
            file_name = xnat_access.session + '_' + MAG_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            deltaTE = xnat_access.get_scan_data_field_value(scan_number, 'parameters/deltaTE')
            mpp_parameters.set_first_t1w_magfieldmap(file_name, scan_number, deltaTE)

            # Set parameter values for the phase field map for the first T1w scan
            file_name = xnat_access.session + '_' + PHASE_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            mpp_parameters.set_first_t1w_phasefieldmap(file_name, scan_number)

        elif mpp_parameters.fieldmap_type == "SE":
            # Set parameter values for the Positive Spin Echo Field Map (RL)
            file_name = xnat_access.session + '_' + POSITIVE_SPIN_ECHO_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            print("file_name: " + file_name)
            scan_number = file_name_to_scan_number[file_name]            
            print("scan_number: " + scan_number)
            mpp_parameters.set_first_t1w_positive_spin_echo_fieldmap(filename, scan_number)




            # ici mpp_parameters.set_first_t1w_positive_spin_echo_fieldmap(filename, scan_number)

            # Set parameter values for the Negative Spin Echo Field Map (LR)
            file_name = xnat_access.session + '_' + NEGATIVE_SPIN_ECHO_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            print("file_name: " + file_name)
            scan_number = file_name_to_scan_number[file_name]
            print("scan_number: " + scan_number)
            # ici mpp_parameters.set_first_t1w_negative_spin_echo_fieldmap(filename, scan_number)

        else:
            print("ERROR: Unrecognized fieldmap type: " + mpp_parameters.fieldmap_type)
            exit(1)
            
    # Determine parameters related to second T1w scan
    if (xnat_access.does_resource_exist(SECOND_T1W_UNPROC_RESOURCE_NAME)):
        xnat_access.resource = SECOND_T1W_UNPROC_RESOURCE_NAME
        file_name_to_scan_number = create_resource_file_name_to_scan_number_map(xnat_access)

        # Set parameter values for the second T1w scan
        file_name = xnat_access.session + '_' + SECOND_T1W_FILE_NAME_BASE + COMPRESSED_NIFTI_EXTENSION
        scan_number = file_name_to_scan_number[file_name]
        series_description = xnat_access.get_scan_data_field_value(scan_number, 'series_description')
        mpp_parameters.set_second_t1w(file_name, scan_number, series_description)

        if mpp_parameters.fieldmap_type == "GE":
            # Set parameter values for the magnitude field map for the second T1w scan
            file_name = xnat_access.session + '_' + MAG_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            deltaTE = xnat_access.get_scan_data_field_value(scan_number, 'parameters/deltaTE')
            mpp_parameters.set_second_t1w_magfieldmap(file_name, scan_number, deltaTE)

            # Set parameter values for the phase field map for the second T1w scan
            file_name = xnat_access.session + '_' + PHASE_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            mpp_parameters.set_second_t1w_phasefieldmap(file_name, scan_number)




    # Determine parameters related to first T2w scan
    if (xnat_access.does_resource_exist(FIRST_T2W_UNPROC_RESOURCE_NAME)):
        xnat_access.resource = FIRST_T2W_UNPROC_RESOURCE_NAME
        file_name_to_scan_number = create_resource_file_name_to_scan_number_map(xnat_access)
        
        # Set parameter values for the first T2w scan
        file_name = xnat_access.session + '_' + FIRST_T2W_FILE_NAME_BASE + COMPRESSED_NIFTI_EXTENSION
        scan_number = file_name_to_scan_number[file_name]
        series_description = xnat_access.get_scan_data_field_value(scan_number, 'series_description')
        mpp_parameters.set_first_t2w(file_name, scan_number, series_description)

        if mpp_parameters.fieldmap_type == "GE":
            # Set parameter values for the magnitude field map for the first T2w scan
            file_name = xnat_access.session + '_' + MAG_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            deltaTE = xnat_access.get_scan_data_field_value(scan_number, 'parameters/deltaTE')
            mpp_parameters.set_first_t2w_magfieldmap(file_name, scan_number, deltaTE)

            # Set parameter values for the phase field map for the first T2w scan
            file_name = xnat_access.session + '_' + PHASE_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            mpp_parameters.set_first_t2w_phasefieldmap(file_name, scan_number)

    # Determine parameters related to second T2w scan
    if (xnat_access.does_resource_exist(SECOND_T2W_UNPROC_RESOURCE_NAME)):
        xnat_access.resource = SECOND_T2W_UNPROC_RESOURCE_NAME
        file_name_to_scan_number = create_resource_file_name_to_scan_number_map(xnat_access)

        # Set parameter values for the second T2w scan
        file_name = xnat_access.session + '_' + SECOND_T2W_FILE_NAME_BASE + COMPRESSED_NIFTI_EXTENSION
        scan_number = file_name_to_scan_number[file_name]
        series_description = xnat_access.get_scan_data_field_value(scan_number, 'series_description')
        mpp_parameters.set_second_t2w(file_name, scan_number, series_description)

        if mpp_parameters.fieldmap_type == "GE":
            # Set parameter values for the magnitude field map for the second T2w scan
            file_name = xnat_access.session + '_' + MAG_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            deltaTE = xnat_access.get_scan_data_field_value(scan_number, 'parameters/deltaTE')
            mpp_parameters.set_second_t2w_magfieldmap(file_name, scan_number, deltaTE)

            # Set parameter values for the phase field map for the second T2w scan
            file_name = xnat_access.session + '_' + PHASE_FIELDMAP_NAME + COMPRESSED_NIFTI_EXTENSION
            scan_number = file_name_to_scan_number[file_name]
            mpp_parameters.set_second_t2w_phasefieldmap(file_name, scan_number)









# Configure parameters for use with MPP

if not mpp_parameters.configure_to_pass_to_mpp():
    print("ERROR: MPP parameters can not be configured for passing to MPP")
    exit(1)







# Show processing parameters
print("")
print("")
mpp_parameters.show_all()
print("")
print("")
mpp_parameters.show_params_to_pass_to_mpp()

exit()






# find FieldMap_Magnitude
T1w_MPR1_UNPROC_RESOURCE_NAME="T1w_MPR1_unproc"
T1w_MPR2_UNPROC_RESOURCE_NAME="T1w_MPR2_unproc"
fieldmap_magnitude_file_name = args.subject + args.session_suffix + "_FieldMap_Magnitude.nii.gz"

fieldmap_magnitude_resource = ""

if xnat_access.does_resource_exist(T1w_MPR1_UNPROC_RESOURCE_NAME) :
    xnat_access.resource = T1w_MPR1_UNPROC_RESOURCE_NAME
    resource_file_name_list = xnat_access.get_resource_file_name_list()
    if fieldmap_magnitude_file_name in resource_file_name_list:
        fieldmap_magnitude_resource = T1w_MPR1_UNPROC_RESOURCE_NAME
        
if fieldmap_magnitude_resource == "" :
    if xnat_access.does_resource_exist(T1w_MPR2_UNPROC_RESOURCE_NAME) :
        xnat_access.resource = T1w_MPR2_UNPROC_RESOURCE_NAME
        resource_file_name_list = xnat_access.get_resource_file_name_list()
        if fieldmap_magnitude_file_name in resource_file_name_list:
            fieldmap_magnitude_resource = T1w_MPR2_UNPROC_RESOURCE_NAME

print("fieldmap_magnitude_resource: " + fieldmap_magnitude_resource)




