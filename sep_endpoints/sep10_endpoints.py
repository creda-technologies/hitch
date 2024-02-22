from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from anchor_sdk.sep_handlers.sep10_handler import Sep10Handler
from anchor_sdk.models import AnchorUser
from anchor_sdk.sep_serializations.sep10_serializations import (
    ChallengeRequest,
    ChallengeResponse,
    TokenRequest,
    TokenResponse
)

class Sep10Endpoints:
    """
    Provides API endpoints for SEP-10 challenge transaction creation and verification.

    This class is utilized in a FastAPI application to define routes handling SEP-10
    operations. It leverages an instance of `Sep10Handler` for processing the underlying
    SEP-10 authentication logic.

    Attributes:
        handler (Sep10Handler): Handler for SEP-10 operations.
        router (APIRouter): FastAPI router object for adding API routes.

    Args:
        handler (Sep10Handler): A handler instance responsible for SEP-10 logic.
        router (APIRouter): A router instance for setting up API routes.
    """

    def __init__(self, handler: Sep10Handler, router: APIRouter):
        """
        Constructs a `Sep10Endpoints` instance with specified handler and router.

        Args:
            handler (Sep10Handler): The handler responsible for SEP-10 logic.
            router (APIRouter): The router for adding API endpoints.
        """
        self.handler = handler
        self.router = router

        self.router.add_api_route(
            "", 
            self.create_challenge_transaction,
            methods=['GET'],
            response_class=JSONResponse,
            description="Create a SEP-10 challenge transaction"
        )

        self.router.add_api_route(
            "", 
            self.verify_challenge_transaction,
            methods=['POST'],
            response_class=JSONResponse,
            description="Submit a SEP-10 challenge transaction for authentication JWT"
        )

    def create_challenge_transaction(self, transaction_request: ChallengeRequest = Depends()) -> ChallengeResponse:
        """
        Endpoint to create a SEP-10 challenge transaction.

        This GET API endpoint generates a new SEP-10 challenge transaction using the
        handler's `create_challenge_transaction` method.

        Args:
            transaction_request (ChallengeRequest): A request object with challenge transaction details.

        Returns:
            ChallengeResponse: A response object containing the challenge transaction and network passphrase.
        """
        user = AnchorUser(
            account_id=transaction_request.account,
            memo_id=transaction_request.memo,
            client_domain=transaction_request.client_domain
        )

        transaction, network_passphrase = self.handler.create_challenge_transaction(user)

        return ChallengeResponse(
            transaction=transaction,
            network_passphrase=network_passphrase
        )
    
    def verify_challenge_transaction(self, token_request: TokenRequest) -> TokenResponse:
        """
        Endpoint to verify a SEP-10 challenge transaction.

        This POST API endpoint verifies a provided SEP-10 challenge transaction using the
        handler's `verify_challenge_transaction` method.

        Args:
            token_request (TokenRequest): A request object containing the signed challenge transaction.

        Returns:
            TokenResponse: A response object containing the authentication JWT upon successful verification.
        """
        token = self.handler.verify_challenge_transaction(
            envelope_xdr=token_request.transaction
        )

        return TokenResponse(
            token=token
        )
