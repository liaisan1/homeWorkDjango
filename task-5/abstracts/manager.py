
from abc import ABC, abstractmethod
from typing import Optional

from abstracts.base import BaseModel



class AbstractEntityManager[T: BaseModel](ABC):
    _cls = None
    _filename = None

    def __init__(self, cls: type[T]):
        self._cls = cls
        self._setup()

    @abstractmethod
    def _setup(self):
        pass

    @abstractmethod
    def save(self) -> None: ...

    @abstractmethod
    def add(self, entities: list[T]) -> list[T]: ...

    @abstractmethod
    def get(self, criteria: Optional[dict] = None) -> list[T]: ...

    @abstractmethod
    def delete(self, criteria: Optional[dict] = None) -> list[T]: ...

    @abstractmethod
    def update(self, criteria: dict, changes: dict) -> list[T]: ...
