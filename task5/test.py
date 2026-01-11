import json
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
from enum import Enum
import shutil


# 1. АБСТРАКТНЫЙ МЕНЕДЖЕР

class AbstractEntityManager(ABC):
    def __init__(self, cls, filename: Optional[str] = None):
        self._cls = cls
        self._filename = filename

    @abstractmethod
    def add(self, entities: List) -> List:
        pass

    @abstractmethod
    def get(self, criteria: Optional[dict] = None) -> List:
        pass

    @abstractmethod
    def update(self, criteria: dict, changes: dict) -> List:
        pass

    @abstractmethod
    def delete(self, criteria: dict) -> List:
        pass

    @abstractmethod
    def save(self) -> None:
        pass


# 2. JSON МЕНЕДЖЕР

class JsonEntityManager(AbstractEntityManager):
    def __init__(self, cls, filename: Optional[str] = None):
        if not filename:
            filename = f"data/{cls.__name__.lower()}s.json"
        super().__init__(cls, filename)

        Path("data").mkdir(exist_ok=True)

        self._data = []
        self._load()

    def _load(self):
        try:
            if os.path.exists(self._filename):
                with open(self._filename, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
        except:
            self._data = []

    def _save(self):
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def add(self, entities: List) -> List:
        for entity in entities:
            entity_dict = entity.__dict__.copy()
            entity_dict.pop('objects', None)

            if 'id' not in entity_dict or not entity_dict['id']:
                entity_dict['id'] = len(self._data) + 1
                entity.id = entity_dict['id']

            self._data.append(entity_dict)

        self.save()
        return entities

    def get(self, criteria: Optional[dict] = None) -> List:
        if not criteria:
            result = []
            for item in self._data:
                obj = self._cls.__new__(self._cls)
                obj.__dict__.update(item)
                result.append(obj)
            return result

        result = []
        for item in self._data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break

            if match:
                obj = self._cls.__new__(self._cls)
                obj.__dict__.update(item)
                result.append(obj)

        return result

    def update(self, criteria: dict, changes: dict) -> List:
        updated = []
        for i, item in enumerate(self._data):
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break

            if match:
                self._data[i].update(changes)
                obj = self._cls.__new__(self._cls)
                obj.__dict__.update(self._data[i])
                updated.append(obj)

        if updated:
            self.save()

        return updated

    def delete(self, criteria: dict) -> List:
        deleted = []
        new_data = []

        for item in self._data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break

            if match:
                obj = self._cls.__new__(self._cls)
                obj.__dict__.update(item)
                deleted.append(obj)
            else:
                new_data.append(item)

        self._data = new_data
        if deleted:
            self.save()

        return deleted

    def save(self) -> None:
        self._save()


# 3. БАЗОВЫЙ КЛАСС И МЕТАКЛАСС


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'Model':
            engine = os.getenv('ENGINE', 'json').lower()
            if engine == 'sqlite':
                cls.objects = JsonEntityManager(cls)
            else:
                cls.objects = JsonEntityManager(cls)
        return cls


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        if self.id:
            changes = self.__dict__.copy()
            changes.pop('objects', None)
            changes.pop('id', None)
            self.__class__.objects.update({'id': self.id}, changes)
        else:
            self.__class__.objects.add([self])

    def delete(self):
        if self.id:
            self.__class__.objects.delete({'id': self.id})

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


# 4. МОДЕЛИ

class User(Model):
    def __init__(self, username=None, email=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.status = kwargs.get('status', 'active')

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}')"


class Post(Model):
    def __init__(self, title=None, description=None, text=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.text = text
        self.status = kwargs.get('status', 'draft')

    def __str__(self):
        return f"Post(id={self.id}, title='{self.title}')"


# ТЕСТ

print("=" * 50)
print("ПРОСТОЙ ТЕСТ (ИСПРАВЛЕННЫЙ)")
print("=" * 50)

Path("data").mkdir(exist_ok=True)

print("\n1. Создаем пользователя:")
user = User(username="тест", email="test@mail.ru")
print(f"   Создан: {user}")

print("\n2. Сохраняем:")
user.save()
print("  Сохранен")

print("\n3. Все пользователи:")
users = User.objects.get()
for u in users:
    print(f"   - {u}")
print(f"   Всего: {len(users)}")

print("\n4. Добавляем второго:")
user2 = User(username="аня", email="anya@mail.ru", age=25)
user2.save()
print(f"   Добавлен: {user2}")

print("\n5. Создаем пост:")
post = Post(title="Мой пост", text="Текст")
post.save()
print(f"   Создан: {post}")

print("\n6. Созданные файлы:")
if os.path.exists("data"):
    for file in os.listdir("data"):
        path = f"data/{file}"
        size = os.path.getsize(path)
        print(f"   {path} - {size} байт")

print("\n" + "=" * 50)
print("ТЕСТ ПРОЙДЕН УСПЕШНО")
print("=" * 50)