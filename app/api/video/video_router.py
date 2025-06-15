from fastapi import APIRouter
from app.api.video.video_create_router import router as create_router
from app.api.video.video_explore_router import router as explore_router
from app.api.video.video_interact_router import router as interact_router
from app.api.video.video_manage_router import router as manage_router

video_router = APIRouter()

# Include all sub-routers into one
video_router.include_router(create_router)
video_router.include_router(manage_router)
video_router.include_router(explore_router)
video_router.include_router(interact_router)