from enum import Enum

class CollectionName(str, Enum):
    USER_AUTH = "user_auth"
    USER_PROFILES = "user_profiles"
    VIDEOS = "videos"
    COMMENTS = "comments"
    LIKES = "likes"
    FOLLOWS = "follows"
    TAGS = "tags"
    MESSAGES = "messages"
    CONVERSATIONS = "conversations"

    @classmethod
    def get_all(cls):
        return [v.value for v in cls.__members__.values()]

    @classmethod
    def get_by_model_name(cls, model_name: str) -> str:
        name = model_name.lower()
        match name:
            case "userauth":
                return cls.USER_AUTH.value
            case "userprofile":
                return cls.USER_PROFILES.value
            case "video":
                return cls.VIDEOS.value
            case "comment":
                return cls.COMMENTS.value
            case "like":
                return cls.LIKES.value
            case "follow":
                return cls.FOLLOWS.value
            case "tag":
                return cls.TAGS.value
            case "message":
                return cls.MESSAGES.value
            case "conversation":
                return cls.CONVERSATIONS.value
            case _:
                raise ValueError(f"Unknown model name: {model_name}")
