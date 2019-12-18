from typing import Any, Dict


class EventStore:
    """
    Adapter to connect to event store.
    """

    def __init__(self, event_store_url: str) -> None:
        self.url = event_store_url
        self.headers = {"Content-Type": "application/json"}

    def save(self, data: Dict[str, Any]) -> None:
        pass

    def send(self, data: Dict[str, Any]) -> None:
        pass

    def get_highest_id(self, key: str) -> int:
        """
        Locks inside all events for the highest id for this key. Returns 0 if
        nothing is found.
        """
        return 0
