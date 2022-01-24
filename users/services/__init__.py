import abc

from sqlalchemy.orm import scoped_session

from users.models import User
from users.services.serializers import UserSerializer
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

    @abc.abstractclassmethod
    def _get_users(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_user(self, user: dict) -> None:
        pass


class UserService(AbstractUserService):

    def _get_users(self) -> list[dict]:
        self._log.debug('Getting all users from the db.')
        users = self.session.query(User).all()
        return self.validator.serialize_users_data(users)

    def _add_user(self, user: dict) -> dict:
        user = self.validator.deserialize_user_data(user)
        user = User(**user)
        self._log.debug(f'Creating user with username: {user.username}')
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self.validator.serialize_user_data(user=user)
