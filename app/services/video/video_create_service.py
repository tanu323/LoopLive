# app/services/video/video_create_service.py

from app.repositories.video.video_create_repository import VideoCreateRepository
from app.services.s3 import S3Service
from app.models.vedio_model import VideoDraft, Video
from app.schemas.video_schema import (
    VideoDraftCreateSchema,
    VideoDraftUpdateSchema,
    FinalizeVideoRequestSchema,
    VideoDraftResponseSchema,
    VideoResponseSchema
)
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.core.enums import VideoStatus

class VideoCreateService:
    def __init__(self, repo: VideoCreateRepository, s3_service: S3Service):
        self.repo = repo
        self.s3_service = s3_service

    # --- Create Draft ---
    async def create_draft(self, draft_data: VideoDraftCreateSchema, user_id: UUID) -> VideoDraftResponseSchema:
        draft = VideoDraft(
            draft_id=uuid4(),
            user_id=user_id,
            original_file_name=draft_data.original_file_name,
            edited_file_name=draft_data.edited_file_name,
            trimmed_start=draft_data.trimmed_start,
            trimmed_end=draft_data.trimmed_end,
            applied_music_id=draft_data.applied_music_id,
            filters_applied=draft_data.filters_applied,
            stickers_applied=draft_data.stickers_applied,
            location=draft_data.location,
            description=draft_data.description,
            tags=draft_data.tags,
            privacy=draft_data.privacy,
            status=VideoStatus.DRAFT,
            finalized=False,
        )
        saved_draft = await self.repo.create_draft(draft)
        return VideoDraftResponseSchema(
            draft_id=saved_draft.draft_id,
            status=saved_draft.status,
            created_at=saved_draft.created_at,
            **draft_data.model_dump()
        )

    # --- Update Draft ---
    async def update_draft(self, draft_id: UUID, user_id: UUID, updates: VideoDraftUpdateSchema) -> VideoDraftResponseSchema:
        update_data = updates.model_dump(exclude_unset=True)
        updated_draft = await self.repo.update_draft(draft_id, user_id, update_data)

        if not updated_draft:
            raise ValueError("Draft not found or access denied")

        return VideoDraftResponseSchema(
            draft_id=updated_draft.draft_id,
            status=updated_draft.status,
            created_at=updated_draft.created_at,
            original_file_name=updated_draft.original_file_name,
            edited_file_name=updated_draft.edited_file_name,
            trimmed_start=updated_draft.trimmed_start,
            trimmed_end=updated_draft.trimmed_end,
            applied_music_id=updated_draft.applied_music_id,
            filters_applied=updated_draft.filters_applied,
            stickers_applied=updated_draft.stickers_applied,
            location=updated_draft.location,
            description=updated_draft.description,
            tags=updated_draft.tags,
            privacy=updated_draft.privacy,
        )

    # --- Finalize Draft ---
    async def finalize_draft(self, draft_id: UUID, user_id: UUID) -> tuple[VideoResponseSchema, str | None]:
        draft = await self.repo.get_draft_by_id_and_user(draft_id, user_id)
        if not draft:
            raise ValueError("Draft not found or access denied")

        if draft.finalized:
            raise ValueError("Draft already finalized")

        # Create video from draft
        video = Video(
            video_id=uuid4(),
            user_id=user_id,
            s3_url=draft.edited_file_name,
            thumbnail_url=None,  # optional enhancement
            description=draft.description,
            location=draft.location,
            tags=draft.tags,
            privacy=draft.privacy,
            upload_date=datetime.now(timezone.utc),
            views=0,
            is_featured=False,
            status=VideoStatus.PUBLISHED,
        )
        saved_video = await self.repo.create_video(video)

        # Mark draft finalized
        await self.repo.mark_draft_finalized(draft_id)

        response = VideoResponseSchema(
            video_id=saved_video.video_id,
            s3_url=saved_video.s3_url,
            thumbnail_url=saved_video.thumbnail_url,
            description=saved_video.description,
            tags=saved_video.tags,
            location=saved_video.location,
            duration=saved_video.duration,
            privacy=saved_video.privacy,
            is_featured=saved_video.is_featured,
            views=saved_video.views,
            status=saved_video.status,
            upload_date=saved_video.upload_date,
        )

        # Return original file URL for cleanup (if any)
        return response, draft.original_file_name
