
from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Self, Any, Dict, get_type_hints
from uuid import uuid4


@dataclass(repr=False, kw_only=True)
class BaseModel:

    _id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def id(self) -> str:
        return self._id

    def to_dict(self) -> dict:
        result = {}

        for field_obj in fields(self):
            field_name = field_obj.name
            value = getattr(self, field_name)

            # Обработка Enum
            if isinstance(value, Enum):
                result[field_name] = value.value
            # Обработка вложенных BaseModel
            elif isinstance(value, BaseModel):
                result[field_name] = value.to_dict()
            # Обработка списков
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, Enum):
                        new_list.append(item.value)
                    elif isinstance(item, BaseModel):
                        new_list.append(item.to_dict())
                    else:
                        new_list.append(item)
                result[field_name] = new_list
            # Все остальное
            else:
                result[field_name] = value

        # Обработка _id -> id
        if "_id" in result:
            result["id"] = result.pop("_id")

        return result

    @classmethod
    def from_dict(cls, dict_data: dict) -> Self:
        data = dict_data.copy()

        # id -> _id
        if "id" in data:
            data["_id"] = data.pop("id")

        type_hints = get_type_hints(cls)

        # Обрабатываем каждое поле
        for field_obj in fields(cls):
            field_name = field_obj.name
            if field_name in data and field_name in type_hints:
                field_type = type_hints[field_name]
                value = data[field_name]

                if (isinstance(field_type, type) and
                        issubclass(field_type, Enum) and
                        value is not None):
                    try:
                        if not isinstance(value, field_type):
                            data[field_name] = field_type(value)
                    except (ValueError, KeyError):
                        try:
                            data[field_name] = field_type[value]
                        except (ValueError, KeyError):
                            pass

        return cls(**data)

    @classmethod
    def from_json(cls, json_value: str) -> Self:
        data = json.loads(json_value)
        return cls.from_dict(data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        return self.to_json()

    def __str__(self) -> str:
        return self.to_json()