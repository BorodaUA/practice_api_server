from typing import Type
import abc

from sqlalchemy import desc

from db import Base


class AbstractService(metaclass=abc.ABCMeta):
    """Abstract class for service."""

    @abc.abstractclassmethod
    def _check_obj_exists(self, able: Type[Base], column: str, value: str) -> None:
        pass

    @abc.abstractclassmethod
    def _get_last_column_object(self, table: Type[Base], column: str) -> None:
        pass

    @abc.abstractclassmethod
    def _create_card_id(self, card_id: str = None) -> None:
        pass


class GenericService(AbstractService):
    """Generic class for services."""

    def _check_obj_exists(self, table: Type[Base], column: str, value: str) -> bool:
        """Check if object exists in the specified db table.

        Args:
            table: db table to check.
            column: name of table column to look up.
            value: to find in the table.

        Returns:
        bool of the object existence.
        """
        self._log.debug(f'Checking if {table.__table__.name} object with {column}: {value} exists.')
        q = self.session.query(table).filter(table.__table__.columns[column] == value)
        obj_exists = self.session.query(q.exists()).scalar()
        if not obj_exists:
            return False
        return True

    def _get_last_column_object(self, table: Type[Base], column: str) -> str | None:
        """Return last column's object from the db filtered by 'created_at' column.

        Args:
            table: db table to check.
            column: name of table column to look up.
            value: to find in the table.

        Returns:
        table's object if it is in the table or None if it is not.
        """
        object = self.session.query(
            table.__table__.columns[column],
        ).order_by(desc(table.created_at)).limit(1).scalar()
        self._log.debug(f'Getting last value: "{object}" from column: "{column}" in {table.__table__.name} table.')
        return object

    def _create_card_id(self, card_id: str = None) -> str:
        """Get card_id number and increment its value by +1.

        Args:
            card_id: string contains card_id, PREFIX-NUMBER.

        Returns:
        Incremented by +1 card_id string.
        """
        prefix, number = card_id.split('-')
        number = int(number) + 1
        return f'{prefix}-{number:07d}'
