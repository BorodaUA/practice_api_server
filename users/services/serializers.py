import abc

from marshmallow.exceptions import ValidationError

from users.models import User
from users.schemas import UserInputSchema, UserOutputSchema


class AbstractUserSerializer(metaclass=abc.ABCMeta):
    """Abstract class for User model serialization."""

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
            result = UserInputSchema(many=collection).load(data)
        except ValidationError as err:
            raise err
        return result

    def _serialize_user_data(self, data: User | list[User], collection: bool = False) -> dict | list[dict]:
        try:
            result = UserOutputSchema(many=collection).dump(data)
        except ValidationError as err:
            raise err
        return result
