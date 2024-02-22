from typing import Optional
from pydantic import BaseModel, validator
from anchor_sdk.util import (
    validate_stellar_address as vsa, 
    validate_stellar_account_memo as vsm,
    validate_client_domain as vsd

)

class SepStellarAccountParams(BaseModel):
    account : Optional[str] = None
    memo : Optional[str] = "0"
    client_domain: Optional[str] = None

    @validator('account')
    def validate_stellar_address(cls, v):
        if not v: return v
        vsa(v)
        return v
    
    @validator('memo')
    def validate_account_memo(cls,v):
        if not v: return v
        vsm(v)
        return v
    
    @validator('client_domain')
    def validate_client_domain(cls, v):
        if not v: return v
        vsd(v)
        return v

