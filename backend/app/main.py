"""Application entry point. Uvicorn (the web server) loads the `app` object from here."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, create any tables that don't exist yet.
    # Fine for learning. In Phase 3 we replace this with Alembic migrations,
    # which are version-controlled schema changes (like Ansible, but for your database).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="TaskTrack API", lifespan=lifespan)
app.include_router(tasks.router)


@app.get("/health", tags=["ops"])
def health():
    """For load balancers, Docker healthchecks and uptime monitors."""
    return {"status": "ok"}
