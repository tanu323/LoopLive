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

# ---------------------- Comment ----------------------------- #

class Comment(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    video_id: UUID
    text: str


# ---------------------- Like -------------------------------- #

class Like(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    video_id: UUID


# ---------------------- Follow ------------------------------ #

class Follow(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    follower_user_id: UUID
    following_user_id: UUID


# ---------------------- Tag --------------------------------- #

class Tag(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str




# ---------------------- Call Session ------------------------- #

class CallSession(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    caller_id: UUID
    receiver_id: UUID
    status: CallStatus = CallStatus.RINGING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    signaling_info: Optional[dict[str, Any]] = None


# ---------------------- Anonymous Call Session -------------- #

class AnonymousCallSession(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_a_id: UUID
    user_b_id: Optional[UUID] = None
    status: CallStatus = CallStatus.RINGING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None


# ---------------------- WebRTC Signaling -------------------- #

class SignalingMessage(DbBaseModel):
    from_user_id: UUID
    to_user_id: UUID
    call_id: Optional[UUID] = None
    type: SignalingMessageType
    data: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None




class Message(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    sender_user_id: UUID
    receiver_user_id: UUID
    text: str
    read: bool = False
    read_at: Optional[datetime] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------- Conversation ------------------------ #

class Conversation(DbBaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_ids: List[UUID]
    last_message_at: Optional[datetime]
    type: ConversationType = ConversationType.ONE_ON_ONE


# ---------------------- Matchmaking Queue ------------------- #

class MatchmakingEntry(DbBaseModel):
    user_id: UUID
    status: MatchmakingStatus = MatchmakingStatus.WAITING
    matched_with: Optional[UUID] = None
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
