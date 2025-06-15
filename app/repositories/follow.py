from app.repositories.base import BaseRepository
from app.models.models import Follow
from app.core.collections import CollectionName

class FollowRepository(BaseRepository[Follow]):
    def __init__(self):
        super().__init__(CollectionName.FOLLOWS.value)
