from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Body, Path
from uuid import UUID
import logging
from app.schemas.video_schema import (
    VideoUploadRequestSchema,
    VideoDraftCreateSchema,
    VideoDraftUpdateSchema,
    VideoDraftResponseSchema,
    FinalizeVideoRequestSchema,     # to convert a draft into a published video.
    VideoResponseSchema,
    UploadURLResponse
)
from app.schemas.user_schema import UserData
from app.services.video.video_create_service import VideoCreateService
from app.services.s3 import S3Service
from app.api.deps import get_video_service, get_s3_service
from app.api.auth.jwt import get_logged_in_user

logger = logging.getLogger(__name__)
video_create_router = APIRouter()

# This route allows the frontend/client to obtain a secure pre-signed URL from AWS S3 to directly upload a video file.
@video_create_router.post("/upload-url", response_model=UploadURLResponse)
async def generate_upload_url(
    upload_request: VideoUploadRequestSchema,
    s3_service: S3Service = Depends(get_s3_service),  # Inject directly or through deps
    current_user: UserData = Depends(get_logged_in_user),
):
    try:
        url = s3_service.generate_presigned_upload_url(
            folder=f"videos/{current_user.user_id}",
            filename=upload_request.file_name,
            content_type=upload_request.content_type
        )
        logger.info(f"[Upload URL] Generated for user_id={current_user.user_id}")
        return url
    except Exception as e:
        logger.error(f"[Upload URL] Generation failed for user_id={current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")


# When the user clicks "Start Editing", an empty or partially filled draft is created in the DB.
@video_create_router.post("/drafts", response_model=VideoDraftResponseSchema)
async def create_video_draft(
    draft_data: VideoDraftCreateSchema,
    service: VideoCreateService = Depends(get_video_service),
    current_user: UserData = Depends(get_logged_in_user),
):
    try:
        draft = await service.create_draft(draft_data, current_user.user_id)
        logger.info(f"[Create Draft] Draft created for user_id={current_user.user_id}")
        return draft
    except Exception as e:
        logger.error(f"[Create Draft] Failed for user_id={current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create video draft")


# video editing is often a multi-step process that can take time, and users may need to save their progress incrementally. This makes the app more robust against crashes or interruptions, allowing users to resume editing later without losing changes.

@video_create_router.patch("/drafts/{draft_id}", response_model=VideoDraftResponseSchema)
async def update_video_draft(
    draft_id: UUID = Path(...),
    updates: VideoDraftUpdateSchema = Body(...),
    service: VideoCreateService = Depends(get_video_service),
    current_user: UserData = Depends(get_logged_in_user),
):
    try:
        updated = await service.update_draft(draft_id, current_user.user_id, updates)
        logger.info(f"[Update Draft] Draft {draft_id} updated by user_id={current_user.user_id}")
        return updated
    except Exception as e:
        logger.error(f"[Update Draft] Failed for draft_id={draft_id}, user_id={current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update video draft")

@video_create_router.post("/finalize", response_model=VideoResponseSchema)
async def finalize_draft_to_video(
    finalize_request: FinalizeVideoRequestSchema,
    service: VideoCreateService = Depends(get_video_service),
    s3_service: S3Service = Depends(get_s3_service),
    background_tasks: BackgroundTasks = Depends(),
    current_user: UserData = Depends(get_logged_in_user),
):
    try:
        video, original_file_url = await service.finalize_draft(draft_id=finalize_request.draft_id,
            user_id=current_user.user_id )
        logger.info(f"[Finalize Draft] Video finalized for user_id={finalize_request.user_id}")

        # Clean up original file in the background (optional safety check)
        if original_file_url:
            background_tasks.add_task(s3_service.delete_file, original_file_url)
            logger.info(f"[Finalize Draft] Scheduled deletion of original file: {original_file_url}")

        return video
    except Exception as e:
        logger.error(f"[Finalize Draft] Failed for draft_id={finalize_request.draft_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to finalize video draft")




