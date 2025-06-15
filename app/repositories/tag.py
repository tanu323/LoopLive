from app.repositories.base import BaseRepository
from app.models.models import Tag
from app.core.collections import CollectionName

class TagRepository(BaseRepository[Tag]):
    def __init__(self):
        super().__init__(CollectionName.TAGS.value)
