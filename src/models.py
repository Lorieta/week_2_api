from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str
    done: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
