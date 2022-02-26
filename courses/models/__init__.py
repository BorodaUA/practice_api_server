import uuid

from sqla_softdelete import SoftDeleteMixin
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from common.constants.models import CourseModelConstants
from db import Base


class CourseStudentAssociation(Base):
    """Many-to-Many table for Course and Student models association."""

    __tablename__ = 'course_student_association'
    __table_args__ = (
        UniqueConstraint('course_id', 'student_id', name='_course_student_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    course = relationship('Course', back_populates='students_association')
    student = relationship('Student', back_populates='courses')

    def __repr__(self):
        return f'CourseStudentAssociation: course_id={self.course_id}, student_id={self.student_id}'


class Course(SoftDeleteMixin, Base):
    """A model representing a course."""

    __tablename__ = 'courses'
    __table_args__ = (
        UniqueConstraint('title', 'code', name='_title_code_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    teacher_id = Column(UUID(as_uuid=True), ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', back_populates='courses')

    students_association = relationship('CourseStudentAssociation', back_populates='course')
    students = association_proxy('students_association', 'student')

    title = Column(String(CourseModelConstants.CHAR_SIZE_256.value), nullable=False)
    code = Column(String(CourseModelConstants.CHAR_SIZE_16.value), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f'Course: id={self.id}, title={self.title}, start_date={self.start_date}, end_date={self.end_date}'
