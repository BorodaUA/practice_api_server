from copy import deepcopy
from typing import Type
import abc

from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from courses.models import Course
from courses.schemas import CourseBaseSchema
from courses.services.serializers import CourseSerializer
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

    @abc.abstractclassmethod
    def _get_courses(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_course(self) -> None:
        pass


class CourseService(AbstractCourseService, GenericService):
    """Provides CRUD operations and related data transformations for Course model."""

    def _get_courses(self) -> list[dict]:
        self._log.debug('Getting all courses from the db.')
        courses = self.session.query(Course).all()
        return self.validator.serialize(courses)

    def _add_course(self, data: dict) -> dict:
        self._log.debug('Saving course to the db.')
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
