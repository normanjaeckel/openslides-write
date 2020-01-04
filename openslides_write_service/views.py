from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Request, Response

from .services.database import Database
from .services.event_store import EventStore
from .utils.types import Environment


class ActionView:
    """
    During initialization we bind the viewpoint and services to the instance.
    """

    def __init__(self, environment: Environment) -> None:
        self.database = Database(environment["database_url"])
        self.event_store = EventStore(environment["event_store_url"])

    def dispatch(self, request: Request, **kwargs: dict) -> Response:
        """
        Dispatches request to the viewpoint.
        """
        if not request.is_json:
            raise BadRequest(
                "Wrong media type. Use 'Content-Type: application/json' instead."
            )
        # return getattr(self, self.viewpoint)(request, **kwargs)
        return
