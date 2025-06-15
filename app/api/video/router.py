from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from app.models.vedio_model import Video, VideoCreate
from app.services.vedio.video import VideoService
from app.services.s3 import S3Service
from app.api.deps import get_video_service, get_s3_service
from app.core.exceptions import AppException

router = APIRouter()

@router.post("/", response_model=Video)
async def upload_video(video: VideoCreate, video_service: VideoService = Depends(get_video_service) , s3: S3Service = Depends(get_s3_service)):
    try:
        url = await s3.upload_file(file, folder="profile_videos")
        await video_service.create_video(user_id, {"profile_picture_url": url}) 
        return {"profile_picture_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    return await video_service.create_video(video)

@router.get("/", response_model=List[Video])
async def list_videos(video_service: VideoService = Depends(get_video_service)):
    return await video_service.get_all_videos()

@router.get("/{video_id}", response_model=Video)
async def get_video(video_id: UUID, video_service: VideoService = Depends(get_video_service)):
    video = await video_service.get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.delete("/{video_id}")
async def delete_video(video_id: UUID, video_service: VideoService = Depends(get_video_service)):
    deleted = await video_service.delete_video(video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found or already deleted")
    return {"success": True}
