from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Example Task Title")
    description: str = Field(..., example="Example task description goes here")
    status: Optional[str] = Field("pending", example="pending")
    due_date: Optional[str] = Field(None, example="2025-10-20")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated Task Title")
    description: Optional[str] = Field(None, example="Updated task description goes here")
    status: Optional[str] = Field(None, example="done")
    due_date: Optional[str] = Field(None, example="2025-10-25")
