"""Settings come from environment variables, never hard-coded in source.

This is the "12-factor app" rule: the same Docker image runs in dev, staging
and prod, and only the environment changes. Think of it like Ansible group_vars.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str  # read from the DATABASE_URL env var; the app refuses to start if it's missing

    # Which websites (origins) the browser may let call this API. See main.py for CORS.
    # Comma-separated in the env var, e.g. CORS_ORIGINS=http://localhost:5173,https://tasktrack.example.com
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
