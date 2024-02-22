from anchor_sdk.exceptions import Sep9InvalidFieldResponded
from anchor_sdk import SEP9_FIELDS, SEP9_VERIFICATION_FIELDS

class AnchorUser:
    """
    Represents a user in the context of Stellar network interactions, encapsulating account details.

    Attributes:
        account_id (str): The Stellar account ID of the user.
        memo_id (int): An optional memo ID to distinguish transactions for accounts using multiplexed addresses.
        client_domain (str): The domain name of the client application the user is interacting with.

    Args:
        account_id (str): The Stellar account ID.
        memo_id (int, optional): The memo ID associated with transactions. Defaults to 0.
        client_domain (str, optional): The domain of the client application. Defaults to None.
    """
    def __init__(self, account_id: str, memo_id: int = 0, client_domain: str = None):
        self.account_id = account_id
        self.memo_id = int(memo_id)
        self.client_domain = client_domain

class Sep12KycField:
    """
    Defines a KYC field for SEP-12 customer data operations within a Stellar anchor service.

    Attributes:
        field_name (str): The name of the KYC field.
        description (str): A description of the KYC field.
        value (str, optional): The value submitted by the user for this field. Defaults to None.
        is_accepted (bool, optional): Whether the field has been accepted. Defaults to False.
        is_processing (bool, optional): Whether the field is currently being processed. Defaults to False.
        is_rejected (bool, optional): Whether the field has been rejected. Defaults to False.
        requires_verification (bool, optional): Whether the field requires verification. Defaults to False.
        type (str, optional): The type of the field (e.g., "string"). Defaults to "string".
        choices (list[str], optional): A list of choices for the field, if applicable. Defaults to an empty list.

    Args:
        field_name (str): The name of the field.
        description (str): The description of the field.
        value (str, optional): The value of the field. Defaults to None.
        is_accepted (bool, optional): Flag indicating if the field is accepted. Defaults to False.
        is_processing (bool, optional): Flag indicating if the field is under processing. Defaults to False.
        is_rejected (bool, optional): Flag indicating if the field is rejected. Defaults to False.
        requires_verification (bool, optional): Flag indicating if the field requires verification. Defaults to False.
        type (str, optional): The data type of the field. Defaults to "string".
        choices (list[str], optional): Possible choices for the field. Defaults to [].
    """
    def __init__(
        self, 
        field_name,
        description: str = None,
        value: str = None,
        is_accepted: bool = False,
        is_processing: bool = False,
        is_rejected: bool = False,
        requires_verification: bool = False,
        type: str = "string",
        choices: list[str] = []
    ):  
        if not field_name in SEP9_FIELDS and not field_name in SEP9_VERIFICATION_FIELDS:
            raise Sep9InvalidFieldResponded(field_name)
        
        if not type in ["string", "bytes"]:
            raise S

        self.field_name = field_name
        self.description = description
        self.value = value
        self.is_accepted = is_accepted
        self.is_processing = is_processing
        self.is_rejected = is_rejected
        self.requires_verification = requires_verification
        self.type = type
        self.choices = choices
    