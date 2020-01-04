from typing import Callable, List, Optional

from typing_extensions import Protocol

from ..utils.types import Event
from .types import Payload


class Action:
    def perform(self, payload: Payload) -> Event:
        """
        ...
        """
        self.validate(payload)
        return self.create_event(payload, 0)

    def validate(self, payload: Payload) -> None:
        """
        ...
        """
        raise NotImplementedError

    def create_event(
        self, payload: Payload, user_id: int, keys: Optional[List] = None
    ) -> Event:
        """
        ...
        """
        raise NotImplementedError


class DatabaseAction(Action):
    def perform(self, payload: Payload) -> Event:
        """
        ...
        """
        self.validate(payload)
        keys = self.read_database(payload, 0)
        return self.create_event(payload, 0)

    def read_database(self, payload: Payload, user_id: int) -> List[str]:
        """
        ...
        """
        raise NotImplementedError  # TODO zweites Protocol
