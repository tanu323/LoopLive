from app.repositories.base import BaseRepository
from app.models.models import Message
from app.core.collections import CollectionName

class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(CollectionName.MESSAGES.value)
