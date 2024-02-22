from typing import Optional, Dict, List
from pydantic import BaseModel, HttpUrl
from anchor_sdk.sep_serializations.sep9_fields import NaturalPerson, NaturalPersonVerification
from anchor_sdk.sep_serializations.common import SepStellarAccountParams

class CustomerGetRequest(SepStellarAccountParams):
    id: Optional[str] = None
    type: Optional[str] = None
    lang: Optional[str] = None

class FieldInfo(BaseModel):
    description: str
    type: str
    choices: Optional[List[str]] = None
    optional: Optional[bool] = None

class ProvidedFieldInfo(FieldInfo):
    status: Optional[str]
    error: Optional[str] = None

class CustomerGetResponse(BaseModel):
    id: Optional[str]
    status: str
    fields: Optional[Dict[str, FieldInfo]] = None
    provided_fields: Optional[Dict[str, ProvidedFieldInfo]] = None
    message: Optional[str] = None

class CustomerPutRequestParams(
    SepStellarAccountParams
):
    id: Optional[str] = None
    type: Optional[str] = None


class CustomerPutRequestBody(
    NaturalPerson, 
    NaturalPersonVerification, 
):
    pass
    # Additional SEP-9 fields as needed


class CustomerPutResponse(BaseModel):
    id: str

class CustomerCallbackPutRequest(SepStellarAccountParams):
    id : Optional[str] = None
    url : HttpUrl
