from sqla_softdelete import SoftDeleteMixin
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from common.constants.models import StudentsModelConstants
from db import Base


class Student(SoftDeleteMixin, Base):
    """A model representing a student."""

    __tablename__ = 'students'

    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True, index=True, nullable=False)
    user = relationship('User', backref=backref('students', uselist=False))
    card_id = Column(String(StudentsModelConstants.CHAR_SIZE_64.value), nullable=True, unique=True)
    student_since = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    courses = relationship('CourseStudentAssociation', back_populates='student')

    def __str__(self):
        return f'Student: id={self.id}, card_id={self.card_id}, student_since={self.student_since}'
