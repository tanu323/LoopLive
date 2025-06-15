
from typing import Optional, List, Any, Tuple, Generic, TypeVar
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from schema import BaseResponse
from app.core.enums import (
    PrivacySetting,
    CallStatus,
    SignalingMessageType,
    MatchmakingStatus,
    VideoStatus,
    ConversationType,
)

T = TypeVar("T")


# ---------------------- User Profile Schemas ---------------------- #

class UserProfileSchema(BaseModel):
    user_id: UUID
    display_name: str
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    privacy_setting: PrivacySetting
    is_verified: bool
    uploaded_videos: List[UUID]

    class Config:
        orm_mode = True

class UserProfileUpdateSchema(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    privacy_setting: Optional[PrivacySetting] = None
    is_verified: Optional[bool] = None
    uploaded_videos: Optional[List[UUID]] = None

    class Config:
        orm_mode = True

class ProfileResponse(BaseResponse[UserProfileSchema]):
    data: UserProfileSchema

# ---------------------- Auth Schemas ---------------------- #

class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenResponse(BaseResponse[TokenData]):
    data: TokenData

class UserData(BaseModel):
    user_id: UUID
    email: EmailStr
    username: str

class UserResponse(BaseResponse[UserData]):
    data: UserData