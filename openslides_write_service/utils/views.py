from ..services.database import Database
from ..services.event_store import EventStore
from .types import Environment


class ViewSet:
    """
    Basic viewset class for all apps.

    During initialization we bind the viewpoint and services to the instance.
    """

    def __init__(self, viewpoint: str, environment: Environment) -> None:
        self.viewpoint = viewpoint
        self.database = Database(environment["database_url"])
        self.event_store = EventStore(environment["event_store_url"])
