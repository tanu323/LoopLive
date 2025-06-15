from typing import Generic, TypeVar, Type, Optional, List, Dict
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.models.base import DbBaseModel
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DbBaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        self.collection = collection
        self.model = model

    async def find_one(self, query: Dict) -> Optional[ModelType]:
        try:
            result = await self.collection.find_one(query)
            return self.model(**result) if result else None
        except Exception as e:
            logger.error(f"[Find One] Failed query={query}: {e}")
            raise

    async def find_by_id(self, id: UUID) -> Optional[ModelType]:
        try:
            return await self.find_one({"id": str(id)})
        except Exception as e:
            logger.error(f"[Find By ID] Failed for id={id}: {e}")
            return None

    async def find_all(self, query: Dict = None) -> List[ModelType]:
        query = query or {}
        try:
            cursor = self.collection.find(query)
            return [self.model(**doc) async for doc in cursor]
        except Exception as e:
            logger.error(f"[Find All] Failed for query={query}: {e}")
            raise

    async def create(self, data: Dict) -> ModelType:
        try:
            result = await self.collection.insert_one(data)
            logger.info(f"[Create] Document inserted with _id={result.inserted_id}")
            return await self.find_by_id(UUID(data["id"]))
        except Exception as e:
            logger.error(f"[Create] Failed to insert data={data}: {e}")
            raise

    async def update(self, id: UUID, data: Dict) -> Optional[ModelType]:
        try:
            result = await self.collection.update_one(
                {"id": str(id)},
                {"$set": data}
            )
            if result.modified_count == 1:
                logger.info(f"[Update] Document updated for id={id}")
                return await self.find_by_id(id)
            logger.warning(f"[Update] No document modified for id={id}")
            return None
        except Exception as e:
            logger.error(f"[Update] Failed for id={id} with data={data}: {e}")
            raise

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.collection.delete_one({"id": str(id)})
            if result.deleted_count == 1:
                logger.info(f"[Delete] Successfully deleted id={id}")
                return True
            logger.warning(f"[Delete] No document found for id={id}")
            return False
        except Exception as e:
            logger.error(f"[Delete] Failed to delete id={id}: {e}")
            raise

    async def get_profile_by_user_id(self, user_id: UUID) -> Optional[ModelType]:
        try:
            result = await self.collection.find_one({"user_id": user_id})
            return self.model(**result) if result else None
        except Exception as e:
            logger.error(f"[Get By User ID] Failed for user_id={user_id}: {e}")
            raise
    

    async def get_by_field(self, field: str, value) -> Optional[ModelType]:
        try:
            result = await self.collection.find_one({field: str(value)})
            return self.model(**result) if result else None
        except Exception as e:
            logger.error(f"[BaseRepository] Failed get_by_field {field}={value}: {e}")
            return None

    async def delete_by_field(self, field: str, value) -> bool:
        try:
            result = await self.collection.delete_one({field: str(value)})
            return result.deleted_count == 1
        except Exception as e:
            logger.error(f"[BaseRepository] Failed delete_by_field {field}={value}: {e}")
            return False
