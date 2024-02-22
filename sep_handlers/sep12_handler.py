from anchor_sdk.models import AnchorUser, Sep12KycField
from anchor_sdk.exceptions import MethodNotImplementedError
from anchor_sdk.sep_handlers.sep10_handler import Sep10Handler

class Sep12Handler:
    """
    Handles SEP-12 operations for a Stellar anchor service.

    This class provides methods to interact with customer data, including fetching required KYC fields,
    processing submitted fields, registering callback URLs for webhooks, processing file submissions,
    and deleting user data.

    Methods:
        fetch_required_fields(self, user: User) -> tuple[str, str, str, list[Sep12KycField]]:
            Fetches the required KYC fields for a customer.
        process_submitted_fields(user: User, fields: list[Sep12KycField]) -> str:
            Processes the submitted KYC fields for a customer.
        register_callback_url(user: User, callback_url: str) -> int:
            Registers a callback URL for receiving webhooks.
        process_file_submissions(user: User, files):
            Processes file submissions related to KYC requirements.
        delete_user_data(user: User):
            Deletes all data related to a specific user.

    Note:
        All methods are placeholders and raise a `MethodNotImplementedError` indicating they need to be
        implemented by the developer.
    """
    def fetch_required_fields(self, user: AnchorUser, customer_type : str) -> tuple[
        str,  # user uuid
        str,  # message
        list[Sep12KycField],  # fields
    ]:
        """
        Fetches the required KYC fields for a customer.

        Args:
            user (User): The user for whom KYC fields are being fetched.

        Raises:
            MethodNotImplementedError: Indicates the method is not implemented.

        Returns:
            tuple[str, str, str, list[Sep12KycField]]: User UUID, KYC status, message, and required KYC fields.
        """
        raise MethodNotImplementedError("sep12", "fetch_required_fields")

    def process_submitted_fields(self, user: AnchorUser, fields: dict[str], customer_type : str) -> str:
        """
        Processes the submitted KYC fields for a customer.

        Args:
            user (User): The user for whom KYC fields are submitted.
            fields (list[Sep12KycField]): The KYC fields being submitted.

        Raises:
            MethodNotImplementedError: Indicates the method is not implemented.

        Returns:
            str: The user UUID indicating the operation was successful.
        """
        raise MethodNotImplementedError("sep12", "process_submitted_fields")

    def register_callback_url(self, user: AnchorUser, callback_url: str) -> int:
        """
        Registers a callback URL for receiving webhooks.

        Args:
            user (User): The user for whom the callback URL is registered.
            callback_url (str): The URL to be registered for callbacks.

        Raises:
            MethodNotImplementedError: Indicates the method is not implemented.

        Returns:
            int: The status code indicating the operation was successful.
        """
        raise MethodNotImplementedError("sep12", "register_callback_url")

    def process_file_submissions(self, user: AnchorUser, files, customer_type : str):
        """
        Processes file submissions related to KYC requirements.

        Args:
            user (User): The user submitting the files.
            files: The files being submitted.

        Raises:
            MethodNotImplementedError: Indicates the method is not implemented.
        """
        raise MethodNotImplementedError("sep12", "process_file_submissions")

    def delete_user_data(self, user: AnchorUser):
        """
        Deletes all data related to a specific user.

        Args:
            user (User): The user whose data is to be deleted.

        Raises:
            MethodNotImplementedError: Indicates the method is not implemented.
        """
        raise MethodNotImplementedError("sep12", "delete_user_data")
