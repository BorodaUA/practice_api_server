import uuid

from sqla_softdelete import SoftDeleteMixin
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from common.constants.models import UserModelConstants
from db import Base


class User(SoftDeleteMixin, Base):
    """A model representing a user."""

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    last_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    username = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    email = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=False, unique=True)
    password = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=True)
    phone_number = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    is_activated = Column(Boolean, nullable=True, default=UserModelConstants.FALSE.value)
    created_at = Column(DateTime, server_default=func.now())

    def __str__(self):
        return f'User: username={self.username}, first_name={self.first_name}, last_name={self.last_name}'
