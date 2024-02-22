from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class AnchorSdkException(Exception):
    """
    Base class for exceptions in the Anchor SDK related to Stellar SEPs.

    This class is intended to be a base for custom exceptions within the SDK, 
    allowing for more granular error handling and response messaging relevant to 
    Stellar network operations and SEPs.

    Attributes:
        status_code (int): HTTP status code associated with the exception.
        error_message (str): Descriptive message detailing the exception.
    """

    def __init__(self, status_code: int, error_message: str):
        """
        Initialize the AnchorSdkException with a status code and an error message.

        Args:
            status_code (int): HTTP status code for the exception.
            error_message (str): Detailed message about the exception.
        """
        self.status_code = status_code
        self.error_message = error_message

    def default_exception_anchor_response(self) -> JSONResponse:
        return JSONResponse(
            content = {
                "error" : self.error_message,
            },
            status_code = self.status_code
        )
    
    def default_validation_parser(exc : RequestValidationError):
        errors = error.errors()
        error_message : str 

        for index, error in enumerate(errors):
            if error['type'] == "json_invalid":
                error_message = "Invalid JSON"
            if error['type'] == "missing":
                if len(error['loc']) > 1:
                    location, field = error['loc']
                    message = error['msg']
                    error_message = f"field '{field}' has issue '{message}"
                    if index != len(errors) - 1:
                        error_message += " | "

                else:
                    error_message = f"missing one or more required fields"
        return JSONResponse(
            content={"error":error_message}
        )



class MethodNotImplementedError(AnchorSdkException):
    """
    Exception raised when a required method is not implemented.

    This exception is specific to cases where a method required for SEP compliance
    or SDK functionality is not implemented, indicating incomplete SDK integration.

    Inherits from AnchorSdkException.

    Attributes:
        status_code (int): HTTP 501 Not Implemented status code.
        error_message (str): Message stating the unimplemented method's name.
    """

    def __init__(self, sep_name : str, event_name: str):
        """
        Initialize the MethodNotImplementedError with the name of the unimplemented method.

        Args:
            event_name (str): The name of the method or event that is not implemented.
        """
        self.status_code = status.HTTP_501_NOT_IMPLEMENTED
        self.error_message = f"'{event_name}' ({sep_name}) has not been implemented"


class Sep10AuthError(AnchorSdkException):
    """
    Exception raised for errors related to SEP-10 authentication.

    This exception is raised in scenarios where SEP-10 (Stellar Web Authentication) 
    procedures fail or encounter issues.

    Inherits from AnchorSdkException.

    Attributes:
        status_code (int): HTTP 401 Unauthorized status code.
        error_message (str): Detailed message about the authentication error.
    """

    def __init__(self, error_message: str):
        """
        Initialize the Sep10AuthError with an error message.

        Args:
            error_message (str): Detailed message about the authentication error.
        """
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.error_message = error_message

3
class Sep12KycError(AnchorSdkException):
    """
    Exception raised for errors related to SEP-12 KYC process.

    SEP-12 pertains to the Know Your Customer (KYC) process in the Stellar network.
    This exception is raised for issues encountered during this process.

    Inherits from AnchorSdkException.

    Attributes:
        status_code (int): HTTP status code specific to the KYC error.
        error_message (str): Detailed message about the KYC error.
    """

    def __init__(self, status_code: int, error_message: str):
        """
        Initialize the Sep12KycError with a status code and an error message.

        Args:
            status_code (int): HTTP status code for the KYC error.
            error_message (str): Detailed message about the KYC error.
        """
        self.status_code = status_code
        self.error_message = error_message


class Sep6TransferError(AnchorSdkException):
    """
    Exception raised for errors related to SEP-6 deposit/withdrawal operations.

    SEP-6 deals with deposit and withdrawal operations in the Stellar network. 
    This exception is used for handling errors specific to these operations.

    Inherits from AnchorSdkException.

    Attributes:
        status_code (int): HTTP status code specific to the transfer error.
        error_message (str): Detailed message about the transfer error.
    """

    def __init__(self, status_code: int, error_message: str):
        """
        Initialize the Sep6TransferError with a status code and an error message.

        Args:
            status_code (int): HTTP status code for the transfer error.
            error_message (str): Detailed message about the transfer error.
        """
        self.status_code = status_code
        self.error_message = error_message

class Sep9FieldsError(AnchorSdkException):
    def __init__(self, field_name : str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.error_message = f"'{field_name}' is not a valid SEP-9 field." 

class Sep9InvalidFieldResponded(AnchorSdkException):
    def __init__(self, field_name : str):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.error_message = f"'{field_name}' is not a valid SEP-9 field, contact the server admin to change it."      

class Sep9InvalidType(AnchorSdkException):
    def __init__(self, type : str):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.error_message = f"'{type}' is not a valid SEP-9 datatype."
