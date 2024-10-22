from datetime import datetime

from pydantic import BaseModel, Field


class AuditModel(BaseModel):
	created_at: datetime | None = Field(None, description="Timestamp of creation.")
	updated_at: datetime | None = Field(None, description="Timestamp of last update.")
