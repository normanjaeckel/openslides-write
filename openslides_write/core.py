from typing import Iterable, Union

from fastjsonschema import JsonSchemaException  # type: ignore
from werkzeug.exceptions import BadRequest, HTTPException
from werkzeug.routing import Map
from werkzeug.wrappers import Response

from .topics import Topics
from .utils.types import ApplicationConfig, DBConfig, StartResponse, WSGIEnvironment
from .utils.wrappers import Request

Apps = (Topics,)


class Application:
    """
    Central application container for the module.

    During initialization we bind configuration and database to the instance
    and also map apps's urls.
    """

    def __init__(self, config: ApplicationConfig) -> None:
        self.config = config
        self.db = DBConfig(protocol="http", host="localhost", port=5984, database="foo")
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
        except JsonSchemaException as e:
            return BadRequest(e.message)
        except HTTPException as e:
            return e
        return response

    def wsgi_app(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> Iterable[bytes]:
        """
        Creates Werkzeug's Request object, calls the dispatch_request method and
        evaluate Response object (or HTTPException) as WSGI application.
        """
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> Iterable[bytes]:
        """
        Dispatches request to `wsgi_app` method so that one may apply custom
        middlewares to the application.
        """
        return self.wsgi_app(environ, start_response)


def create_app() -> Application:
    """
    Application factory function to create a new instance of the application.
    """
    app = Application(
        ApplicationConfig(foo="bar")
    )  # TODO: Add configuration for startup such as database configs etc.
    return app
