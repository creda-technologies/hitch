from stellar_sdk import Keypair, MuxedAccount
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from anchor_sdk.exceptions import Sep10AuthError, Sep12KycError
from urllib.parse import urlparse
from anchor_sdk.models import Sep12KycField
from validators import domain
import re
import phonenumbers
import pycountry

email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_stellar_address(account_id : str):
    if account_id.startswith("G"):
        try:
            Keypair.from_public_key(account_id).public_key

        except Ed25519PublicKeyInvalidError:
            raise Sep10AuthError(f"Invalid account '{account_id}'")
        
    elif account_id.startswith("M"):
        try:
            MuxedAccount.from_account(account_id)
        except:
            raise Sep10AuthError(f"Invalid Muxed account: '{account_id}'")
        
    else: raise Sep10AuthError("Invalid account")
    
def validate_stellar_account_memo(memo_id : str):
    try:
        int(memo_id)
    except:
        raise Sep10AuthError("Invalid memo")

def validate_client_domain(client_domain : str):
    try:
        if not domain(client_domain):
            raise Sep10AuthError(f"Invalid domain '{client_domain}'")
    except:
        raise Sep10AuthError(f"Invalid domain '{client_domain}'")


def validate_email_address(email : str):
    if email_regex.match(email) is None:
        raise Sep12KycError(400, f"Invalid email: '{email}'")

def validate_phone_number(mobile_number):
    try:
        phonenumbers.parse(mobile_number, None)
    
    except phonenumbers.NumberParseException:
        raise Sep12KycError(400, f"Invalid mobile number: '{mobile_number}'")
    
def validate_country_code(code : str, field = "address"):
    country = pycountry.countries.get(alpha_3=code)
    if country is None:
        raise Sep12KycError(400, f"Invalid {field} country code: '{code}'")
    
def sep12_fields_to_json(fields : list[Sep12KycField]) -> tuple[
    dict, # fields
    dict  # provided fields
]:
    required_fields = {}
    provided_fields = {}
    
    for field in fields:
        field_object = {
            "type" : field.type,
            "description" : field.description
        }

        
        status = None
        if field.is_accepted: status = "ACCEPTED"
        elif field.is_rejected: status = "REJECTED"  
        elif field.is_processing: status = "PROCESSING"
        if field.value and not field.is_accepted and field.requires_verification:
            status = "VERIFICATION_REQUIRED"

        if status:
            field_object['status'] = status
            provided_fields[field.field_name] = field_object

        else:
            if field.choices:
                field_object['choices'] = field.choices
            
            required_fields[field.field_name] = field_object

    return (required_fields, provided_fields)
