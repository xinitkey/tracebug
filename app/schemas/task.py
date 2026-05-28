from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_done: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(BaseModel):
    title: str | None = None 
    description: str | None = None
    is_done: bool | None = None
