"""Schemas describe the JSON that goes IN and OUT of the API.

Why separate from models? Because what's stored and what's exposed are different things.
In Phase 3 a User will have a `password_hash` column, and you never want that in an API
response. Schemas are the bouncer at the door.

They're also your first security layer: FastAPI rejects any request whose body doesn't
match (wrong types, missing fields, a 10,000-character title) with a 422 error before
your code ever runs. That's "input validation".
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """What a client sends to create a task."""
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)


class TaskUpdate(BaseModel):
    """What a client sends to edit a task. Every field is optional, so a client can change just one."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    done: bool | None = None


class TaskOut(BaseModel):
    """What the API sends back."""
    model_config = ConfigDict(from_attributes=True)  # allow building this straight from a SQLAlchemy object

    id: int
    title: str
    description: str | None
    done: bool
    created_at: datetime
