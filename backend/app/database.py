"""Database connection setup.

- engine: manages a pool of connections to Postgres (reused, not opened per request)
- SessionLocal: a factory that hands out a "session", which is one unit of work / transaction
- get_db: FastAPI calls this for every request that needs the DB, then closes the session afterwards
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Every table model inherits from this."""


def get_db():
    db = SessionLocal()
    try:
        yield db          # the request handler runs here
    finally:
        db.close()        # always runs, even if the handler raised an error
