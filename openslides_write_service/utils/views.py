from ..services.database import Database
from ..services.event_writer import EventWriter
from ..services.sequencer import Sequencer
from .types import ServicesConfig


class ViewSet:
    """
    Basic viewset class for all apps.

    During initialization we bind the viewpoint and services to the instance.
    """

    def __init__(self, viewpoint: str, services: ServicesConfig) -> None:
        self.viewpoint = viewpoint
        self.database = Database(services["database"])
        self.sequencer = Sequencer(services["sequencer"])
        self.event_writer = self.database
