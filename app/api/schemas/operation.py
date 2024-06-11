from enum import StrEnum
from typing import Any, List

from pydantic import BaseModel, Field


class DataType(StrEnum):
    STR = "STR"
    CLASS = "CLASS"
    INT = "INT"
    BOOL = "BOOL"
    DICT = "DICT"
    LIST = "LIST"

    def is_class_type(self):
        return self == DataType.CLASS


class PrimitiveValue(BaseModel):
    value: Any


class ObjectValue(BaseModel):
    class_name: str = Field(default=None, description="Class name")
    base_classes: str | None = Field(default=None, description="Base classes name (separated by comma")
    attributes: dict = Field(default=None, description="Attributes")


class ListValue(BaseModel):
    data_type: DataType = Field(default=DataType.STR, description="Data type")
    values: List["DataTemplate"] | List[Any]


class DataTemplate(BaseModel):
    data_type: DataType | None = Field(default=None, description="Data type")
    primitive_value: PrimitiveValue | None = Field(default=None, description="Simple value")
    object_value: ObjectValue | None = Field(default=None, description="Object value")
    list_value: ListValue | None = Field(default=None, description="List value")


class CreateEndpointRequest(BaseModel):
    name: str
    summary: str
    description: str
    method: str
    path: str
    response: DataTemplate


class RegisteredEndpoint(BaseModel):
    endpoint: str
    status: str
