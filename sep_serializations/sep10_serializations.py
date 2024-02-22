from pydantic import BaseModel, Field
from typing import Optional
from anchor_sdk.sep_serializations.common import SepStellarAccountParams

class ChallengeRequest(SepStellarAccountParams):
    account : str
    home_domain: Optional[str] = Field(None, description="Optional home domain of the client")
    
# Challenge Response
class ChallengeResponse(BaseModel):
    transaction: str
    network_passphrase: str = Field(None, description="Optional but recommended Stellar network passphrase")

# Token Request
class TokenRequest(BaseModel):
    transaction: str = Field(..., description="Base64 encoded signed challenge transaction XDR")

# Token Response
class TokenResponse(BaseModel):
    token: str