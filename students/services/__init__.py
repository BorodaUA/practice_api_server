from copy import deepcopy
from typing import Type
import abc

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from common.constants.models import StudentsModelConstants
from students.models import Student
from students.schemas import StudentBaseSchema
from students.services.serializers import StudentSerializer
from students.utils.exceptions import TeacherExistsError
from teachers.models import Teacher
from utils.exceptions import parse_integrity_error
from utils.logging import setup_logging


class AbstractStudentService(metaclass=abc.ABCMeta):

    def __init__(
        self, session: scoped_session,
        validator: StudentSerializer = StudentSerializer,
        input_schema: Type[StudentBaseSchema] | None = None,
        output_schema: Type[StudentBaseSchema] | None = None,
            ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.validator = validator(input_schema, output_schema)

    def get_students(self) -> list[dict]:
        """Query database and return list Student objects from the db.

        Returns:
        List of Student object serialized with StudentOutputSchema.
        """
        return self._get_students()

    def add_student(self, data: dict) -> dict:
        """Getting student dict payload and saving it in the Student table.

        Args:
            data: dict from flask request json payload.

        Returns:
        Single Student object serialized with StudentOutputSchema.
        """
        return self._add_student(data)

    @abc.abstractclassmethod
    def _get_students(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_student(self, data: dict) -> None:
        pass


class StudentService(AbstractStudentService, GenericService):
    """Provides CRUD operations and related data transformations for Student model."""

    def _get_students(self) -> list[dict]:
        self._log.debug('Getting all students from the db.')
        students = self.session.query(Student).all()
        return self.validator.serialize(students)

    def _add_student(self, data: dict) -> dict:
        student = self.validator.deserialize(data=data)
        db_student = self._save_student_data(data=student)
        return self.validator.serialize(data=db_student)

    def _save_student_data(self, data: dict) -> Student:
        """Saves and return Student data in the db.

        Args:
            data: dict of serialized student data.

        Returns:
        Student model object saved in the db.
        """
        student = deepcopy(data)
        # check if teacher with id exists.
        self._is_teacher_exists(column='id', value=student['id'])
        # Generating teacher card_id, if exception occurs during the saving process, rollback session and try again.
        while True:
            try:
                student['card_id'] = self._create_student_card_id()
                db_student = Student(**student)
                self.session.add(db_student)
                self.session.commit()
                self._log.debug(f'Created student with card_id: {student["card_id"]}')
                break
            except IntegrityError as err:
                table_name, field, value = parse_integrity_error(error=err)
                self._log.debug(
                    f'Error during saving {table_name} with {field}: {value} and card_id: {student["card_id"]}'
                )
                if field not in ['card_id']:
                    raise err
                self.session.rollback()
        self.session.refresh(db_student)
        return db_student

    def _is_teacher_exists(self, column: str, value: str) -> None:
        """Checks if Teacher from the request json data exists in the db.

        Args:
            column: name of table column to look up.
            value: to find in the table.
        Raises:
        TeacherExistsError if Teacher obj with id exists.

        Returns:
        Nothing.
        """
        if self._check_obj_exists(table=Teacher, column=column, value=value):
            raise TeacherExistsError(
                f'Student with {column}: {value} can not be created, '
                f'because a Teacher with {column}: {value} already exists.'
            )

    def _create_student_card_id(self) -> str:
        """Create student card_id number.

        Returns:
        properly formatted teacher card_id.
        """
        db_card_id = self._get_last_column_object(table=Student, column='card_id')
        if db_card_id:
            card_id = self._create_card_id(card_id=db_card_id)
        else:
            card_id = self._create_card_id(card_id=StudentsModelConstants.CARD_ID_DEFAULT_NUMBER.value)
        return card_id
