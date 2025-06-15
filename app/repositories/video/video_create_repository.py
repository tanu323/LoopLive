# app/repositories/video/video_create_repository.py

from app.models.vedio_model import VideoDraft, Video
from app.repositories.base import BaseRepository
from app.repositories.video.video_repository import VideoRepository
from motor.motor_asyncio import AsyncIOMotorCollection
from uuid import UUID

class VideoCreateRepository:
    def __init__(self, video_repo: VideoRepository, draft_collection: AsyncIOMotorCollection):
        self.video_repo = video_repo
        self.draft_collection = draft_collection

    # --- Draft related ---

    async def create_draft(self, draft: VideoDraft) -> VideoDraft:
        await self.draft_collection.insert_one(draft.model_dump())
        return draft

    async def get_draft_by_id_and_user(self, draft_id: UUID, user_id: UUID) -> VideoDraft | None:
        doc = await self.draft_collection.find_one({
            "draft_id": draft_id,
            "user_id": user_id
        })
        return self.map_draft(doc)

    async def update_draft(self, draft_id: UUID, user_id: UUID, update_data: dict) -> VideoDraft | None:
        doc = await self.draft_collection.find_one_and_update(
            {"draft_id": draft_id, "user_id": user_id},
            {"$set": update_data},
            return_document=True 
        )
        return self.map_draft(doc)

    async def mark_draft_finalized(self, draft_id: UUID):
        await self.draft_collection.update_one(
            {"draft_id": draft_id},
            {"$set": {"finalized": True}}
        )

    # --- Final video creation ---

    async def create_video(self, video: Video) -> Video:
        return await self.video_repo.create_video(video)

    # --- Helper ---

    def map_draft(self, doc: dict | None) -> VideoDraft | None:
        if not doc:
            return None
        return VideoDraft(**doc)
