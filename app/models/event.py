from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None  # Made optional
    datetime: datetime
