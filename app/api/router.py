from fastapi import APIRouter
from app.api.routes import auth, sinav

api_router = APIRouter(prefix="/api/v2")
api_router.include_router(auth.router)
api_router.include_router(sinav.router)
