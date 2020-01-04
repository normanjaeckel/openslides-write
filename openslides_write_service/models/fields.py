from abc import ABC

from .types import Schema


class Field(ABC):
    """
    Abstract base class for model fields.
    """

    def __init__(self, description: str) -> None:
        self.description = description

    def get_schema(self) -> Schema:
        ...


class IdField(Field):
    def get_schema(self) -> Schema:
        return {
            "description": self.description,
            "type": "integer",
            "minimum": 1,
        }


class CharField(Field):
    def get_schema(self) -> Schema:
        return {
            "description": self.description,
            "type": "string",
            "minLength": 1,
            "maxLength": 256,
        }


class TextField(Field):
    def get_schema(self) -> Schema:
        return {
            "description": self.description,
            "type": "string",
        }


class ManyToManyArrayField(Field):
    def get_schema(self) -> Schema:
        return {
            "description": self.description,
            "type": "array",
            "items": {"type": "integer"},
            "uniqueItems": True,
        }
