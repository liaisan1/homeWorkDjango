import os

from dotenv import load_dotenv

from abstracts.manager import AbstractEntityManager
from managers.json_manager import JsonEntityManager
from managers.sqlite_manager import SqliteEntityManager

managers = {
    "json": JsonEntityManager,
    "sqlite": SqliteEntityManager,
}


class Meta(type):
    @staticmethod
    def __get_entity_manager_class() -> type[AbstractEntityManager]:
        engine = os.getenv("ENGINE", "json")
        return managers.get(engine, JsonEntityManager)

    def __init__(cls, name, bases, namespace):
        super(Meta, cls).__init__(name, bases, namespace)
        load_dotenv()
        entity_manager_cls = cls.__class__.__get_entity_manager_class()
        cls.objects = entity_manager_cls[cls](cls)
        cls.save = cls.objects.save
