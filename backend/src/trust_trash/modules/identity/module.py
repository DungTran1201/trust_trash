"""Module composition boundary for identity."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
