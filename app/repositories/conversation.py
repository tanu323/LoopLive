from app.repositories.base import BaseRepository
from app.models.models import Conversation
from app.core.collections import CollectionName

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(CollectionName.CONVERSATIONS.value)
