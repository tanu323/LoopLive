from app.repositories.base import BaseRepository
from app.models.user_models import UserAuth
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from uuid import UUID
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class UserAuthRepository(BaseRepository[UserAuth]):
    def __init__(self,  collection: AsyncIOMotorCollection):
        super().__init__(collection, UserAuth)

    async def register_user(self, user: UserAuth) -> UserAuth:
        try:
            await self.collection.insert_one(user.model_dump(by_alias=True))
            logger.info(f"[Register User] Successfully registered user with email: {user.email}")
            return user
        except Exception as e:
            logger.error(f"[Register User] Failed to register user with email: {user.email} — Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed"
            )

    async def get_by_email(self, email: str) -> Optional[UserAuth]:
        try:
            user_data = await self.collection.find_one({"email": email})
            if user_data:
                logger.info(f"[Get User by Email] User found with email: {email}")
                return UserAuth(**user_data)
            logger.warning(f"[Get User by Email] No user found with email: {email}")
            return None
        except Exception as e:
            logger.error(f"[Get User by Email] Error while fetching user by email: {email} — Error: {e}")
            return None

    async def delete_user(self, userId: UUID) -> bool:
        try:
            result = await self.collection.delete_one({"id": str(userId)})
            if result.deleted_count == 1:
                logger.info(f"[Delete User] Successfully deleted user with ID: {userId}")
                return True
            logger.warning(f"[Delete User] No user found to delete with ID: {userId}")
            return False
        except Exception as e:
            logger.error(f"[Delete User] Failed to delete user with ID: {userId} — Error: {e}")
            return False
