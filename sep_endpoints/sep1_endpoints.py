from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse
from anchor_sdk.sep_handlers.sep1_handler import Sep1Handler

class Sep1Endpoints:
    """
    A class to define and handle SEP-1 related API endpoints using FastAPI.

    This class is responsible for setting up a router for the Stellar network-related
    endpoint(s), specifically for serving the 'stellar.toml' file.

    Attributes:
        handler (Sep1Handler): An instance of Sep1Handler used to handle the logic 
                               for SEP-1 operations.
        router (APIRouter): An instance of APIRouter from FastAPI to define and handle
                            API routes.

    Methods:
        return_toml_data(): Handles the GET request for '/stellar.toml' and returns
                            the TOML data related to Stellar network configuration.
    """

    def __init__(
        self,
        handler: Sep1Handler,
        router: APIRouter
    ):
        """
        Initializes the Sep1Endpoints instance with a handler and router.

        Args:
            handler (Sep1Handler): An instance of Sep1Handler, responsible for 
                                   handling the logic related to SEP-1 operations.
            router (APIRouter): An APIRouter instance from FastAPI, used to define 
                                and manage API routes.
        """
        self.handler = handler
        self.router = router

        # Adding the '/stellar.toml' route to the API router
        self.router.add_api_route(
            "/stellar.toml", 
            self.return_toml_data,
            methods=['GET'],
            response_class=PlainTextResponse
        )

    def return_toml_data(self):
        """
        Handles the GET request for the '/stellar.toml' endpoint.

        This method invokes the `return_toml_data` method of the handler 
        to process and return the Stellar TOML file data.

        Returns:
            A response containing the Stellar TOML data.
        """
        return self.handler.return_toml_data(None)
