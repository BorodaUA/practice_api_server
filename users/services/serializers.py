import abc

from marshmallow.exceptions import ValidationError

from users.models import User
from users.schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema

SCHEMA_MAPPING = {
    'GET': {'deserializer_cls': UserInputSchema, 'serializer_cls': UserOutputSchema},
    'POST': {'deserializer_cls': UserInputSchema, 'serializer_cls': UserOutputSchema},
    'PUT': {'deserializer_cls': UserUpdateSchema, 'serializer_cls': UserOutputSchema},
    'DELETE': {'deserializer_cls': UserInputSchema, 'serializer_cls': UserOutputSchema},
}


def get_deserializer_cls(method: str) -> UserInputSchema | UserUpdateSchema:
    """Retunr deserializer class from SCHEMA_MAPPING dict based on http method name."""
    return SCHEMA_MAPPING[method]['deserializer_cls']


def get_serializer_cls(method: str) -> UserOutputSchema:
    """Retunr serializer class from SCHEMA_MAPPING dict based on http method name."""
    return SCHEMA_MAPPING[method]['serializer_cls']


class AbstractUserSerializer(metaclass=abc.ABCMeta):
    """Abstract class for User model serialization."""

    def __init__(self, method: str) -> None:
        self.deserializer = get_deserializer_cls(method)
        self.serializer = get_serializer_cls(method)

    def deserialize_user_data(self, user: dict) -> dict:
        """Return deserialized data for single object User object."""
        return self._deserialize_user_data(data=user, collection=False)

    def serialize_user_data(self, user: User) -> dict:
        """Return serialized data for UserInputSchema."""
        return self._serialize_user_data(data=user, collection=False)

    def serialize_users_data(self, users: list[User]) -> list[dict]:
        """Return collection of serialized User objects."""
        return self._serialize_user_data(data=users, collection=True)


class UserSerializer(AbstractUserSerializer):
    """Serializer class for User model."""

    def _deserialize_user_data(self, data: dict, collection: bool = False) -> dict | list[dict]:
        try:
            result = self.deserializer(many=collection).load(data)
        except ValidationError as err:
            raise err
        return result

    def _serialize_user_data(self, data: User | list[User], collection: bool = False) -> dict | list[dict]:
        try:
            result = self.serializer(many=collection).dump(data)
        except ValidationError as err:
            raise err
        return result
