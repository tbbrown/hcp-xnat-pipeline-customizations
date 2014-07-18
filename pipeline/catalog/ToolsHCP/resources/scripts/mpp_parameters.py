
class MppParameters(object):
    """
    Class for containing and managing parameters for the Minimal PreProcessing (MPP) pipeline.
    This class:
    * Maintains a set of key values for parameters that need to be specified to invoke the MPP
    * Maintains a key-value mapping used to keep track of the currently set values for the parameters
    * Provides a set set of methods for setting and getting the MPP invocation parameters
    * Exposes those getter and setter methods to make the parameters properties of this class
    * Provides methods for validating the parameter settings
    """

    _VALUE_FALSE = '0'
    _VALUE_TRUE = '1'
    _VALUE_UNSET = 'N/A'

    _KEY_SUBJECT = 'subject'
    _KEY_SESSION_ID = 'sessionId'
    _KEY_XNAT_ID = 'xnat_id'
    _KEY_LAUNCH_STRUCTURAL = 'launchStructural'
    _KEY_LAUNCH_DIFFUSION = 'launchDiffusion'
    _KEY_FIELDMAP_TYPE = 'fieldmap_type'

    # Keys for parameters that apply to the first T1w scan
    _KEY_FIRST_T1W_FILE_NAME = 'structural_t1name_1'
    _KEY_FIRST_T1W_SCAN_NUMBER = 'structural_t1scanid_1'
    _KEY_FIRST_T1W_SERIES_DESC = 'structural_t1seriesdesc_1'

    _KEY_FIRST_T1W_MAGFIELDMAP_FILE_NAME = 'structural_t1magscanname_1'
    _KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER = 'structural_t1magscanid_1'
    _KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE = 'structural_t1magscan_te_1'

    _KEY_FIRST_T1W_PHASEFIELDMAP_FILE_NAME = 'structural_t1phascanname_1'
    _KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER = 'structural_t1phascanid_1'

    # Keys for parameters that apply to the second T1w scan
    _KEY_SECOND_T1W_FILE_NAME = 'structural_t1name_2'
    _KEY_SECOND_T1W_SCAN_NUMBER = 'structural_t1scanid_2'
    _KEY_SECOND_T1W_SERIES_DESC = 'structural_t1seriesdesc_2'

    _KEY_SECOND_T1W_MAGFIELDMAP_FILE_NAME = 'structural_t1magscanname_2'
    _KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER = 'structural_t1magscanid_2'
    _KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE = 'structural_t1magscan_te_2'

    _KEY_SECOND_T1W_PHASEFIELDMAP_FILE_NAME = 'structural_t1phascanname_2'
    _KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER = 'structural_t1phascanid_2'

    # Keys for parameters that apply to the first T2w scan
    _KEY_FIRST_T2W_FILE_NAME = 'structural_t2name_1'
    _KEY_FIRST_T2W_SCAN_NUMBER = 'structural_t2scanid_1'
    _KEY_FIRST_T2W_SERIES_DESC = 'structural_t2seriesdesc_1'

    _KEY_FIRST_T2W_MAGFIELDMAP_FILE_NAME = 'structural_t2magscanname_1'
    _KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER = 'structural_t2magscanid_1'
    _KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE = 'structural_t2magscan_te_1'

    _KEY_FIRST_T2W_PHASEFIELDMAP_FILE_NAME = 'structural_t2phascanname_1'
    _KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER = 'structural_t2phascanid_1'

    # Keys for parameters that apply to the second T2w scan
    _KEY_SECOND_T2W_FILE_NAME = 'structural_t2name_2'
    _KEY_SECOND_T2W_SCAN_NUMBER = 'structural_t2scanid_2'
    _KEY_SECOND_T2W_SERIES_DESC = 'structural_t2seriesdesc_2'

    _KEY_SECOND_T2W_MAGFIELDMAP_FILE_NAME = 'structural_t2magscanname_2'
    _KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER = 'structural_t2magscanid_2'
    _KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE = 'structural_t2magscan_te_2'

    _KEY_SECOND_T2W_PHASEFIELDMAP_FILE_NAME = 'structural_t2phascanname_2'
    _KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER = 'structural_t2phascanid_2'

    # Keys for parameters that apply to all structural (T1w and T2w) scans
    _KEY_MAGFIELDMAP_FILE_NAME = 'structural_magscanname'
    _KEY_MAGFIELDMAP_SCAN_NUMBER = 'structural_magscanid'
    _KEY_PHASEFIELDMAP_FILE_NAME = 'structural_phascanname'
    _KEY_PHASEFIELDMAP_SCAN_NUMBER = 'structural_phascanid'
    _KEY_DELTA_TE = 'structural_TE'
    _KEY_AVGRDMETHOD = 'structural_Avgrdcmethod'

    def _initialize_parameters(self):
        self._parameters[self._KEY_SUBJECT] = self._VALUE_UNSET
        self._parameters[self._KEY_SESSION_ID] = self._VALUE_UNSET
        self._parameters[self._KEY_XNAT_ID] = self._VALUE_UNSET
        self._parameters[self._KEY_LAUNCH_STRUCTURAL] = self._VALUE_FALSE
        self._parameters[self._KEY_LAUNCH_DIFFUSION] = self._VALUE_FALSE
        self._parameters[self._KEY_FIELDMAP_TYPE] = self._VALUE_UNSET
        self._parameters[self._KEY_AVGRDMETHOD] = self._VALUE_UNSET

        # parameters that apply to the first T1w scan
        self._parameters[self._KEY_FIRST_T1W_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T1W_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T1W_SERIES_DESC] = self._VALUE_UNSET

        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE] = self._VALUE_UNSET

        self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET

        # parameters that apply to the second T1w scan
        self._parameters[self._KEY_SECOND_T1W_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T1W_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T1W_SERIES_DESC] = self._VALUE_UNSET

        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE] = self._VALUE_UNSET

        self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET

        # parameters that apply to the first T2w scan
        self._parameters[self._KEY_FIRST_T2W_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T2W_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T2W_SERIES_DESC] = self._VALUE_UNSET

        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE] = self._VALUE_UNSET

        self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET

        # parameters that apply to the second T2w scan
        self._parameters[self._KEY_SECOND_T2W_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T2W_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T2W_SERIES_DESC] = self._VALUE_UNSET

        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE] = self._VALUE_UNSET

        self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET

        # parameters that apply to all structural (T1w and T2w) scans
        self._parameters[self._KEY_MAGFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_MAGFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET
        self._parameters[self._KEY_PHASEFIELDMAP_FILE_NAME] = self._VALUE_UNSET
        self._parameters[self._KEY_PHASEFIELDMAP_SCAN_NUMBER] = self._VALUE_UNSET

    def _format_parameter(self, key):
        sep = " : "
        return str(key) + sep + str(self._parameters[key])

    def show_all(self):
        pre = "\t"
        pre2 = "\t\t"

        print("\nMPP Processing Parameters")
        print(pre + self._format_parameter(self._KEY_SUBJECT))
        print(pre + self._format_parameter(self._KEY_SESSION_ID))
        print(pre + self._format_parameter(self._KEY_XNAT_ID))
        print(pre + self._format_parameter(self._KEY_FIELDMAP_TYPE))

        print(pre + self._format_parameter(self._KEY_LAUNCH_STRUCTURAL))

        # parameters that apply to the first T1w scan
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_SERIES_DESC))

        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_MAGFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE))
        
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_PHASEFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER))

        # parameters that apply to the second T1w scan
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_SERIES_DESC))

        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_MAGFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE))

        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_PHASEFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER))

        # parameters that apply to the first T2w scan
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_SERIES_DESC))

        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_MAGFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE))

        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_PHASEFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER))

        # parameters that apply to the second T2w scan
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_SERIES_DESC))

        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_MAGFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE))

        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_PHASEFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER))

        # parameters that apply to all structural (T1w and T2w) scans
        print(pre2 + self._format_parameter(self._KEY_MAGFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_MAGFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_PHASEFIELDMAP_FILE_NAME))
        print(pre2 + self._format_parameter(self._KEY_PHASEFIELDMAP_SCAN_NUMBER))
        print(pre2 + self._format_parameter(self._KEY_AVGRDMETHOD))

        print(pre + self._format_parameter(self._KEY_LAUNCH_DIFFUSION))

    def show_params_to_pass_to_mpp(self):
        sep = " : "
        print(self._format_parameter(self._KEY_XNAT_ID))
        print(self._format_parameter(self._KEY_SUBJECT))
        print(self._format_parameter(self._KEY_SESSION_ID))
        print(self._format_parameter(self._KEY_LAUNCH_STRUCTURAL))
        print(self._format_parameter(self._KEY_MAGFIELDMAP_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_PHASEFIELDMAP_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_FIRST_T1W_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_FIRST_T1W_SERIES_DESC))
        print(self._format_parameter(self._KEY_SECOND_T1W_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_SECOND_T1W_SERIES_DESC))
        print(self._format_parameter(self._KEY_FIRST_T2W_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_FIRST_T2W_SERIES_DESC))
        print(self._format_parameter(self._KEY_SECOND_T2W_SCAN_NUMBER))
        print(self._format_parameter(self._KEY_SECOND_T2W_SERIES_DESC))
        print(self._format_parameter(self._KEY_DELTA_TE))
        print(self._format_parameter(self._KEY_AVGRDMETHOD))

    def __init__(self):
        super(MppParameters, self).__init__()
        self._parameters = dict()
        self._initialize_parameters()

    def get_subject(self):
        return self._parameters[self._KEY_SUBJECT]

    def set_subject(self, new_subject):
        self._parameters[self._KEY_SUBJECT] = new_subject

    subject=property(get_subject, set_subject)

    def get_session(self):
        return self._parameters[self._KEY_SESSION_ID]

    def set_session(self, new_session):
        self._parameters[self._KEY_SESSION_ID] = new_session

    session=property(get_session, set_session)

    def get_xnat_session_id(self):
        return self._parameters[self._KEY_XNAT_ID]

    def set_xnat_session_id(self, new_xnat_session_id):
        self._parameters[self._KEY_XNAT_ID] = new_xnat_session_id

    xnat_session_id=property(get_xnat_session_id, set_xnat_session_id)

    def set_launch_structural(self):
        self._parameters[self._KEY_LAUNCH_STRUCTURAL] = self._VALUE_TRUE

    def set_do_not_launch_structural(self):
        self._parameters[self._KEY_LAUNCH_STRUCTURAL] = self._VALUE_FALSE

    def set_fieldmap_type(self, new_fieldmap_type):
        if new_fieldmap_type == "GE":
            self._parameters[self._KEY_FIELDMAP_TYPE] = new_fieldmap_type
            self._parameters[self._KEY_AVGRDMETHOD] = "FIELDMAP"
        elif new_fieldmap_type == "SE":
            self._parameters[self._KEY_FIELDMAP_TYPE] = new_fieldmap_type
            self._parameters[self._KEY_AVGRDMETHOD] = "TOPUP"
        else:
            print("Unrecognized fieldmap type specification")

    def get_fieldmap_type(self):
        return self._parameters[self._KEY_FIELDMAP_TYPE]

    fieldmap_type=property(get_fieldmap_type, set_fieldmap_type)

    def set_first_t1w(self, new_file_name, new_scan_number, new_series_desc):
        self._parameters[self._KEY_FIRST_T1W_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T1W_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_FIRST_T1W_SERIES_DESC] = new_series_desc

    def set_first_t1w_magfieldmap(self, new_file_name, new_scan_number, new_delta_te):
        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE] = new_delta_te

    def set_first_t1w_phasefieldmap(self, new_file_name, new_scan_number):
        self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER] = new_scan_number
    
    def set_second_t1w(self, new_file_name, new_scan_number, new_series_desc):
        self._parameters[self._KEY_SECOND_T1W_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T1W_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_SECOND_T1W_SERIES_DESC] = new_series_desc

    def set_second_t1w_magfieldmap(self, new_file_name, new_scan_number, new_delta_te):
        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE] = new_delta_te

    def set_second_t1w_phasefieldmap(self, new_file_name, new_scan_number):
        self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER] = new_scan_number

    def _is_first_t1w_set(self):
        if (self._parameters[self._KEY_FIRST_T1W_FILE_NAME] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_FIRST_T1W_SCAN_NUMBER] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_FIRST_T1W_SERIES_DESC] == self._VALUE_UNSET): 
            return False
        else:
            return True

    def _is_second_t1w_set(self):
        if (self._parameters[self._KEY_SECOND_T1W_FILE_NAME] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_SECOND_T1W_SCAN_NUMBER] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_SECOND_T1W_SERIES_DESC] == self._VALUE_UNSET):
            return False
        else:
            return True

    def get_T1w_count(self):
        count = 0
        if self._is_first_t1w_set():
            count += 1
        if self._is_second_t1w_set():
            count += 1
        return count

    def set_first_t2w_magfieldmap(self, new_file_name, new_scan_number, new_delta_te):
        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE] = new_delta_te

    def set_first_t2w_phasefieldmap(self, new_file_name, new_scan_number):
        self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER] = new_scan_number

    def set_second_t2w_magfieldmap(self, new_file_name, new_scan_number, new_delta_te):
        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE] = new_delta_te

    def set_second_t2w_phasefieldmap(self, new_file_name, new_scan_number):
        self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER] = new_scan_number

    def _is_first_t2w_set(self):
        if (self._parameters[self._KEY_FIRST_T2W_FILE_NAME] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_FIRST_T2W_SCAN_NUMBER] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_FIRST_T2W_SERIES_DESC] == self._VALUE_UNSET):
            return False
        else:
            return True

    def _is_second_t2w_set(self):
        if (self._parameters[self._KEY_SECOND_T2W_FILE_NAME] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_SECOND_T2W_SCAN_NUMBER] == self._VALUE_UNSET) or \
                (self._parameters[self._KEY_SECOND_T2W_SERIES_DESC] == self._VALUE_UNSET):
            return False
        else:
            return True

    def get_T2w_count(self):
        count = 0
        if self._is_first_t2w_set():
            count += 1
        if self._is_second_t2w_set():
            count += 1
        return count

    def validate_params(self):
        if (self._parameters[self._KEY_LAUNCH_STRUCTURAL] == self._VALUE_TRUE):
            # Must have at least one T1w scan
            if self.get_T1w_count() < 1:
                print("Parameter Validation Error: No T1w scans set")
                return False

            # If there are 2 T1w scans
            if self.get_T1w_count() > 1:
                # they must have the same magnitude fieldmap scan number
                if (self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER] != \
                        self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER]):
                    print("Parameter Validation Error: First and second T1w scans do not have the same magnitude field map")
                    return False
                # they must have the same phase fieldmap scan number
                if (self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER] != \
                        self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER]):
                    print("Parameter Validation Error: First and second T1w scans do not have the same phase field map")
                    return False

            # Must have at least one T2w scan
            if self.get_T2w_count() < 1:
                print("Parameter Validation Error: No T2w scans set")
                return False

            # If there are 2 T2w scans
            if self.get_T2w_count() > 1:
                # they must have the same magnitude fieldmap scan number
                if (self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER] != \
                        self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER]):
                    print("Parameter Validation Error: First and second T2w scans do not have the same magnitude field map")
                    return False
                # they must have the same phase fieldmap scan number
                if (self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER] != \
                        self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER]):
                    print("Parameter Validation Error: First and second T2w scans do not have the same phase field map")
                    return False

            # All the T1w and T2w scans that are set, must have the same magnitude fieldmap
            mag_fieldmap_scan_numbers = list()
            if self._is_first_t1w_set():
                mag_fieldmap_scan_numbers.append(self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER])
            if self._is_second_t1w_set():
                mag_fieldmap_scan_numbers.append(self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER])
            if self._is_first_t2w_set():
                mag_fieldmap_scan_numbers.append(self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER])
            if self._is_second_t2w_set():
                mag_fieldmap_scan_numbers.append(self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER])

            if len(set(mag_fieldmap_scan_numbers)) != 1:
                print("Parameter Validation Error: All T1w and T2w scans that are used must have the same magnitude field map scan number")
                return False

            # All the T1w and T2w scans that are set, must have the same phase fieldmap
            phase_fieldmap_scan_numbers = list()
            if self._is_first_t1w_set():
                phase_fieldmap_scan_numbers.append(self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER])
            if self._is_second_t1w_set():
                phase_fieldmap_scan_numbers.append(self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER])
            if self._is_first_t2w_set():
                phase_fieldmap_scan_numbers.append(self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER])
            if self._is_second_t2w_set():
                phase_fieldmap_scan_numbers.append(self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER])

            if len(set(phase_fieldmap_scan_numbers)) != 1:
                print("Parameter Validation Error: All T1w and T2w scans that are used must have the same phase field map scan number")
                return False

            # All the T1w and T2w scans that are set, must have the same delta TE value
            delta_te_values = list()
            if self._is_first_t1w_set():
                delta_te_values.append(self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE])
            if self._is_second_t1w_set():
                delta_te_values.append(self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE])
            if self._is_first_t2w_set():
                delta_te_values.append(self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE])
            if self._is_second_t2w_set():
                delta_te_values.append(self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE])
                
            if len(set(delta_te_values)) != 1:
                print("Parameter Validation Error: All T1w and T2w scans that are used must have the same delta TE value")
                return False

        return True

    def get_magfieldmap_file_name(self):
        if self._is_first_t1w_set():
            return self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_FILE_NAME]
        elif self._is_second_t1w_set():
            return self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_FILE_NAME]
        elif self._is_first_t2w_set():
            return self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_FILE_NAME]
        elif self._is_second_t2w_set():
            return self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_FILE_NAME]
        else:
            return self._VALUE_UNSET

    def get_magfieldmap_scan_number(self):
        if self._is_first_t1w_set():
            return self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_SCAN_NUMBER]
        elif self._is_second_t1w_set():
            return self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_SCAN_NUMBER]
        elif self._is_first_t2w_set():
            return self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_SCAN_NUMBER]
        elif self._is_second_t2w_set():
            return self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_SCAN_NUMBER]
        else:
            return self._VALUE_UNSET

    def get_phasefieldmap_file_name(self):
        if self._is_first_t1w_set():
            return self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_FILE_NAME]
        elif self._is_second_t1w_set():
            return self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_FILE_NAME]
        elif self._is_first_t2w_set():
            return self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_FILE_NAME]
        elif self._is_second_t2w_set():
            return self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_FILE_NAME]
        else:
            return self._VALUE_UNSET

    def get_phasefieldmap_scan_number(self):
        if self._is_first_t1w_set():
            return self._parameters[self._KEY_FIRST_T1W_PHASEFIELDMAP_SCAN_NUMBER]
        elif self._is_second_t1w_set():
            return self._parameters[self._KEY_SECOND_T1W_PHASEFIELDMAP_SCAN_NUMBER]
        elif self._is_first_t2w_set():
            return self._parameters[self._KEY_FIRST_T2W_PHASEFIELDMAP_SCAN_NUMBER]
        elif sefl._is_second_t2w_set():
            return self._parameters[self._KEY_SECOND_T2W_PHASEFIELDMAP_SCAN_NUMBER]
        else:
            return self._VALUE_UNSET

    def get_delta_te(self):
        if self._is_first_t1w_set():
            return self._parameters[self._KEY_FIRST_T1W_MAGFIELDMAP_DELTA_TE]
        elif self._is_second_t1w_set():
            return self._parameters[self._KEY_SECOND_T1W_MAGFIELDMAP_DELTA_TE]
        elif self._is_first_t2w_set():
            return self._parameters[self._KEY_FIRST_T2W_MAGFIELDMAP_DELTA_TE]
        elif sefl._is_second_t2w_set():
            return self._parameters[self._KEY_SECOND_T2W_MAGFIELDMAP_DELTA_TE]
        else:
            return self._VALUE_UNSET
        
    def configure_to_pass_to_mpp(self):
        if not self.validate_params():
            print("ERROR: MPP parameters do not pass validation checks")
            return False

        # Establish parameters that apply to all structural (T1w and T2w) scans
        self._parameters[self._KEY_MAGFIELDMAP_FILE_NAME] = self.get_magfieldmap_file_name()
        self._parameters[self._KEY_MAGFIELDMAP_SCAN_NUMBER] = self.get_magfieldmap_scan_number()

        self._parameters[self._KEY_PHASEFIELDMAP_FILE_NAME] = self.get_phasefieldmap_file_name()
        self._parameters[self._KEY_PHASEFIELDMAP_SCAN_NUMBER] = self.get_phasefieldmap_scan_number()

        self._parameters[self._KEY_DELTA_TE] = self.get_delta_te()

        return True

    def set_first_t2w(self, new_file_name, new_scan_number, new_series_desc):
        self._parameters[self._KEY_FIRST_T2W_FILE_NAME] = new_file_name
        self._parameters[self._KEY_FIRST_T2W_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_FIRST_T2W_SERIES_DESC] = new_series_desc

    def set_second_t2w(self, new_file_name, new_scan_number, new_series_desc):
        self._parameters[self._KEY_SECOND_T2W_FILE_NAME] = new_file_name
        self._parameters[self._KEY_SECOND_T2W_SCAN_NUMBER] = new_scan_number
        self._parameters[self._KEY_SECOND_T2W_SERIES_DESC] = new_series_desc



