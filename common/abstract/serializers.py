from typing import Type
import abc

from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from db import Base


class AbstractSerializer(metaclass=abc.ABCMeta):
    """Abstract class for serialization."""

    def __init__(
        self,
        input_schema: Type[Schema] | None = None,
        output_schema: Type[Schema] | None = None,
            ) -> None:
        self.input_schema = input_schema
        self.output_schema = output_schema

    def deserialize(self, data: dict) -> dict:
        """Return deserialized data for self.input_schema."""
        return self._deserialize(data=data)

    def serialize(self, data: Type[Base]) -> dict | list[dict]:
        """Return serialized data for self.output_schema."""
        return self._serialize(data=data)

    @abc.abstractclassmethod
    def _deserialize(self, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _serialize(self, data: Type[Base]) -> None:
        pass


class GenericSerializer(AbstractSerializer):
    """Generic class for serialization."""

    def _deserialize(self, data: dict) -> dict | list[dict]:
        try:
            result = self.input_schema.load(data)
        except ValidationError as err:
            raise err
        return result

    def _serialize(self, data:  Type[Base] | list[Type[Base]]) -> dict | list[dict]:
        try:
            result = self.output_schema.dump(data)
        except ValidationError as err:
            raise err
        return result
