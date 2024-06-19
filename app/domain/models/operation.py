from enum import StrEnum
from typing import Any
from pydantic import BaseModel
from abc import ABC


class Method(StrEnum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Operation(BaseModel):
    name: str
    summary: str | None = None
    description: str | None = None
    method: Method
    path: str
    response: Any


class Rule(BaseModel):
    content: str
