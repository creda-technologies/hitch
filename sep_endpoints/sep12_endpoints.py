from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Depends
from anchor_sdk.sep_handlers.sep12_handler import Sep12Handler
from anchor_sdk.sep_serializations.sep12_serializations import (
    CustomerGetRequest,
    CustomerGetResponse,
    CustomerPutRequestBody,
    CustomerPutRequestParams,
    CustomerPutResponse,
    CustomerCallbackPutRequest,
)
from anchor_sdk.exceptions import Sep9FieldsError
from anchor_sdk.models import Sep12KycField
from anchor_sdk.sep_handlers.sep10_handler import Sep10Handler
from anchor_sdk.util import sep12_fields_to_json
from anchor_sdk import SEP9_ALL_FIELDS
class Sep12Endpoints:
    """
    Defines SEP-12 customer endpoint implementations for a Stellar anchor service.

    The class provides API routes for handling SEP-12 customer data, including fetching
    required KYC fields, submitting customer information, and registering callback URLs for webhooks.

    Attributes:
        handler (Sep12Handler): The handler for SEP-12 operations.
        router (APIRouter): FastAPI router object to which API routes are added.
        auth_handler (Sep10Handler): The handler for SEP-10 authentication.

    Methods:
        __init__(self, router: APIRouter, handler: Sep12Handler, auth_handler: Sep10Handler):
            Initializes the SEP-12 endpoints with a router, SEP-12 handler, and SEP-10 authentication handler.
        fetch_required_fields(self, request: Request, fields_request: CustomerGetRequest = Depends()) -> CustomerGetResponse:
            Fetches the required KYC fields for a customer.
        put_customer_fields(self, request: Request, fields_submission: CustomerPutRequest) -> CustomerPutResponse:
            Handles the submission of new or updated customer fields.
        register_callback(self, request: Request, callback_submission: CustomerCallbackPutRequest) -> dict:
            Registers callback URLs for receiving webhooks related to customer data.
    """
    def __init__(self, router: APIRouter, handler: Sep12Handler, auth_handler: Sep10Handler):
        """
        Initializes the SEP-12 endpoints.

        Args:
            router (APIRouter): FastAPI router object for route registration.
            handler (Sep12Handler): Handler for SEP-12 operations.
            auth_handler (Sep10Handler): Handler for SEP-10 authentication.
        """
        self.handler = handler
        self.router = router
        self.auth_handler = auth_handler

        # Register API routes
        self.router.add_api_route(
            "/customer",
            self.fetch_required_fields,
            methods=['GET'],
            description="Get required fields for SEP12 KYC",
            response_class=JSONResponse,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            "/customer",
            self.put_customer_fields,
            methods=["PUT"],
            description="Handle submission for new fields",
            response_class=JSONResponse,
        )

        self.router.add_api_route(
            "/customer/callback",
            self.register_callback,
            methods=['PUT'],
            description="Register callback URLs for webhooks",
        )

    def fetch_required_fields(self, request: Request, fields_request: CustomerGetRequest = Depends()) -> CustomerGetResponse:
        """
        Fetches the required KYC fields for a customer.

        Args:
            request (Request): The FastAPI request object.
            fields_request (CustomerGetRequest, optional): Dependency that extracts customer get request parameters.

        Returns:
            CustomerGetResponse: The response containing required KYC fields for the customer.
        """
        user = self.auth_handler.authenticated_route(request)

        id, message, fields = (
            self.handler.fetch_required_fields(user, fields_request.type) 
            if fields_request.type is not None else
            self.handler.fetch_required_fields(user)
        )

        fields, provided_fields = sep12_fields_to_json(fields)
        
        return_object =  {
            "id" : id,
            "status" : self.get_status_from_fields(fields, provided_fields),
            "message" : message,
        }
        
        if fields: return_object['fields'] = fields
        if provided_fields: return_object['provided_fields'] = provided_fields

        return return_object

    def put_customer_fields(self, request: Request, fields_submission: CustomerPutRequestBody, type : str = None) -> CustomerPutResponse:
        """
        Handles the submission of new or updated customer fields.

        Args:
            request (Request): The FastAPI request object.
            fields_submission (CustomerPutRequest): The submitted customer fields.

        Returns:
            CustomerPutResponse: The response containing the ID of the updated customer.
        """
        user = self.auth_handler.authenticated_route(request)
        fields = {}
        for field, value in fields_submission:
            if field in SEP9_ALL_FIELDS and value:
                fields[field] = value
        
        user_id = (
                self.handler.process_submitted_fields(
                    user, 
                    fields,
                    type
                ) 
                if type is not None else
                self.handler.process_submitted_fields(
                    user, 
                    fields
                )
            )

        return CustomerPutResponse(
            id=user_id
        )


    def register_callback(self, request: Request, callback_submission: CustomerCallbackPutRequest) -> int:
        """
        Registers callback URLs for receiving webhooks related to customer data.

        Args:
            request (Request): The FastAPI request object.
            callback_submission (CustomerCallbackPutRequest): The submitted callback URL data.

        Returns:
            dict: The result of the callback registration operation.
        """
        user = self.auth_handler.authenticated_route(request)

        return self.handler.register_callback_url(
            user=user,
            callback_url=callback_submission.url
        )
    

    @staticmethod
    def get_status_from_fields(fields, provided_fields) -> str:
        if len(fields) > 0:
            return "NEEDS_INFO"
        
        all_statuses = [provided_fields[field]['status'] for field in provided_fields]
        all_fields_rejected = all([status == "REJECTED" for status in all_statuses])

        if all_fields_rejected: return "REJECTED"
        elif (
            ("VERIFICATION_REQUIRED" in all_statuses)
                or 
            (not all_fields_rejected and "REJECTED" in all_statuses)
            ): 
            return "NEEDS_INFO"
        
        elif "PROCESSING" in all_statuses : return "PROCESSING"

        return "ACCEPTED"