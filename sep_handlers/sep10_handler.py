from anchor_sdk.models import AnchorUser
from stellar_sdk import Network, Server
from fastapi import Request
from anchor_sdk.exceptions import MethodNotImplementedError

class Sep10Handler:
    """
    Implements the Stellar SEP-10 protocol for handling authentication. SEP-10 
    provides a standard way to authenticate a user by verifying their Stellar 
    account through a challenge-response process.

    Methods:
        create_challenge_transaction: Creates a challenge transaction for a user.
        verify_challenge_transaction: Verifies a signed challenge transaction.

    Note: This implementation serves as a template and requires specific 
          method implementations.
    """

    def __init__(self):
        pass

    def create_challenge_transaction(self, user: AnchorUser) -> tuple[str, str]:
        """
        Creates a challenge transaction for a given user.

        This method is part of the authentication process in the Stellar network, 
        where the server generates a transaction that the client signs with their 
        private key to prove ownership of their Stellar account.

        Args:
            user (User): The user for whom to create the challenge transaction.

        Returns:
            tuple[str, str]: A tuple containing the challenge transaction in XDR format
                             and the network passphrase of the anchor.

        Raises:
            MethodNotImplementedError: If the method is not implemented.

        Note: This method is a placeholder and needs to be implemented.
        """
        raise MethodNotImplementedError("sep10", "create_challenge_transaction")

    def verify_challenge_transaction(self, envelope_xdr: str) -> str:
        """
        Verifies a challenge transaction signed by the user.

        This method checks if the challenge transaction provided by the client
        was signed correctly and verifies the user's Stellar account.

        Args:
            envelope_xdr (str): The challenge transaction in XDR format to verify.

        Returns:
            str: The result of the verification process.

        Raises:
            MethodNotImplementedError: If the method is not implemented.

        Note: This method is a placeholder and needs to be implemented.
        """
        raise MethodNotImplementedError("sep10", "verify_challenge_transaction")

    def authenticated_route(self, request: Request) -> AnchorUser:
        raise MethodNotImplementedError("sep10", "authenticated_route")

    def _verify_token(self, token : str) -> AnchorUser:
        raise MethodNotImplementedError("sep10", "verify_token_private")
