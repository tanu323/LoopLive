from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.mongo import get_database  # Assuming this is from your mongo.py
from app.repositories.video.video_repository import VideoRepository
from app.repositories.user.user_auth import UserAuthRepository
from app.repositories.user.user_profile import UserProfileRepository
from app.repositories.comment import CommentRepository
from app.repositories.like import LikeRepository
from app.repositories.message import MessageRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.follow import FollowRepository
from app.repositories.tag import TagRepository

from app.services.vedio.video import VideoService
from app.services.user.user_profile import UserProfileService
from app.services.user.user_auth import UserAuthService
from app.services.comment import CommentService
from app.services.like import LikeService
from app.services.message import MessageService
from app.services.conversation import ConversationService
from app.services.follow import FollowService
from app.services.tag import TagService
from app.services.s3 import S3Service

from app.core.collections import CollectionName
# Initialize DB (shared across app)
db: AsyncIOMotorDatabase | None = None
async def initialize_db():
    """Initialize MongoDB connection."""
    global db
    db = get_database()
# Singleton dependency storage
dependency_storage = None
class DependencyStorage:
    def __init__(self):
        if db is None:
            raise RuntimeError("Database not initialized")
        # Repositories
        self._user_auth_repo = UserAuthRepository(db[CollectionName.USER_AUTH.value])
        self._user_profile_repo = UserProfileRepository(db[CollectionName.USER_PROFILES.value])
        self._video_repo = VideoRepository(db[CollectionName.VIDEOS.value])
        self._comment_repo = CommentRepository(db[CollectionName.COMMENTS.value])
        self._like_repo = LikeRepository(db[CollectionName.LIKES.value])
        self._message_repo = MessageRepository(db[CollectionName.MESSAGES.value])
        self._conversation_repo = ConversationRepository(db[CollectionName.CONVERSATIONS.value])
        self._follow_repo = FollowRepository(db[CollectionName.FOLLOWS.value])
        self._tag_repo = TagRepository(db[CollectionName.TAGS.value])

        # Services
        self._video_service = VideoService(video_repository=self._video_repo)
        self._user_auth_service = UserAuthService(user_repository=self._user_repo)
        self._user_profile_service = UserProfileService(user_repository=self._user_repo)
        self._comment_service = CommentService(comment_repository=self._comment_repo)
        self._like_service = LikeService(like_repository=self._like_repo)
        self._message_service = MessageService(message_repository=self._message_repo)
        self._conversation_service = ConversationService(conversation_repository=self._conversation_repo)
        self._follow_service = FollowService(follow_repository=self._follow_repo)
        self._tag_service = TagService(tag_repository=self._tag_repo)
        self._s3_service = S3Service()


    # Repository Getters
    def get_video_repository(self) -> VideoRepository:
        return self._video_repo
    def get_user_profile_repository(self) -> UserProfileRepository:
        return self._user_profile_repo
    def get_user_auth_repository(self) -> UserAuthRepository:
        return self._user_auth_repo
    def get_comment_repository(self) -> CommentRepository:
        return self._comment_repo
    def get_like_repository(self) -> LikeRepository:
        return self._like_repo
    def get_message_repository(self) -> MessageRepository:
        return self._message_repo
    def get_conversation_repository(self) -> ConversationRepository:
        return self._conversation_repo
    def get_follow_repository(self) -> FollowRepository:
        return self._follow_repo
    def get_tag_repository(self) -> TagRepository:
        return self._tag_repo
    
    # Service Getters
    def get_user_profile_service(self) -> UserProfileService:
        return self._user_profile_service
    def get_user_auth_service(self) -> UserAuthService:
        return self._user_auth_service
    def get_video_service(self) -> VideoService:
        return self._video_service
    def get_comment_service(self) -> CommentService:
        return self._comment_service
    def get_like_service(self) -> LikeService:
        return self._like_service
    def get_message_service(self) -> MessageService:
        return self._message_service
    def get_conversation_service(self) -> ConversationService:
        return self._conversation_service
    def get_follow_service(self) -> FollowService:
        return self._follow_service
    def get_tag_service(self) -> TagService:
        return self._tag_service
    def get_s3_service(self) -> S3Service:
        return self._s3_service

async def initialize_dependencies():
    """Initialize all dependencies."""
    global dependency_storage
    await initialize_db()
    dependency_storage = DependencyStorage()
# Dependency getters
def get_video_repository() -> VideoRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_video_repository()
def get_user_auth_repository() -> UserAuthRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_user_auth_repository()
def get_user_profile_repository() -> UserProfileRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_user_profile_repository()
def get_comment_repository() -> CommentRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_comment_repository()
def get_like_repository() -> LikeRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_like_repository()
def get_message_repository() -> MessageRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_message_repository()
def get_conversation_repository() -> ConversationRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_conversation_repository()
def get_follow_repository() -> FollowRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_follow_repository()
def get_tag_repository() -> TagRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_tag_repository()


def get_video_service() -> VideoService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_video_service()
def get_user_auth_service() -> UserAuthService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_user_auth_service()
def get_user_profile_service() -> UserProfileService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_user_profile_service()
def get_comment_service() -> CommentService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_comment_service()
def get_like_service() -> LikeService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_like_service()
def get_message_service() -> MessageService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_message_service()
def get_conversation_service() -> ConversationService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_conversation_service()
def get_follow_service() -> FollowService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_follow_service()
def get_tag_service() -> TagService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_tag_service()
def get_s3_service() -> S3Service:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_s3_service()