from typing import Iterable, Union

from fastjsonschema import JsonSchemaException  # type: ignore
from werkzeug.exceptions import BadRequest, HTTPException
from werkzeug.routing import Map
from werkzeug.wrappers import Response

from .topics import Topics
from .utils.types import (
    ApplicationConfig,
    DatabaseConfig,
    StartResponse,
    WSGIEnvironment,
)
from .utils.wrappers import Request

Apps = (Topics,)


class Application:
    """
    Central application container for this service.

    During initialization we bind configuration and database to the instance
    and also map apps's urls.
    """

    def __init__(self, config: ApplicationConfig) -> None:
        self.config = config
        self.db = config["database"]
        self.url_map = Map()
        for App in Apps:
            self.url_map.add(App(self.db))
        super().__init__()

    def dispatch_request(self, request: Request) -> Union[Response, HTTPException]:
        """
        Dispatches request to single apps according to url rules. Returns a
        Response object or a HTTPException (both are WSGI applications
        themselves).
        """
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            rule, arguments = adapter.match(return_rule=True)
            response = rule.view.dispatch(request, **arguments)
        except JsonSchemaException as exception:
            return BadRequest(exception.message)
        except HTTPException as exception:
            return exception
        return response

    def wsgi_application(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> Iterable[bytes]:
        """
        Creates Werkzeug's Request object, calls the dispatch_request method and
        evaluates Response object (or HTTPException) as WSGI application.
        """
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> Iterable[bytes]:
        """
        Dispatches request to `wsgi_application` method so that one may apply
        custom middlewares to the application.
        """
        return self.wsgi_application(environ, start_response)


def create_application() -> Application:
    """
    Application factory function to create a new instance of the application.

    Parses database configuration from environment variables.
    """
    # TODO: Parse database config from environment variables.
    application = Application(
        ApplicationConfig(
            database=DatabaseConfig(protocol="http", host="localhost", port=5984)
        )
    )
    return application
