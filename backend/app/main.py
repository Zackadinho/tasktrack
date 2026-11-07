"""Application entry point. Uvicorn (the web server) loads the `app` object from here."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
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

# CORS (Cross-Origin Resource Sharing):
# The frontend runs on localhost:5173 and the API on localhost:8000. To a browser those
# are different "origins", and by default it BLOCKS JavaScript from reading responses
# across origins. That rule stops evil.com from quietly calling your bank's API with
# your cookies. This middleware tells the browser which origins we trust.
# Never use allow_origins=["*"] once logins exist.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(tasks.router)


@app.get("/health", tags=["ops"])
def health():
    """For load balancers, Docker healthchecks and uptime monitors."""
    return {"status": "ok"}
