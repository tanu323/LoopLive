from typing import Optional, List, Any, Tuple, Generic, TypeVar
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.core.enums import PrivacySetting, VideoStatus
from schema import BaseResponse

T = TypeVar["T"]

# ---------------------- Video Schemas ---------------------- #

class VideoSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    s3_url: str
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    location: Optional[str] = None
    duration: Optional[float] = None
    upload_date: datetime
    views: int
    privacy: PrivacySetting
    is_featured: bool
    status: VideoStatus

    class Config:
        orm_mode = True

class VideoListResponse(BaseResponse[List[VideoSchema]]):
    data: List[VideoSchema]


class UploadURLResponse(BaseModel):
    url: str
    key: str


# ------------------ Upload ------------------

# VideoUploadRequestSchema is for pre-signed URL endpoint.

class VideoUploadRequestSchema(BaseModel):
    file_name: str
    content_type: str


# ------------------ Drafts ------------------

class VideoDraftCreateSchema(BaseModel):
    original_file_name: Optional[str] = None
    edited_file_name: Optional[str] = None
    trimmed_start: Optional[float] = None
    trimmed_end: Optional[float] = None
    applied_music_id: Optional[str] = None
    filters_applied: Optional[List[str]] = []
    stickers_applied: Optional[List[str]] = []
    location: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    privacy: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY


class VideoDraftUpdateSchema(BaseModel):
    edited_file_name: Optional[str]
    trimmed_start: Optional[float]
    trimmed_end: Optional[float]
    applied_music_id: Optional[str]
    filters_applied: Optional[List[str]]
    stickers_applied: Optional[List[str]]
    location: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    privacy: Optional[PrivacySetting]
    finalized: Optional[bool]


class VideoDraftResponseSchema(VideoDraftCreateSchema):
    draft_id: UUID
    status: VideoStatus
    created_at: datetime

    class Config:
        orm_mode = True

class FinalizeVideoRequestSchema(BaseModel):
    draft_id: UUID
    title: str
    thumbnail_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    location: Optional[str] = None
    privacy: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY
    status: VideoStatus = VideoStatus.PUBLISHED


# ------------------ Final Videos ------------------

class VideoCreateSchema(BaseModel):
    s3_url: str
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    location: Optional[str] = None
    duration: Optional[float] = None
    privacy: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY
    is_featured: bool = False


class VideoResponseSchema(VideoCreateSchema):
    video_id: UUID
    upload_date: datetime
    views: int
    status: VideoStatus

    class Config:
        orm_mode = True
