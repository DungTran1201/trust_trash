"""Module composition boundary for governance."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
