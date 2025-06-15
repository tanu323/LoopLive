from typing import Optional, List, Any, Tuple, Generic, TypeVar
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from app.core.enums import (
    PrivacySetting,
    CallStatus,
    SignalingMessageType,
    MatchmakingStatus,
    VideoStatus,
    ConversationType,
)

T = TypeVar("T")

# ---------------------- Generic API Response Wrapper ---------------------- #

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None



# ---------------------- Comment Schemas ---------------------- #

class CommentSchema(BaseModel):
    id: UUID
    user_id: UUID
    video_id: UUID
    text: str

class CommentListResponse(BaseResponse[List[CommentSchema]]):
    data: List[CommentSchema]


# ---------------------- Like Schemas ---------------------- #

class LikeSchema(BaseModel):
    id: UUID
    user_id: UUID
    video_id: UUID

class LikeListResponse(BaseResponse[List[LikeSchema]]):
    data: List[LikeSchema]


# ---------------------- Follow Schemas ---------------------- #

class FollowSchema(BaseModel):
    id: UUID
    follower_user_id: UUID
    following_user_id: UUID

class FollowListResponse(BaseResponse[List[FollowSchema]]):
    data: List[FollowSchema]



# ---------------------- Message & Conversation Schemas ---------------------- #

class MessageSchema(BaseModel):
    id: UUID
    sender_user_id: UUID
    receiver_user_id: UUID
    text: str
    read: bool
    read_at: Optional[datetime]
    timestamp: datetime

class ConversationSchema(BaseModel):
    id: UUID
    user_ids: List[UUID]
    last_message_at: Optional[datetime]
    type: ConversationType

class ConversationListResponse(BaseResponse[List[ConversationSchema]]):
    data: List[ConversationSchema]


# ---------------------- Call Session Schemas ---------------------- #

class CallSessionSchema(BaseModel):
    id: UUID
    caller_id: UUID
    receiver_id: UUID
    status: CallStatus
    started_at: datetime
    ended_at: Optional[datetime]
    signaling_info: Optional[dict[str, Any]]

class AnonymousCallSessionSchema(BaseModel):
    id: UUID
    user_a_id: UUID
    user_b_id: Optional[UUID]
    status: CallStatus
    started_at: datetime
    ended_at: Optional[datetime]


# ---------------------- Matchmaking Queue Schema ---------------------- #

class MatchmakingEntrySchema(BaseModel):
    user_id: UUID
    status: MatchmakingStatus
    matched_with: Optional[UUID]
    joined_at: datetime
    updated_at: Optional[datetime]


# ---------------------- WebRTC Signaling ---------------------- #

class SignalingMessageSchema(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    call_id: Optional[UUID] = None
    type: SignalingMessageType
    data: dict[str, Any]
    timestamp: datetime
    acknowledged_at: Optional[datetime]
