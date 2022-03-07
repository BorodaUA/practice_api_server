from sqla_softdelete import SoftDeleteMixin
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from common.constants.models import TeacherModelConstants
from db import Base


class Teacher(SoftDeleteMixin, Base):
    """A model representing a teacher."""

    __tablename__ = 'teachers'

    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True, index=True, nullable=False)
    user = relationship('User', backref=backref('teachers', uselist=False))
    card_id = Column(String(TeacherModelConstants.CHAR_SIZE_64.value), nullable=True, unique=True)
    qualification = Column(String(TeacherModelConstants.CHAR_SIZE_256.value), nullable=False)
    working_since = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    courses = relationship('Course', back_populates='teacher')
    subjects = relationship('Subject', back_populates='teacher')

    def __str__(self):
        return f'Teacher: id={self.id}, card_id={self.card_id}, qualification={self.qualification}'
