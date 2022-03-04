import uuid

from sqla_softdelete import SoftDeleteMixin
from sqlalchemy import Column, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from common.constants.models import CourseModelConstants
from db import Base


class Subject(SoftDeleteMixin, Base):
    """A model representing a subject."""

    __tablename__ = 'subjects'
    __table_args__ = (
        UniqueConstraint('title', 'code', name='_title_code_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    title = Column(String(CourseModelConstants.CHAR_SIZE_256.value), nullable=False)
    code = Column(String(CourseModelConstants.CHAR_SIZE_16.value), nullable=False)

    course = relationship('Course', backref=backref('course'), uselist=False)

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f'Subject: id={self.id}, title={self.title}, code={self.code}'
