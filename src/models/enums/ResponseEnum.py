from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILS = "file_upload_fails"
    PROCESSING_SUCCESSED = "processing_successed"
    PROCESSING_FAILED = "processing_failed"
    NO_FILES_ERROR = "no_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
