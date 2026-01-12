
import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from abstracts.base import BaseModel
from abstracts.manager import AbstractEntityManager

load_dotenv()



class JsonEntityManager[T: BaseModel](AbstractEntityManager[T]):

    def _setup(self):
        classname = self._cls.__name__
        self._filename = f"{classname}.json"
        self.__check_folder()
        self.load()

    __folder: Path = (
        Path(__file__).parent.parent
        / "resources"
        / (os.getenv("JSON_DATA_FOLDER", "json"))
    )
    __entities: list[T] = []

    def __check_folder(self):
        self.__folder.mkdir(parents=True, exist_ok=True)

    @property
    def filename(self) -> Path:
        path = self.__folder / self._filename
        if not path.exists():
            with open(str(path), "w") as f:
                f.write("[]")
        return path

    def load(self) -> None:
        with open(str(self.filename), "r") as file:
            entities = json.load(file)
        self.__entities = [self._cls.from_dict(entity) for entity in entities]

    def save(self) -> None:
        with open(str(self.filename), "w") as file:
            json.dump([entity.to_dict() for entity in self.__entities], file)

    def add(self, entities: list[T]) -> list[T]:
        self.__entities.extend(entities)
        return entities

    @staticmethod
    def _check_entity_matches_criteria(entity: T, criteria: dict) -> bool:
        if all(
            (hasattr(entity, k) and entity.__getattribute__(k) == v)
            for k, v in criteria.items()
        ):
            return True
        return False

    def _get_entities_by_criteria(self, criteria: dict | None) -> list[T]:
        if criteria is None:
            return self.__entities
        result = []
        for entity in self.__entities:
            if self._check_entity_matches_criteria(entity, criteria):
                result.append(entity)
        return result

    def get(self, criteria: Optional[dict] = None) -> list[T]:
        """Filter stored entities by criteria and return as list.

        Args:
            criteria (Optional[dict], optional): Dictinary of search conditions.
            Defaults to None.

        Returns:
            list[T]: Filtered entities
        """
        return self._get_entities_by_criteria(criteria)

    def delete(self, criteria: Optional[dict] = None) -> list[T]:
        """Filter and delete stored entities by criteria.

        Args:
            criteria (Optional[dict], optional): Dictinary of search conditions.
            Defaults to None.

        Returns:
            list[str]: ID's of deleted entities
        """
        entities_to_delete = self._get_entities_by_criteria(criteria)
        self.__entities = [e for e in self.__entities if e not in entities_to_delete]
        return entities_to_delete

    def __getitem__(self, criteria: dict) -> list[T]:
        """Filter stored entities by criteria and return as list.

        Args:
            criteria (Optional[dict], optional): Dictinary of search conditions.
            Defaults to None.

        Returns:
            list[T]: Filtered entities
        """
        return self.get(criteria)

    def update(self, criteria: dict, changes: dict) -> list[T]:
        """Modify entities from source by criteria and return as list.

        Args:
            criteria (dict): Dictinary of search conditions.
            changes (dict): Dictinary of changed.

        Returns:
            list[T]: Updated entities
        """
        entities_to_update = self._get_entities_by_criteria(criteria)
        for entity in entities_to_update:
            for k, v in changes.items():
                entity.__setattr__(k, v)
        return entities_to_update
