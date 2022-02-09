from copy import deepcopy
from typing import Type
from uuid import UUID
import abc

from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from courses.models import Course
from courses.schemas import CourseBaseSchema
from courses.services.serializers import CourseSerializer
from courses.utils.exceptions import CourseNotFoundError
from students.services import StudentService
from utils.logging import setup_logging


class AbstractCourseService(metaclass=abc.ABCMeta):

    def __init__(
        self, session: scoped_session,
        validator: CourseSerializer = CourseSerializer,
        input_schema: Type[CourseBaseSchema] | None = None,
        output_schema: Type[CourseBaseSchema] | None = None,
            ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.validator = validator(input_schema, output_schema)
        self.student_service = StudentService(session=self.session)

    def get_courses(self) -> list[dict]:
        """Query database and return list Course objects from the db.

        Returns:
        List of Course object serialized with CourseOutputSchema.
        """
        return self._get_courses()

    def add_course(self, data: dict) -> dict:
        """Getting user dict payload and saving it in the Course table.

        Args:
            data: dict from flask request json payload.

        Returns:
        Single Course object serialized with CourseOutputSchema.
        """
        return self._add_course(data)

    def get_course_by_id(self, id: UUID) -> dict:
        """Query database and return single Course objects from the db filtered by id.

        Args:
            id: UUID of Course object.

        Returns:
        Course object serialized with CourseOutputSchema.
        """
        return self._get_course_by_id(id)

    @abc.abstractclassmethod
    def _get_courses(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_course(self, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _get_course_by_id(self, id: UUID) -> None:
        pass


class CourseService(AbstractCourseService, GenericService):
    """Provides CRUD operations and related data transformations for Course model."""

    def _get_courses(self) -> list[dict]:
        self._log.debug('Getting all courses from the db.')
        courses = self.session.query(Course).all()
        return self.validator.serialize(courses)

    def _add_course(self, data: dict) -> dict:
        course = self.validator.deserialize(data=data)
        db_course = self._save_course_data(data=course)
        return self.validator.serialize(data=db_course)

    def _save_course_data(self, data: dict) -> Course:
        """Saves course data in the Course model.

        Args:
            data: deserialized course dict.

        Returns:
        Saved in the db Course object.
        """
        course = deepcopy(data)
        db_course = Course(**course)
        self._log.debug(f'Creating course with title: {course["title"]}')
        self.session.add(db_course)
        self.session.commit()
        self.session.refresh(db_course)
        return db_course

    def _get_course_by_id(self, id: UUID) -> dict:
        course = self._get_course(column='id', value=id)
        return self.validator.serialize(data=course)

    def _get_course(self, column: str, value: UUID | str) -> Course:
        if self._course_exists(column=column, value=value):
            self._log.debug(f'Getting Course with {column}: {value}.')
            return self.session.query(Course).filter(Course.__table__.columns[column] == value).one()

    def _course_exists(self, column: str, value: str) -> bool:
        """Check if Course object exists in the db.

        Args:
            column: name of column in the Course model.
            value: to find in the Course model.
        Raises:
        CourseNotFoundError exception if object not present in Course model.

        Returns:
        bool of Course object existence.
        """
        self._log.debug(f'Checking if Course with {column}: {value} exists.')
        q = self.session.query(Course).filter(Course.__table__.columns[column] == value)
        obj_exists = self.session.query(q.exists()).scalar()
        if not obj_exists:
            raise CourseNotFoundError(f'Course with {column}: {value} not found.')
        return True
