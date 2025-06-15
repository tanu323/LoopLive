# app/services/base.py
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.repositories.base import BaseRepository
from typing import Optional, Tuple, Dict
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger()

class BaseService:
    def __init__(self, base_repo: BaseRepository):
        self.base_repo = base_repo 


    async def get_by_user_id(self, user_id: UUID):
        try:
            data = await self.base_repo.get_profile_by_user_id(user_id)
            if not data:
                logger.warning(f"[BaseService] No data found for user_id={user_id}")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given UserID resource was not found")
            logger.info(f"[BaseService] Successfully retrieved data for user_id={user_id}")
            return data
        except Exception as e:
            logger.error(f"[BaseService] Failed to fetch user by user_id={user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal error during user retrieval")

    

    async def get_by_field(self, field: str, value) -> Optional[Dict]:
        try:
            return await self.base_repo.get_by_field(field, value)
        except Exception as e:
            logger.error(f"[BaseService] Failed get_by_field {field}={value}: {e}")
            raise HTTPException(status_code=500, detail="Internal error during get_by_field")


    async def delete_by_user_id(self, user_id: UUID) -> bool:
        try:
            return await self.base_repo.delete_by_field("user_id", user_id)
        except Exception as e:
            logger.error(f"[BaseService] Failed delete_by_user_id={user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal error during delete")
