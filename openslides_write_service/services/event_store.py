from typing import Any, Dict


class EventStoreAdapter:
    """
    Adapter to connect to event store.
    """

    def __init__(self, event_store_url: str) -> None:
        self.url = event_store_url
        self.headers = {"Content-Type": "application/json"}

    def send(self, events: List[Dict[str, Any]]) -> None:
        pass
