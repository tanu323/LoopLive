# enums.py
from enum import Enum


class PrivacySetting(str, Enum):
    PUBLIC = "public"
    FOLLOWERS_ONLY = "followers"
    PRIVATE = "private"


class CallStatus(str, Enum):
    RINGING = "ringing"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    ENDED = "ended"


class SignalingMessageType(str, Enum):
    OFFER = "offer"
    ANSWER = "answer"
    CANDIDATE = "candidate"
    BYE = "bye"


class MatchmakingStatus(str, Enum):
    WAITING = "waiting"
    MATCHED = "matched"
    DISCONNECTED = "disconnected"


class VideoStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"


class ConversationType(str, Enum):
    ONE_ON_ONE = "one_on_one"
    GROUP = "group"
