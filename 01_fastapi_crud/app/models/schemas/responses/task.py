from pydantic import BaseModel, Field
from typing import Optional

class TaskOut(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Example Task Title")
    description: str = Field(..., example="Example task description goes here")
    status: str = Field(..., example="pending")
    due_date: Optional[str] = Field(None, example="2025-10-20")
