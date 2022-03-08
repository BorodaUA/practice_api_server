from marshmallow import Schema, fields

from students.schemas import StudentOutputSchema
from subjects.schemas import SubjectOutputSchema
from teachers.schemas import TeacherOutputSchema


class CourseBaseSchema(Schema):
    """Course Base schema for Course model."""
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class CourseInputSchema(CourseBaseSchema):
    """Course Input schema for Course model."""
    teacher_id = fields.UUID(required=True)
    subject_id = fields.UUID(required=True)


class CourseOutputSchema(CourseBaseSchema):
    """Course Output schema for Course model."""
    id = fields.UUID()
    subject = fields.Nested(SubjectOutputSchema)
    teacher = fields.Nested(TeacherOutputSchema)
    students = fields.Nested(StudentOutputSchema(many=True))


class CourseUpdateSchema(CourseBaseSchema):
    """Course Update schema for Course model."""
    pass


class CourseStudentInputSchema(Schema):
    """CourseStudent Input schema for Course model."""
    id = fields.UUID(required=True)
