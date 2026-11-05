"""Module composition boundary for processing."""

from fastapi import APIRouter
from .presentation.router import router


def get_router() -> APIRouter:
    return router
