"""Models describe database TABLES. One class = one table, one attribute = one column.

SQLAlchemy turns this class into roughly:

    CREATE TABLE tasks (
        id          SERIAL PRIMARY KEY,
        title       VARCHAR(200) NOT NULL,
        description TEXT,
        done        BOOLEAN NOT NULL DEFAULT false,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
    );
"""
from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
