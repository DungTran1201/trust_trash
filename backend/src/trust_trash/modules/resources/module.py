"""Module composition boundary for resources."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
