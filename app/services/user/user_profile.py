
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import Optional, Tuple, dict, List
from app.models.user_models import UserProfile, UserProfileUpdate
from app.repositories.user.user_profile import UserProfileRepository
from app.schemas.user_schema import UserRegisterRequest
from app.core.logging import get_logger
from app.services.base import BaseService

logger = get_logger()

# user_profile_service.py
class UserProfileService(BaseService):

    def __init__(self, profile_repo: UserProfileRepository):    
        
        """
        This line calls the constructor of the parent class BaseService, passing profile_repo to it.

        It's likely that BaseService uses this UserProfileRepository to provide basic CRUD (Create, Read, Update, Delete) operations.
        
        """
        
        super().__init__(profile_repo)
        self.profile_repo = profile_repo


    async def create_profile(self, profile_data: UserProfile) -> UserProfile:
        try:
            created = await self.profile_repo.create(profile_data)
            logger.info(f"[Create Profile] Successfully created profile for user_id={created.user_id}")
            return created
        except Exception as e:
            logger.error(f"[Create Profile] Failed to create profile for user_id={profile_data.user_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to create profile")


    async def get_profile(self, user_id: UUID) -> UserProfile:
        try:
            profile = await self.get_by_user_id(user_id)
            logger.info(f"[Get Profile] Retrieved profile for user_id={user_id}")
            return profile
        except HTTPException:
            logger.error(f"[Get Profile] Profile not found for user_id={user_id}")
            raise
        except Exception as e:
            logger.error(f"[Get Profile] Unexpected error while retrieving profile for user_id={user_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve profile")
        

    async def update_profile(self, user_id: UUID, update_data: UserProfileUpdate) -> UserProfile:
        existing_profile = await self.get_by_user_id(user_id)
        if not existing_profile:
            logger.error(f"[Update Profile] No profile found for user_id={user_id}. Update aborted.")
            raise HTTPException(status_code=404, detail="Profile not found")

        # Safely extract update dict
        try:
            if isinstance(update_data, UserProfileUpdate):
                update_dict = update_data.model_dump(exclude_unset=True)
            elif isinstance(update_data, dict):
                update_dict = update_data
            else:
                logger.error(f"[Update Profile] Invalid update_data type for user_id={user_id}. Expected dict or UserProfileUpdate.")
                raise HTTPException(status_code=400, detail="Invalid format of update_data in update_profile route")
        except Exception as e:
            logger.error(f"[Update Profile] Failed to parse update_data for user_id={user_id}: {e}")
            raise HTTPException(status_code=400, detail="Invalid update payload")

        # Attempt profile update
        try:
            updated = await self.profile_repo.update_profile(user_id, update_dict)
            if not updated:
                logger.error(f"[Update Profile] No changes applied for user_id={user_id}. Update may have failed silently.")
                raise HTTPException(status_code=500, detail="Update failed")
            logger.info(f"[Update Profile] Successfully updated profile for user_id={user_id}")
            return updated

        except Exception as e:
            logger.error(f"[Update Profile] Unexpected error while updating profile for user_id={user_id}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Update failed")


    async def search_profiles(self, query: str, skip: int = 0, limit: int = 10) -> List[UserProfile]:
        try:
            results = await self.profile_repo.search(query=query, skip=skip, limit=limit)
            logger.info(f"[Search Profiles] Returned {len(results)} profiles for query='{query}' (skip={skip}, limit={limit})")
            return results
        except Exception as e:
            logger.error(f"[Search Profiles] Failed to search profiles with query='{query}': {e}")
            raise HTTPException(status_code=500, detail="Search failed")