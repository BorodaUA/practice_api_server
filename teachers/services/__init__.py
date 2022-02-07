from copy import deepcopy
from typing import Type
from uuid import UUID
import abc

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from common.constants.models import TeacherModelConstants
from students.models import Student
from teachers.models import Teacher
from teachers.schemas import TeacherBaseSchema
from teachers.services.serializers import TeacherSerializer
from teachers.utils.exceptions import StudentExistsError, TeacherNotFoundError
from utils.exceptions import parse_integrity_error
from utils.logging import setup_logging


class AbstractTeacherService(metaclass=abc.ABCMeta):

    def __init__(
        self, session: scoped_session,
        validator: TeacherSerializer = TeacherSerializer,
        input_schema: Type[TeacherBaseSchema] | None = None,
        output_schema: Type[TeacherBaseSchema] | None = None,
            ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.validator = validator(input_schema, output_schema)

    def get_teachers(self) -> list[dict]:
        """Query database and return list Teacher objects from the db.

        Returns:
        List of Teacher object serialized with TeacherOutputSchema.
        """
        return self._get_teachers()

    def add_teacher(self, data: dict) -> dict:
        """Getting user dict payload and saving it in the Teacher table.

        Args:
            data: dict from flask request json payload.

        Returns:
        Single Teacher object serialized with TeacherOutputSchema.
        """
        return self._add_teacher(data)

    def get_teacher_by_id(self, id: UUID) -> dict:
        """Query database and return single Teacher objects from the db filtered by id.

        Args:
            id: UUID of Teacher object.

        Returns:
        Teacher object serialized with TeacherOutputSchema.
        """
        return self._get_teacher_by_id(id)

    def delete_teacher(self, id: UUID) -> None:
        """Delete Teacher object from the database.

        Args:
            id: UUID of Teacher object.

        Returns:
        Nothing.
        """
        return self._delete_teacher(id)

    @abc.abstractclassmethod
    def _get_teachers(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_teacher(self, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _get_teacher_by_id(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _delete_teacher(self, id: UUID) -> None:
        pass


class TeacherService(AbstractTeacherService, GenericService):
    """Provides CRUD operations and related data transformations for Teacher model."""

    def _get_teachers(self) -> list[dict]:
        self._log.debug('Getting all teachers from the db.')
        teachers = self.session.query(Teacher).all()
        return self.validator.serialize(teachers)

    def _add_teacher(self, data: dict) -> dict:
        teacher = self.validator.deserialize(data=data)
        db_teacher = self._save_teacher_data(data=teacher)
        return self.validator.serialize(data=db_teacher)

    def _save_teacher_data(self, data: dict) -> Teacher:
        """Saves and return Teacher data in the db.

        Args:
            data: dict of serialized teacher data.

        Returns:
        Teacher model object saved in the db.
        """
        teacher = deepcopy(data)
        # check if student with id exists.
        self._is_student_exists(column='id', value=teacher['id'])
        # Generating teacher card_id, if exception occurs during the saving process, rollback session and try again.
        while True:
            try:
                teacher['card_id'] = self._create_teacher_card_id()
                db_teacher = Teacher(**teacher)
                self.session.add(db_teacher)
                self.session.commit()
                self._log.debug(f'Created teacher with card_id: {teacher["card_id"]}')
                break
            except IntegrityError as err:
                table_name, field, value = parse_integrity_error(error=err)
                self._log.debug(
                    f'Error during saving {table_name} with {field}: {value} and card_id: {teacher["card_id"]}'
                )
                if field not in ['card_id']:
                    raise err
                self.session.rollback()
        self.session.refresh(db_teacher)
        return db_teacher

    def _is_student_exists(self, column: str, value: str) -> None:
        """Checks if Student from the request json data exists in the db.

        Args:
            column: name of table column to look up.
            value: to find in the table.
        Raises:
        StudentExistsError if Student with id exists.

        Returns:
        Nothing.
        """
        if self._check_obj_exists(table=Student, column=column, value=value):
            raise StudentExistsError(
                f'Teacher with {column}: {value} can not be created, '
                f'because a Student with {column}: {value} already exists.'
            )

    def _create_teacher_card_id(self) -> str:
        """Create teacher card_id number.

        Returns:
        properly formatted teacher card_id.
        """
        db_card_id = self._get_last_column_object(table=Teacher, column='card_id')
        if db_card_id:
            card_id = self._create_card_id(card_id=db_card_id)
        else:
            card_id = self._create_card_id(card_id=TeacherModelConstants.CARD_ID_DEFAULT_NUMBER.value)
        return card_id

    def _get_teacher_by_id(self, id: UUID) -> dict:
        teacher = self._get_teacher(column='id', value=id)
        return self.validator.serialize(data=teacher)

    def _get_teacher(self, column: str, value: UUID | str) -> dict:
        if self._teacher_exists(column=column, value=value):
            self._log.debug(f'Getting Teacher with {column}: {value}.')
            return self.session.query(Teacher).filter(Teacher.__table__.columns[column] == value).one()

    def _teacher_exists(self, column: str, value: str) -> bool:
        """Check if Teacher object exists in the db.

        Args:
            column: name of column in the Teacher model.
            value: to find in the Teacher model.
        Raises:
        TeacherNotFoundError exception if object not present in Teacher model.

        Returns:
        bool of Teacher object existence.
        """
        self._log.debug(f'Checking if Teacher with {column}: {value} exists.')
        q = self.session.query(Teacher).filter(Teacher.__table__.columns[column] == value)
        obj_exists = self.session.query(q.exists()).scalar()
        if not obj_exists:
            raise TeacherNotFoundError(f'Teacher with {column}: {value} not found.')
        return True

    def _delete_teacher(self, id: UUID) -> None:
        if self._teacher_exists(column='id', value=id):
            user = self.session.query(Teacher).filter(Teacher.id == id).one()
            # Soft deleting Teacher object.
            user.delete()
            self.session.commit()
            self._log.debug(f'Teacher with id: "{id}" deleted.')
