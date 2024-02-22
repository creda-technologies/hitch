from fastapi import Request
from anchor_sdk.models import AnchorUser
from anchor_sdk.exceptions import Sep10AuthError, MethodNotImplementedError
from anchor_sdk.sep_handlers.sep10_handler import Sep10Handler
from anchor_sdk.default_sep10_handler.util.sep10_utils import (
    get_client_signing_key,
    challenge_transaction,
    validate_challenge_xdr,
    generate_jwt
)
from stellar_sdk import Network, Server
from fastapi import Request

from stellar_sdk.sep.exceptions import (
    InvalidSep10ChallengeError,
    StellarTomlNotFoundError,
)
import toml
import jwt
from jwt import (
    ExpiredSignatureError,
    DecodeError,
    InvalidAlgorithmError,
    InvalidSignatureError
)

class DefaultSep10Handler(Sep10Handler):

    def __init__(
        self,
        jwt_secret_key : str,
        sep10_signing_key : str,
        web_auth_domain : str,
        home_domain : str,
        host_url : str,
        allowed_client_domains : list[str] = [],
        client_attribution_required : bool = False,
        network_passphrase : str = Network.TESTNET_NETWORK_PASSPHRASE,
        server: Server = Server("https://horizon-testnet.stellar.org")
    ):
        self.server = server
        self.host_url = host_url
        self.home_domain = home_domain
        self.jwt_secret_key = jwt_secret_key
        self.web_auth_domain = web_auth_domain
        self.sep10_signing_key = sep10_signing_key
        self.network_passphrase = network_passphrase
        self.allowed_client_domains = allowed_client_domains
        self.client_attribution_required = client_attribution_required


    def create_challenge_transaction(self, user: AnchorUser) -> tuple[str, str]:
        memo = user.memo_id
        client_signing_key = None
        account = user.account_id
        client_domain = user.client_domain
        web_auth_domain = self.web_auth_domain
        server_secret_key = self.sep10_signing_key
        network_passphrase = self.network_passphrase
        home_domain = self.home_domain

        sep10_client_domains = self.allowed_client_domains
        sep10_client_attribution_required = self.client_attribution_required
        if sep10_client_attribution_required and not client_domain:
            raise Sep10AuthError("No client domain provided")

        if sep10_client_attribution_required and client_domain not in sep10_client_domains:
            raise Sep10AuthError(f"Client domain '{client_domain}' not allowed")

        if client_domain:
            try:
                client_signing_key = get_client_signing_key(client_domain)
            except (
                ConnectionError,
                StellarTomlNotFoundError,
                toml.decoder.TomlDecodeError,
            ):
                raise Sep10AuthError(f"Unable to fetch '{client_domain}' signing key")
        try:
            transaction = challenge_transaction(
                server_secret_key,
                account,
                web_auth_domain,
                network_passphrase,
                home_domain,
                client_domain,
                client_signing_key,
                memo
            )
            return (transaction, network_passphrase)

        except ValueError as e:
            raise Sep10AuthError(f"Error generating challenge transaction: {e}")

    def verify_challenge_transaction(self, envelope_xdr: str) -> str:
        client_domain = validate_challenge_xdr(
            envelope_xdr=envelope_xdr,
            server_account_secret=self.sep10_signing_key,
            web_auth_domain=self.web_auth_domain,
            network_passphrase=self.network_passphrase,
            home_domains=[self.home_domain]
        )
        token = generate_jwt(
            server_account_secret=self.sep10_signing_key,
            web_auth_domain=self.web_auth_domain,
            envelope_xdr=envelope_xdr,
            host_url=self.host_url,
            jwt_secret_key=self.jwt_secret_key,
            network_passphrase=self.network_passphrase,
            client_domain=client_domain,
            home_domains=[self.home_domain]
        )
        return token

    def authenticated_route(self, request: Request) -> AnchorUser:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise Sep10AuthError("Authorization header missing")

        scheme, _, token = authorization.partition(' ')
        if scheme.lower() != 'bearer':
            raise Sep10AuthError("Invalid authentication scheme")

        # Here, implement your logic to validate the token
        return self._verify_token(token=token)

    def _verify_token(self, token: str) -> AnchorUser:
        try:
            decoded_jwt = jwt.decode(
                token,
                algorithms=['HS256'],
                key=self.jwt_secret_key,
            )

            account_memo_split = decoded_jwt['sub'].split(":")
            account = account_memo_split[0]
            memo = account_memo_split[1] if len(account_memo_split) > 1 else None
            client_domain = decoded_jwt['client_domain']
            if not client_domain in self.allowed_client_domains and self.client_attribution_required:
                raise Sep10AuthError("token was not signed by one of the allowed domains")

            return AnchorUser(
                account_id=account,
                memo_id=memo,
                client_domain=client_domain
            )

        except ExpiredSignatureError:
            raise Sep10AuthError("Token has expired, please re-authenticate")

        except (DecodeError, InvalidSignatureError, InvalidAlgorithmError) as e:
            raise Sep10AuthError("This token is invalid")
