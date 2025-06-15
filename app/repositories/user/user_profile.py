from typing import List, Optional, Dict
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.user_models import UserProfile
from app.repositories.base import BaseRepository
from app.core.collections import CollectionName
import logging

logger = logging.getLogger(__name__)

class UserProfileRepository(BaseRepository[UserProfile]):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection, UserProfile)

    async def create(self, profile_data: UserProfile) -> UserProfile:
        try:
            await self.collection.insert_one(profile_data.model_dump(by_alias=True))
            logger.info(f"[Create Profile] Successfully created profile for user_id={profile_data.user_id}")
            return profile_data
        except Exception as e:
            logger.error(f"[Create Profile] Failed to create profile for user_id={profile_data.user_id}: {e}")
            raise

    async def update_profile(self, user_id: UUID, updates: dict) -> Optional[UserProfile]:
        try:
            result = await self.collection.update_one({"user_id": user_id}, {"$set": updates})
            if result.modified_count == 0:
                logger.warning(f"[Update Profile] No changes made for user_id={user_id}")
            else:
                logger.info(f"[Update Profile] Successfully updated profile for user_id={user_id}")
            return await self.get_by_user_id(user_id)
        except Exception as e:
            logger.error(f"[Update Profile] Failed to update profile for user_id={user_id}: {e}")
            raise

    async def search(self, query: str, skip: int = 0, limit: int = 10) -> List[UserProfile]:
        """
        Perform a case-insensitive regex search on display_name.
        """
        try:
            cursor = (
                self.collection
                .find({"display_name": {"$regex": query, "$options": "i"}})
                .skip(skip)
                .limit(limit)
            )
            results = [UserProfile(**doc) async for doc in cursor]
            logger.info(f"[Search Profiles] Found {len(results)} profiles matching query='{query}'")
            return results
        except Exception as e:
            logger.error(f"[Search Profiles] Search failed for query='{query}': {e}")
            raise
