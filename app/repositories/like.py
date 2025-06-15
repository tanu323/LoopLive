from app.repositories.base import BaseRepository
from app.models.models import Like
from app.core.collections import CollectionName

class LikeRepository(BaseRepository[Like]):
    def __init__(self):
        super().__init__(CollectionName.LIKES.value)
