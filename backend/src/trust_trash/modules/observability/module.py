"""Module composition boundary for observability."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
