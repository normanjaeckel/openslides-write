from abc import ABC

from ..utils.types import Schema


class Model(ABC):
    """
    Abstract base class for models in OpenSlides.
    """

    def get_schema(self, field: str) -> Schema:
        """
        Returns JSON schema for the given field.
        """
        return getattr(self, field).get_schema()
