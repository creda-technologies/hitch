from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from anchor_sdk.util import (
    validate_email_address as vea,
    validate_phone_number as vpn,
    validate_country_code as vcc
)

# Natural Person Fields
class NaturalPerson(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    additional_name: Optional[str] = None
    address_country_code: Optional[str] = None
    state_or_province: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None
    email_address: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    birth_country_code: Optional[str] = None
    tax_id: Optional[str] = None
    tax_id_name: Optional[str] = None
    occupation: Optional[int] = None
    employer_name: Optional[str] = None
    employer_address: Optional[str] = None
    id_type: Optional[str] = None
    id_country_code: Optional[str] = None
    id_issue_date: Optional[date] = None
    id_expiration_date: Optional[date] = None
    id_number: Optional[str] = None
    photo_id_front: Optional[bytes] = None
    photo_id_back: Optional[bytes] = None
    notary_approval_of_photo_id: Optional[bytes] = None
    ip_address: Optional[str] = None
    photo_proof_residence: Optional[bytes] = None
    sex: Optional[str] = None
    proof_of_income: Optional[bytes] = None
    proof_of_liveness: Optional[bytes] = None
    referral_id: Optional[str] = None

    @validator('email_address')
    def validate_email_address(cls, v):
        if not v: return v
        vea(v)
        return v
    
    @validator('mobile_number')
    def validate_phone_number(cls, v):
        if not v: return v
        vpn(v)
        return v

    @validator('address_country_code')
    def validate_address_country_code(cls,v):
        if not v: return v
        vcc(v, "address")
        return v


# Financial Account Fields
class FinancialAccount(BaseModel):
    bank_account_type: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_number: Optional[str] = None
    bank_phone_number: Optional[str] = None
    bank_branch_number: Optional[str] = None
    clabe_number: Optional[str] = None
    cbu_number: Optional[str] = None
    cbu_alias: Optional[str] = None
    crypto_address: Optional[str] = None
    crypto_memo: Optional[str] = None

# Organization Fields
class Organization(BaseModel):
    name: Optional[str] = Field(None, alias='organization.name')
    VAT_number: Optional[str] = Field(None, alias='organization.VAT_number')
    registration_number: Optional[str] = Field(None, alias='organization.registration_number')
    registration_date: Optional[str] = Field(None, alias='organization.registration_date')
    registered_address: Optional[str] = Field(None, alias='organization.registered_address')
    number_of_shareholders: Optional[int] = Field(None, alias='organization.number_of_shareholders')
    shareholder_name: Optional[str] = Field(None, alias='organization.shareholder_name')
    photo_incorporation_doc: Optional[bytes] = Field(None, alias='organization.photo_incorporation_doc')
    photo_proof_address: Optional[bytes] = Field(None, alias='organization.photo_proof_address')
    address_country_code: Optional[str] = Field(None, alias='organization.address_country_code')
    state_or_province: Optional[str] = Field(None, alias='organization.state_or_province')
    city: Optional[str] = Field(None, alias='organization.city')
    postal_code: Optional[str] = Field(None, alias='organization.postal_code')
    director_name: Optional[str] = Field(None, alias='organization.director_name')
    website: Optional[str] = Field(None, alias='organization.website')
    email: Optional[str] = Field(None, alias='organization.email')
    phone: Optional[str] = Field(None, alias='organization.phone')

class AcceptsSep9Fields(NaturalPerson, FinancialAccount, Organization):
    pass


class NaturalPersonVerification(BaseModel):
    mobile_number_verification: Optional[str] = None
    email_address_verification: Optional[str] = None
    
    # If your implementation requires other fields to be verified, 
    # add them here following the same pattern.
