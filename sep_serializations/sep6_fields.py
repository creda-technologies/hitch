from typing import Dict, List, Optional
from pydantic import BaseModel

class FieldInfo(BaseModel):
    """
    Describes individual fields required for deposit or withdrawal operations.

    Attributes:
        description: A human-readable description of the field.
        optional: Indicates whether the field is optional. Defaults to False.
        choices: A list of possible values for the field, if applicable.

    Example:
        {
            "description": "your email address for transaction status updates",
            "optional": True,
            "choices": ["USA", "PRI"]
        }
    """
    description: str
    optional: Optional[bool] = None
    choices: Optional[List[str]] = None

class AssetFields(BaseModel):
    """
    Represents the collection of fields required for processing deposits or withdrawals for a specific asset.

    Attributes are dynamically defined based on the asset's requirements.
    """
    email_address: Optional[FieldInfo] = None
    amount: Optional[FieldInfo] = None
    country_code: Optional[FieldInfo] = None
    type: Optional[FieldInfo] = None

class AssetOperationInfo(BaseModel):
    """
    Defines operation information for deposits or withdrawals of an asset, including status, authentication, limits, and fees.

    Attributes:
        enabled: Indicates if the operation is enabled for this asset.
        authentication_required: Specifies if authentication is needed.
        min_amount: Minimum transaction amount.
        max_amount: Maximum transaction amount.
        fee_fixed: Fixed transaction fee.
        fee_percent: Percentage transaction fee.
        fields: Additional information required for the transaction.

    Example for deposit:
        {
            "enabled": True,
            "authentication_required": True,
            "min_amount": 0.1,
            "max_amount": 1000,
            "fields": {
                "email_address": {
                    "description": "your email address for transaction status updates",
                    "optional": True
                }
            }
        }
    """
    enabled: bool
    authentication_required: Optional[bool] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    fee_fixed: Optional[float] = None
    fee_percent: Optional[float] = None
    fields: Optional[Dict[str, FieldInfo]] = None

class FeeInfo(BaseModel):
    """
    Provides information about fees for transactions.

    Attributes:
        enabled: Indicates if the fee information is provided.
        description: A detailed description of how fees are determined.

    Example:
        {
            "enabled": False,
            "description": "Fees vary from 3 to 7 percent based on the assets transacted and the method by which funds are delivered to or collected by the anchor."
        }
    """
    enabled: bool
    description: Optional[str] = None

class EndpointInfo(BaseModel):
    """
    Describes the availability and authentication requirement of an endpoint.

    Attributes:
        enabled: Indicates if the endpoint is available.
        authentication_required: Indicates if authentication is required to access the endpoint.

    Example:
        {
            "enabled": True,
            "authentication_required": True
        }
    """
    enabled: bool
    authentication_required: Optional[bool] = None

class InfoResponse(BaseModel):
    """
    Represents the complete response from the `/info` endpoint, detailing supported operations, fees, and features.

    Attributes:
        deposit: Supported currencies and their deposit information.
        withdraw: Supported currencies and their withdrawal information.
        fee: Information about transaction fees.
        transactions: Information about the transactions endpoint.
        transaction: Information about the transaction endpoint.
        features: Supported features like account creation and claimable balances.

    Example:
        {
            "deposit": {
                "USD": {
                    "enabled": True,
                    "authentication_required": True,
                    ...
                }
            },
            "withdraw": {
                "USD": {
                    "enabled": True,
                    ...
                }
            },
            "fee": {
                "enabled": False,
                "description": "Fees vary from 3 to 7 percent..."
            },
            "transactions": {
                "enabled": True,
                "authentication_required": True
            },
            "transaction": {
                "enabled": False,
                "authentication_required": True
            },
            "features": {
                "account_creation": True,
                "claimable_balances": True
            }
        }
    """
    deposit: Dict[str, AssetOperationInfo]
    withdraw: Dict[str, AssetOperationInfo]
    fee: FeeInfo
    transactions: EndpointInfo
    transaction: EndpointInfo
    features: Dict[str, bool]

# This file now accurately represents the full structure of the `/info` endpoint response, including all required sections.
