"""Settings come from environment variables, never hard-coded in source.

This is the "12-factor app" rule: the same Docker image runs in dev, staging
and prod, and only the environment changes. Think of it like Ansible group_vars.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str  # read from the DATABASE_URL env var; the app refuses to start if it's missing


settings = Settings()
