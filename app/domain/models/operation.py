from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models.base import AuditModel


class Method(StrEnum):
	GET = "GET"
	HEAD = "HEAD"
	POST = "POST"
	PUT = "PUT"
	PATCH = "PATCH"
	DELETE = "DELETE"


class DataType(StrEnum):
	STR = "STR"
	CLASS = "CLASS"
	INT = "INT"
	BOOL = "BOOL"
	DICT = "DICT"
	LIST = "LIST"


class Operation(AuditModel):
	id: int | None = Field(None, description="Operation ID.")
	uuid: UUID | None = Field(None, description="Operation UUID. (External ID)")
	name: str | None = Field(None, description="The name to identify an operation")
	summary: str | None = Field(None, description="The summary of an operation")
	description: str | None = Field(None, description="The description of an operation")
	method: Method = Field(..., description="HTTP Method of an operation")
	path: str | None = Field(None, description="The path of an operation")
	response_type: DataType | None = Field(None, description="Type of the content response")
	response_content: Any | None = Field(None, description="The content of the response")


class Rule(BaseModel):
	content: str
