
import os
from enum import Enum
from sqlite3 import Connection, Cursor, connect
from typing import Any, List, Optional  # Добавьте Any сюда!

from abstracts.base import BaseModel
from abstracts.manager import AbstractEntityManager



class SqliteEntityManager[T: BaseModel](AbstractEntityManager[T]):

    __con: Connection
    __cursor: Cursor
    __table: str

    def _setup(self):
        self.__table = self._cls.__name__
        db_filename = os.getenv("DB_FILENAME", "data")
        self._filename = f"{db_filename}.sqlite"
        self.__con = connect(self._filename)
        self.__cursor = self.__con.cursor()
        self.__create_table()

    def __get_fields(self) -> List[str]:
        """Form field list of entity.

        Returns:
            List[str]: Entity field names
        """
        field_names = [cls_field for cls_field in self._cls.__annotations__.keys()]
        field_names.append("id")
        return field_names

    def __create_table(self) -> None:
        """Create sqlite table."""
        self.__cursor.execute(f"DROP TABLE IF EXISTS {self.__table}")
        fields = self.__get_fields()
        fields_sql = ", ".join([f"{field} TEXT" for field in fields])
        self.__cursor.execute(f"CREATE TABLE {self.__table} ({fields_sql})")

    @staticmethod
    def __format_condition(key: str, value: Any) -> str:  # Теперь Any определен
        """Format col=val expressions by value type for WHERE and SET expressions.

        Examples:
            key='status', value=UserStatus.CREATED
            result = "status=0"

            key='id', value="abc"
            result = "id='abc'"

        Args:
            key (str): Column name
            value (Any): Value

        Returns:
            str: Formatted col=val expression
        """
        if isinstance(value, str):
            val = f"'{value}'"
        elif value is None:
            val = "NULL"
        elif isinstance(value, bool):
            val = "1" if value else "0"
        else:
            val = str(value)
        return f"{key}={val}"

    def __form_where_condition(self, criteria: Optional[dict] = None) -> str:
        """Form WHERE expression based on criteria.

        Args:
            criteria (Optional[dict], optional): Dictionary to filter. Defaults to None.

        Examples:
            criteria = {"username": "aaa", "password": "bb"}
            result = "WHERE username='aaa' AND password='bbb'"

            criteria = {"status": UserStatus.CREATED}
            result = "WHERE status=0"

            criteria = None
            result = ""

        Returns:
            str: _description_
        """
        stmt = "WHERE 1=1"
        if not criteria:
            return stmt
        fields = self.__get_fields()
        for k, v in criteria.items():
            if k not in fields or v is None:
                raise ValueError(f"error in pair ({k}, {v})")
            stmt += f" AND {self.__format_condition(k, v)}"
        return stmt

    def add(self, entities: List[T]) -> List[T]:
        """Add entities to source.

        Args:
            entities (T): Entities to store

        Returns:
            List[T]: Added entities
        """
        fields = self.__get_fields()
        formatted_fields = []
        for entity in entities:
            row = []
            # Получаем словарь объекта (Enum уже преобразованы в значения)
            entity_dict = entity.to_dict()
            for field in fields:
                # Для поля 'id' берем из словаря по ключу 'id'
                if field == "id":
                    value = entity_dict.get("id")
                else:
                    value = entity_dict.get(field)
                row.append(value)
            formatted_fields.append(row)

        placeholders = ", ".join(["?" for _ in fields])
        fields_str = ", ".join(fields)
        stmt = f"INSERT INTO {self.__table} ({fields_str}) VALUES ({placeholders})"
        self.__cursor.executemany(stmt, formatted_fields)
        return entities

    def get(self, criteria: Optional[dict] = None) -> List[T]:
        """Filter entities from source by criteria and return as list.

        Args:
            criteria (Optional[dict], optional): Dictinary of search conditions.
            Defaults to None.

        Returns:
            List[T]: Filtered entities
        """
        try:
            stmt = (
                f"SELECT * FROM {self.__table} {self.__form_where_condition(criteria)}"
            )
            result = self.__cursor.execute(stmt)
            rows = result.fetchall()

            # Преобразуем результаты в объекты модели
            entities: List[T] = []
            fields = self.__get_fields()
            for row in rows:
                entity_dict = {}
                for i, field in enumerate(fields):
                    if field == "id":
                        entity_dict["_id"] = row[i]
                    else:
                        entity_dict[field] = row[i]
                entities.append(self._cls.from_dict(entity_dict))
            return entities
        except ValueError as e:
            print(e)
            return []

    def update(self, criteria: dict, changes: dict) -> List[T]:
        """Modify entities from source by criteria and return as list.

        Args:
            criteria (dict): Dictinary of search conditions.
            changes (dict): Dictinary of changed.

        Returns:
            List[T]: Updated entities from source
        """
        changes_stmt = "SET "
        changes_list = []
        fields = self.__get_fields()
        for k, v in changes.items():
            if k in fields and v is not None:
                changes_list.append(self.__format_condition(k, v))
        if len(changes_list) == 0:
            return []
        changes_stmt += ", ".join(changes_list)
        try:
            stmt = f"UPDATE {self.__table} {changes_stmt} {self.__form_where_condition(criteria)}"
            self.__cursor.execute(stmt)
            # Возвращаем обновленные сущности
            return self.get(criteria)
        except ValueError as e:
            print(e)
            return []

    def delete(self, criteria: Optional[dict] = None) -> List[T]:
        """Delete entities from source by criteria and return as list.

        Args:
            criteria (dict): Dictinary of search conditions.

        Returns:
            List: Deleted entities
        """
        # Получаем сущности перед удалением
        entities_to_delete = self.get(criteria)
        try:
            stmt = f"DELETE FROM {self.__table} {self.__form_where_condition(criteria)}"
            self.__cursor.execute(stmt)
            return entities_to_delete
        except ValueError as e:
            print(e)
            return []

    def save(self):
        """Save changes to source."""
        self.__con.commit()