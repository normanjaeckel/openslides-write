import logging
import os
from typing import Iterable, Union

from werkzeug.exceptions import BadRequest, HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.routing import RuleFactory as WerkzeugRuleFactory
from werkzeug.wrappers import Response

from .utils.types import ApplicationConfig, Environment, StartResponse, WSGIEnvironment
from .utils.wrappers import Request
from .views import ActionView

logger = logging.getLogger(__name__)


class RuleFactory(WerkzeugRuleFactory):
    """
    """

    def get_rules(self, map: Map) -> Iterable[Rule]:
        """
        """
        return [
            Rule("/system/api/actions", endpoint="actions", methods=("POST",),),
        ]


class Application:
    """
    Central application container for this service.

    During initialization we bind configuration to the instance and also map
    rule factory's urls.
    """

    def __init__(self, config: ApplicationConfig) -> None:
        self.config = config
        self.environment = config["environment"]
        self.url_map = Map()
        self.url_map.add(RuleFactory())

    def dispatch_request(self, request: Request) -> Union[Response, HTTPException]:
        """
        Dispatches request to single apps according to URL rules. Returns a
        Response object or a HTTPException (both are WSGI applications
        themselves).
        """
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            rule, arguments = adapter.match(return_rule=True)
            logger.debug(f"Found rule {rule} with arguments {arguments}")
            if rule.endpoint == "actions":
                response = ActionView(self.environment).dispatch(request, **arguments)
            else:
                raise BadRequest(".............")  # TODO
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


def get_environment() -> Environment:
    """
    Parses environment variables and sets their defaults if they do not exist.
    """

    database_url = event_store_url = auth_url = os.environ.get(
        "OPENSLIDES_WRITE_SERVICE_EVENT_STORE_URL",
        "http://localhost:9000/",  # TODO: Use correct variables here.
    )
    worker_timeout = int(
        os.environ.get("OPENSLIDES_WRITE_SERVICE_WORKER_TIMEOUT", "30")
    )
    return Environment(
        database_url=database_url,
        event_store_url=event_store_url,
        auth_url = auth_url,
        worker_timeout=worker_timeout,
    )


def create_application() -> Application:
    """
    Application factory function to create a new instance of the application.

    Parses services configuration from environment variables.
    """
    # Setup global loglevel.
    logging.basicConfig(
        level=os.environ.get("OPENSLIDES_WRITE_SERVICE_DEBUG", logging.WARNING)
    )

    logger.debug("Create application")

    environment = get_environment()
    logger.debug(f"Using environment: {environment}")

    # Create application instance.
    application = Application(ApplicationConfig(environment=environment))
    return application
