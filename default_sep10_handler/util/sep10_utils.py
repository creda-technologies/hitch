from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.sep.stellar_toml import fetch_stellar_toml
from anchor_sdk.exceptions import Sep10AuthError
from stellar_sdk import Keypair, Network, ManageData, MuxedAccount, Server
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, NotFoundError
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    read_challenge_transaction,
    verify_challenge_transaction_threshold,
    verify_challenge_transaction_signed_by_client_master_key,
)
import jwt

def get_client_signing_key(client_domain):
    client_toml_contents = fetch_stellar_toml(
        client_domain,
        client=RequestsClient(
            request_timeout=3
        ),
    )
    client_signing_key = client_toml_contents.get("SIGNING_KEY")
    if not client_signing_key:
        raise Sep10AuthError(f"Invalid stellar toml at '{client_domain}'")
    try:
        Keypair.from_public_key(client_signing_key)
    except Ed25519PublicKeyInvalidError:
        raise Sep10AuthError(f"Invalid signing key at '{client_domain}'")
    return client_signing_key

def challenge_transaction(
        server_secret,
        client_account,
        web_auth_domain,
        network_passphrase,
        home_domain,
        client_domain=None,
        client_signing_key=None,
        memo=None,
    ):
        """
        Generate the challenge transaction for a client account.
        This is used in `GET <auth>`, as per SEP 10.
        Returns the XDR encoding of that transaction.
        """
        return build_challenge_transaction(
            server_secret=server_secret,
            client_account_id=client_account,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=900,
            client_domain=client_domain,
            client_signing_key=client_signing_key,
            memo=memo,
        )

def validate_challenge_xdr(
        envelope_xdr: str,
        server_account_secret : str,
        web_auth_domain : str,
        network_passphrase : str = Network.TESTNET_NETWORK_PASSPHRASE,
        home_domains : list[str] = [],
        server : Server = Server("https://horizon-testnet.stellar.org")
    ):
    server_account_public_key = Keypair.from_secret(server_account_secret).public_key
    try:
        challenge = read_challenge_transaction(
            challenge_transaction=envelope_xdr,
            server_account_id=server_account_public_key,
            home_domains=home_domains,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
        )
    except (InvalidSep10ChallengeError, TypeError) as e:
        print(e)
        raise Sep10AuthError(f"Invalid Sep10 transaction: {str(e)}")

    client_domain = None
    for operation in challenge.transaction.transaction.operations:
        if (
            isinstance(operation, ManageData)
            and operation.data_name == "client_domain"
        ):
            client_domain = operation.data_value.decode()
            break

    # extract the Stellar account from the muxed account to check for its existence
    stellar_account = challenge.client_account_id
    if challenge.client_account_id.startswith("M"):
        stellar_account = MuxedAccount.from_account(
            challenge.client_account_id
        ).account_id

    try:
        account = server.load_account(stellar_account)
    except NotFoundError:
        try:
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_transaction=envelope_xdr,
                server_account_id=server_account_public_key,
                home_domains=home_domains,
                web_auth_domain=web_auth_domain,
                network_passphrase=network_passphrase,
            )
            if (client_domain and len(challenge.transaction.signatures) != 3) or (
                not client_domain and len(challenge.transaction.signatures) != 2
            ):
                raise Sep10AuthError(
                    "There is more than one client signer on a challenge for an account that doesn't exist"
                )
        except InvalidSep10ChallengeError as e:
            raise Sep10AuthError(f"Missing or invalid signature(s) for {challenge.client_account_id}: {str(e)}")
        else:
            return client_domain

    signers = account.load_ed25519_public_key_signers()
    threshold = account.thresholds.med_threshold
    try:
        signers_found = verify_challenge_transaction_threshold(
            challenge_transaction=envelope_xdr,
            server_account_id=server_account_public_key,
            home_domains=home_domains,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            threshold=threshold,
            signers=signers,
        )
    except InvalidSep10ChallengeError as e:
        raise Sep10AuthError(str(e))

    return client_domain

def generate_jwt(
        server_account_secret : str,
        web_auth_domain : str,
        envelope_xdr: str,
        host_url : str,
        jwt_secret_key : str,
        network_passphrase : str = Network.TESTNET_NETWORK_PASSPHRASE,
        client_domain: str | None = None,
        home_domains : list[str] = [],
    ) -> str:
    """
    Generates the JSON web token from the challenge transaction XDR.

    See: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md#token
    """
    server_account_public_key = Keypair.from_secret(server_account_secret).public_key

    challenge = read_challenge_transaction(
        challenge_transaction=envelope_xdr,
        server_account_id=server_account_public_key,
        home_domains=home_domains,
        web_auth_domain=web_auth_domain,
        network_passphrase=network_passphrase,
    )

    # set iat value to minimum timebound of the challenge so that the JWT returned
    # for a given challenge is always the same.
    # https://github.com/stellar/stellar-protocol/pull/982
    issued_at = challenge.transaction.transaction.preconditions.time_bounds.min_time

    # format sub value based on muxed account or memo
    if challenge.client_account_id.startswith("M") or not challenge.memo:
        sub = challenge.client_account_id
    else:
        sub = f"{challenge.client_account_id}:{challenge.memo}"

    jwt_dict = {
        "iss": host_url + " auth",
        "sub": sub,
        "iat": issued_at,
        "exp": issued_at + 24 * 60 * 60,
        "jti": challenge.transaction.hash().hex(),
        "client_domain": client_domain,
    }
    return jwt.encode(jwt_dict, jwt_secret_key, algorithm="HS256")
