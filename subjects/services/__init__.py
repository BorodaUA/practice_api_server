from copy import deepcopy
from typing import Type
from uuid import UUID
import abc

from sqlalchemy.orm import scoped_session

from common.abstract.services import GenericService
from courses.schemas import CourseBaseSchema
from subjects.models import Subject
from subjects.services.serializers import SubjectSerializer
from subjects.utils.exceptions import SubjectNotFoundError
from utils.logging import setup_logging


class AbstractSubjectService(metaclass=abc.ABCMeta):

    def __init__(
        self, session: scoped_session,
        validator: SubjectSerializer = SubjectSerializer,
        input_schema: Type[CourseBaseSchema] | None = None,
        output_schema: Type[CourseBaseSchema] | None = None,
            ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.validator = validator(input_schema, output_schema)

    def get_subjects(self) -> list[dict]:
        """Query database and return list Subject objects from the db.

        Returns:
        List of Subject object serialized with SubjectOutputSchema.
        """
        return self._get_subjects()

    def add_subject(self, data: dict) -> dict:
        """Getting subject dict payload and saving it in the Subject table.

        Args:
            data: dict from flask request json payload.

        Returns:
        Single Subject object serialized with SubjectOutputSchema.
        """
        return self._add_subject(data)

    def get_subject_by_id(self, id: UUID) -> dict:
        """Query database and return single Subject object from the db filtered by id.

        Args:
            id: UUID of Subject object.

        Returns:
        Subject object serialized with SubjectOutputSchema.
        """
        return self._get_subject_by_id(id)

    def update_subject(self, id: UUID, data: dict) -> dict:
        """Update Subject object in the database.

        Args:
            id: UUID of Subject object.
            data: dict from flask request json payload.

        Returns:
        Updated Subject object from the database.
        """
        return self._update_subject(id, data)

    def delete_subject(self, id: UUID) -> None:
        """Delete Subject object from the database.

        Args:
            id: UUID of Subject object.

        Returns:
        Nothing.
        """
        return self._delete_subject(id)

    @abc.abstractclassmethod
    def _get_subjects(self) -> None:
        pass

    @abc.abstractclassmethod
    def _add_subject(self) -> None:
        pass

    @abc.abstractclassmethod
    def _get_subject_by_id(self, id: UUID) -> None:
        pass

    @abc.abstractclassmethod
    def _update_subject(self, id: UUID, data: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _delete_subject(self, id: UUID) -> None:
        pass


class SubjectService(AbstractSubjectService, GenericService):
    """Provides CRUD operations and related data transformations for Subject model."""

    def _get_subjects(self) -> list[dict]:
        self._log.debug('Getting all subjects from the db.')
        subjects = self.session.query(Subject).all()
        return self.validator.serialize(subjects)

    def _add_subject(self, data: dict) -> dict:
        subject = self.validator.deserialize(data=data)
        db_subject = self._save_subject_data(data=subject)
        return self.validator.serialize(data=db_subject)

    def _save_subject_data(self, data: dict) -> Subject:
        """Saves subject data in the Subject model.

        Args:
            data: deserialized subject dict.

        Returns:
        Saved in the db Subject object.
        """
        subject = deepcopy(data)
        db_subject = Subject(**subject)
        self._log.debug(f'Creating subject with title: {subject["title"]}')
        self.session.add(db_subject)
        self.session.commit()
        self.session.refresh(db_subject)
        return db_subject

    def _get_subject_by_id(self, id: UUID) -> dict:
        subject = self._get_subject(column='id', value=id)
        return self.validator.serialize(data=subject)

    def _get_subject(self, column: str, value: UUID | str) -> Subject:
        if self._subject_exists(column=column, value=value):
            self._log.debug(f'Getting Subject with {column}: {value}.')
            return self.session.query(Subject).filter(Subject.__table__.columns[column] == value).one()

    def _subject_exists(self, column: str, value: str) -> bool:
        """Check if Subject object exists in the db.

        Args:
            column: name of column in the Subject model.
            value: to find in the Subject model.
        Raises:
        SubjectNotFoundError exception if object not present in Subject model.

        Returns:
        bool of Subject object existence.
        """
        self._log.debug(f'Checking if Subject with {column}: {value} exists.')
        q = self.session.query(Subject).filter(Subject.__table__.columns[column] == value)
        obj_exists = self.session.query(q.exists()).scalar()
        if not obj_exists:
            raise SubjectNotFoundError(f'Subject with {column}: {value} not found.')
        return True

    def _update_subject(self, id: UUID, data: dict) -> dict:
        subject = self.validator.deserialize(data=data)
        db_subject = self._get_subject(column='id', value=id)
        db_subject.title = subject['title']
        db_subject.code = subject['code']
        self.session.commit()
        self.session.refresh(db_subject)
        self._log.debug(f'Subject with id: {id} updated.')
        return self.validator.serialize(data=db_subject)

    def _delete_subject(self, id: UUID) -> None:
        if self._subject_exists(column='id', value=id):
            subject = self.session.query(Subject).filter(Subject.id == id).one()
            # Soft deleting Course object.
            subject.delete()
            self.session.commit()
            self._log.debug(f'Subject with id: {id} deleted.')
