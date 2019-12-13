import os
from typing import Iterable, Union
from urllib.parse import urlparse

import redis
from fastjsonschema import JsonSchemaException  # type: ignore
from werkzeug.exceptions import BadRequest, HTTPException
from werkzeug.routing import Map
from werkzeug.wrappers import Response

from .topics import Topics
from .utils.types import (
    ApplicationConfig,
    ServicesConfig,
    StartResponse,
    WSGIEnvironment,
)
from .utils.wrappers import Request

Apps = (Topics,)


class Application:
    """
    Central application container for this service.

    During initialization we bind configuration for services to the instance
    and also map apps's urls.
    """

    def __init__(self, config: ApplicationConfig) -> None:
        self.config = config
        self.services = config["services"]
        self.url_map = Map()
        for App in Apps:
            self.url_map.add(App(self.services))

    def dispatch_request(self, request: Request) -> Union[Response, HTTPException]:
        """
        Dispatches request to single apps according to URL rules. Returns a
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

    Parses services configuration from environment variables.
    """
    # Read environment variables.
    database_url = os.environ.get(
        "OPENSLIDES_WRITE_SERVICE_DATABASE_URL", "http://localhost:8008/get-elements"
    )
    sequencer_url = os.environ.get(
        "OPENSLIDES_WRITE_SERVICE_SEQUENCER_URL", "http://localhost:6379/0"
    )
    event_writer_url = os.environ.get(
        "OPENSLIDES_WRITE_SERVICE_EVENT_WRITER_URL", "http://localhost:8008/save"
    )

    # Parse OPENSLIDES_WRITE_SERVICE_SEQUENCER_URL and initiate connection
    # to redis with it.
    parse_result = urlparse(sequencer_url)
    if not parse_result.hostname or not parse_result.port:
        raise RuntimeError(
            "Bad environment variable OPENSLIDES_WRITE_SERVICE_SEQUENCER_URL."
        )
    redis_sequencer_connection = redis.Redis(
        host=parse_result.hostname,
        port=parse_result.port,
        db=int(parse_result.path.strip("/")),
    )

    application = Application(
        ApplicationConfig(
            services=ServicesConfig(
                database=database_url,
                sequencer=redis_sequencer_connection,
                event_writer=event_writer_url,
            )
        )
    )
    return application
