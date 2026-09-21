"""
Central API Router.

Author: Harsh Aryan
Project: Cognisys
"""

from fastapi import APIRouter
from app.api.v1.intelligence import router as intelligence_router
from app.api.v1.repository import router as repository_router
from app.api.v1.analysis import router as analysis_router

api_router = APIRouter()

api_router.include_router(repository_router)
api_router.include_router(analysis_router)
api_router.include_router(intelligence_router)