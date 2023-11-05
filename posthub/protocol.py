from typing import Generic, TypeVar

import orjson
from pydantic import BaseModel as PydanticModel
from pydantic import Field
from pydantic.generics import GenericModel as PydanticGenericModel

DataT = TypeVar("DataT")


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class BaseModel(PydanticModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        alias_generator = to_camel_case
        orm_mode = True
        allow_population_by_field_name = True


class Response(PydanticGenericModel, Generic[DataT]):
    """
    Базовый ответ на запрос
    """

    code: int = Field(200, description="Код ответа (http-like)")
    message: str | None = Field(description="Описание кода ответа")
    payload: DataT | None = Field(None, description="Тело ответа")

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
