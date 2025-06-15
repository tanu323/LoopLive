from pydantic import Field, EmailStr
from typing import Optional, List, Any, Tuple
from base import DbBaseModel
from datetime import datetime
from uuid import UUID, uuid4
from app.core.enums import (
    PrivacySetting,
    CallStatus,
    SignalingMessageType,
    MatchmakingStatus,
    VideoStatus,
    ConversationType,
)


# ---------------------- Video ------------------------------- #

class Video(DbBaseModel):
    video_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    s3_url: str
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    location: Optional[str] = None
    duration: Optional[float] = None
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    views: int = 0
    privacy: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY
    is_featured: bool = False
    status: VideoStatus = VideoStatus.PUBLISHED


class VideoUploadRequest(DbBaseModel):      #or generating a presigned URL to upload to S3, unrelated to editing or publishing logic.
    user_id: UUID
    file_name: str
    content_type: str

# ---------------------- Video Editing  -------------- #    

class VideoDraft(DbBaseModel):
    draft_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    original_file_name: Optional[str] = None
    edited_file_name: Optional[str] = None

    # Editing fields
    trimmed_start: Optional[float] = None
    trimmed_end: Optional[float] = None
    applied_music_id: Optional[str] = None
    filters_applied: Optional[List[str]] = []
    stickers_applied: Optional[List[str]] = []

    # Post settings
    location: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    privacy: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY
    status: VideoStatus = VideoStatus.DRAFT

    finalized: bool = False



    