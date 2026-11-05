"""Module composition boundary for connections."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
