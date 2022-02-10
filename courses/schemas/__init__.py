from marshmallow import Schema, fields, validate

from common.constants.schemas import CourseSchemaConstants
from courses.models import Course
from students.schemas import StudentOutputSchema
from teachers.schemas import TeacherOutputSchema


class CourseBaseSchema(Schema):
    """Course Base schema for Course model."""

    title = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=CourseSchemaConstants.CHAR_SIZE_2.value,
                max=CourseSchemaConstants.CHAR_SIZE_256.value,
            ),
        ],
    )
    code = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=CourseSchemaConstants.CHAR_SIZE_2.value,
                max=CourseSchemaConstants.CHAR_SIZE_16.value,
            ),
        ],
    )
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class CourseInputSchema(CourseBaseSchema):
    """Course Input schema for Course model."""
    teacher_id = fields.UUID()


class CourseOutputSchema(CourseBaseSchema):
    """Course Output schema for Course model."""
    id = fields.UUID()
    teacher = fields.Nested(TeacherOutputSchema)
    students = fields.Method('get_associated_students')

    def get_associated_students(self, obj: Course) -> list[dict] | list:
        """Custom method for CourseOutputSchema students field.

        Args:
            obj: Course object.

        Returns:
        List of Student objects from CourseStudentAssociation table serialized with StudentOutputSchema.
        """
        if not obj.students:
            return []
        return [StudentOutputSchema(many=False).dump(association.student) for association in obj.students]


class CourseUpdateSchema(CourseBaseSchema):
    """Course Update schema for Course model."""
    pass
