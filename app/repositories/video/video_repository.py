# app/repositories/video/video_repository.py

from app.models.vedio_model import Video
from app.repositories.base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorCollection
from uuid import UUID

class VideoRepository(BaseRepository[Video]):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def get_by_id(self, video_id: UUID) -> Video | None:
        doc = await self.collection.find_one({"video_id": video_id})
        return self.map_document(doc)
    
    # Common base methods can go here:
    # create_video, update_video, delete_video, search_videos, etc.
