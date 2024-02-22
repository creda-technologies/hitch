from fastapi import APIRouter
from anchor_sdk.sep_handlers.sep10_handler import Sep10Handler
from anchor_sdk.sep_handlers.sep12_handler import Sep12Handler
from anchor_sdk.sep_handlers.sep6_handler import Sep6Handler
from anchor_sdk.sep_serializations.sep6_fields import InfoResponse
from fastapi.responses import JSONResponse

class Sep6Endpoints:

    def __init__(
            self,
            router : APIRouter,
            handler : Sep6Handler,
            auth_handler : Sep10Handler,
            kyc_handler : Sep12Handler
    ):
        self.router = router
        self.auth_handler = auth_handler
        self.kyc_handler = kyc_handler
        self.handler = handler

        self.router.add_api_route(
            "/info",
            self.info,
            methods=['GET'],
            response_class=JSONResponse,
            description="Fetch SEP-6 information"
       )
        
        # self.router.add_api_route(
        #     "/deposit",
        #     self.deposit,
        #     methods=['GET'],
        #     response_class=JSONResponse,
        #     description="Create or access a SEP-6 programmatic deposit"
        # )

        # self.router.add_api_route(
        #     "/withdraw",
        #     self.withdraw,
        #     methods=['GET'],
        #     response_class=JSONResponse,
        #     description="Create or access a SEP-6 programmatic withdrawal"
        # )

        # self.router.add_api_route(
        #     "/deposit-exchange",
        #     self.deposit_exchange,
        #     methods=["GET"],
        #     response_class=JSONResponse,
        #     description="Create or access a SEP-6 programmatic deposit between inequivalent assets"
        # )

        # self.router.add_api_route(
        #     "/withdraw-exchange",
        #     self.withdraw_exchange,
        #     methods=["GET"],
        #     response_class=JSONResponse,
        #     description="Create or access a SEP-6 programmatic withdrawal between inequivalent assets"
        # )

        # self.router.add_api_route(
        #     "/fee",
        #     self.handler.fee,
        #     methods=["GET"],
        #     response_class=JSONResponse,
        #     description="Query advanced fee structures for transactions"
        # )

        # self.router.add_api_route(
        #     "/transactions",
        #     self.transactions,
        #     methods=["GET"],
        #     response_class=JSONResponse,
        #     description="Query transactions of an account"
        # )

        # self.router.add_api_route(
        #     "/transaction",
        #     self.transaction,
        #     methods=["GET"],
        #     response_class=JSONResponse,
        #     description="Query transaction details for a particular transaction"
        # )
        
    def info(self, lang : str = "en") -> InfoResponse:
        response = self.handler.info()
        return InfoResponse()

