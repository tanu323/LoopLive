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

 


#  ---------------------- Authentication ---------------------- #

class UserAuth(DbBaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    username: str
    hashed_password: str

# ---------------------- User Profile ------------------------ #

class UserProfile(DbBaseModel):
    user_id: UUID
    display_name: str
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    privacy_setting: PrivacySetting = PrivacySetting.FOLLOWERS_ONLY
    is_verified: bool = False
    uploaded_videos: List[UUID] = Field(default_factory=list)

class UserProfileUpdate(DbBaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    privacy_setting: Optional[PrivacySetting] = None
    is_verified: Optional[bool] = None
    uploaded_videos: Optional[List[UUID]] = None


# ---------------------- Message ----------------------------- #