from app.repositories.base import BaseRepository
from app.models.models import Comment
from app.core.collections import CollectionName

class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(CollectionName.COMMENTS.value)
