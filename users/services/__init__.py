from uuid import UUID
import abc

from passlib.hash import argon2
from sqlalchemy.orm import scoped_session

from users.models import User
from users.services.serializers import UserSerializer
from users.utils.exceptions import UserNotFoundError
from utils.logging import setup_logging


class AbstractUserService(metaclass=abc.ABCMeta):

    def __init__(self, session: scoped_session, validator: UserSerializer = UserSerializer) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.validator = validator()

    def get_users(self) -> list[dict]:
        """Return list of User objects from the db."""
        return self._get_users()

    def add_user(self, user: dict) -> dict:
        """Add User object to the db."""
        return self._add_user(user)

    def delete_user(self, id: UUID) -> None:
        """Delete User object from the db."""
        return self._delete_user(id)

    def get_user_by_id(self, id: UUID) -> dict:
        """Return User object from the db filtered by id."""
        return self._get_user_by_id(id)

    @abc.abstractclassmethod
    def _get_users(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_user(self, user: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _delete_user(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _get_user_by_id(self, id: UUID) -> None:
        pass


class UserService(AbstractUserService):

    def _get_users(self) -> list[dict]:
        self._log.debug('Getting all users from the db.')
        users = self.session.query(User).all()
        return self.validator.serialize_users_data(users)

    def _add_user(self, user: dict) -> dict:
        user = self.validator.deserialize_user_data(user)
        user['password'] = self._hash_password(password=user['password'])
        user = User(**user)
        self._log.debug(f'Creating user with username: {user.username}')
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self.validator.serialize_user_data(user=user)

    def _hash_password(self, password: str) -> str:
        """Return password hashed with argon2 algorithm."""
        return argon2.using(rounds=4).hash(password)

    def _delete_user(self, id: UUID) -> None:
        if self._user_exists(column='id', value=id):
            user = self.session.query(User).filter(User.id == id).one()
            # Soft deleting User object.
            user.delete()
            self.session.commit()
            self._log.debug(f'User with id: "{id}" deleted.')

    def _user_exists(self, column: str, value: UUID) -> bool:
        """Check if User object exists in the db."""
        self._log.debug(f'Checking if User with {column}: {value} exists.')
        q = self.session.query(User).filter(User.__table__.columns[column] == value)
        user_exists = self.session.query(q.exists()).scalar()
        if not user_exists:
            raise UserNotFoundError(f'User with {column}: {value} not found.')
        return True

    def _get_user(self, column: str, value: UUID | str) -> dict:
        if self._user_exists(column=column, value=value):
            return self.session.query(User).filter(User.__table__.columns[column] == value).one()

    def _get_user_by_id(self, id: UUID) -> dict:
        user = self._get_user(column='id', value=id)
        return self.validator.serialize_user_data(user=user)
