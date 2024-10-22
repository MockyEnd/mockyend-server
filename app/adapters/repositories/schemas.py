from typing import Any
from pydantic import BaseModel, Field

from app.domain.models.operation import Method, DataType


class OperationCreate(BaseModel):
	name: str = Field(..., description="The name of the operation")
	summary: str = Field(..., description="The summary of the operation")
	description: str = Field(..., description="The description of the operation")
	method: Method = Field(..., description="The HTTP method of the operation")
	path: str = Field(..., description="The path of the operation")
	response_type: DataType | None = Field(..., description="Type of the content response")
	response_content: Any | None = Field(..., description="The content of the response")
