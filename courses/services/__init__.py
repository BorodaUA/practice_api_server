from copy import deepcopy
from typing import Type
from uuid import UUID
import abc

from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from courses.models import Course, CourseStudentAssociation
from courses.schemas import CourseBaseSchema
from courses.services.serializers import CourseSerializer
from courses.utils.exceptions import CourseNotFoundError
from students.services import StudentService
from students.utils.exceptions import StudentNotFoundError
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
        """Getting course dict payload and saving it in the Course table.

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

    def update_course(self, id: UUID, data: dict) -> dict:
        """Update Course object in the database.

        Args:
            id: UUID of Course object.
            data: dict from flask request json payload.

        Returns:
        Updated Course object from the database.
        """
        return self._update_course(id, data)

    def delete_course(self, id: UUID) -> None:
        """Delete Course object from the database.

        Args:
            id: UUID of Course object.

        Returns:
        Nothing.
        """
        return self._delete_course(id)

    def get_course_students(self, id: UUID) -> list[dict]:
        """Query database and return list Course object students from the db.

        Returns:
        List of Course object students serialized with StudentOutputSchema.
        """
        return self._get_course_students(id)

    def add_course_student(self, id: UUID, data: dict) -> dict:
        """Getting student id from json payload and saving it in associate table for Course-Students relationship.

        Args:
            data: dict from flask request json payload.

        Returns:
        Single Student object serialized with StudentOutputSchema.
        """
        return self._add_course_student(id, data)

    def get_course_student_by_id(self, id: UUID, student_id: UUID) -> dict:
        """Query database and return Course's Student object from the db.

        Returns:
        Course's Student object serialized with StudentOutputSchema.
        """
        return self._get_course_student_by_id(id, student_id)

    @abc.abstractclassmethod
    def _get_courses(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_course(self, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _get_course_by_id(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _update_course(self, id: UUID, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _delete_course(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _get_course_students(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _add_course_student(self, id: UUID, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _get_course_student_by_id(self, id: UUID, student_id: UUID) -> None:
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

    def _update_course(self, id: UUID, data: dict) -> dict:
        course = self.validator.deserialize(data=data)
        db_course = self._get_course(column='id', value=id)
        db_course.title = course['title']
        db_course.code = course['code']
        db_course.start_date = course['start_date']
        db_course.end_date = course['end_date']
        self.session.commit()
        self.session.refresh(db_course)
        self._log.debug(f'Course with id: {id} updated.')
        return self.validator.serialize(data=db_course)

    def _delete_course(self, id: UUID) -> None:
        if self._course_exists(column='id', value=id):
            course = self.session.query(Course).filter(Course.id == id).one()
            # Soft deleting Course object.
            course.delete()
            self.session.commit()
            self._log.debug(f'Course with id: {id} deleted.')

    def _get_course_students(self, id: UUID) -> list[dict]:
        self._log.debug('Getting all Course students from the db.')
        course = self._get_course(column='id', value=id)
        return self.validator.serialize([association.student for association in course.students])

    def _save_course_student_data(self, id: UUID, data: dict) -> Course:
        """Saves course student data in the CourseStudentAssociation model.

        Args:
            id: Course object UUID.
            data: deserialized course dict.

        Returns:
        Saved in the db Course object.
        """
        db_student = self.student_service._get_student(column='id', value=str(data['id']))
        db_course = self._get_course(column='id', value=id)
        course_student_association = CourseStudentAssociation()
        course_student_association.student = db_student
        db_course.students.append(course_student_association)
        self.session.add(db_course)
        self.session.commit()
        self.session.refresh(db_course)
        self._log.debug(f'Student object with id: {str(data["id"])} added to Course with id: {id}.')
        return db_course

    def _add_course_student(self, id: UUID, data: dict) -> dict:
        student_id = self.validator.deserialize(data=data)
        db_course = self._save_course_student_data(id, student_id)
        return self.validator.serialize(data=db_course.students[-1].student)

    def _get_course_student_by_id(self, id: UUID, student_id: UUID) -> dict:
        id = str(id)
        student_id = str(student_id)
        if self._course_student_exists(course_id=id, student_id=student_id):
            association = self.session.query(CourseStudentAssociation).filter_by(
                course_id=id,
                student_id=student_id,
            ).one()
            return self.validator.serialize(association.student)

    def _course_student_exists(self, course_id: str, student_id: str) -> bool:
        """Checks if Course and Student objects were added to association table CourseStudentAssociation.

        Args:
            course_id: Course object UUID.
            student_id: Student object UUID.

        Returns:
        book of objects existence in CourseStudentAssociation table.
        """
        if self._course_exists(column='id', value=course_id):
            q = self.session.query(CourseStudentAssociation).filter_by(
                course_id=course_id,
                student_id=student_id,
            )
            obj_exists = self.session.query(q.exists()).scalar()
            if not obj_exists:
                raise StudentNotFoundError(f'Student with id: {student_id} not found in Course with id: {course_id}.')
            return True
