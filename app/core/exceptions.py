import logging
import sys
from typing import Optional, Union, Dict, Any
from starlette import status

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class AppException(Exception):
    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        error_code: int = 500,
        details: Optional[Union[str, Dict[str, Any]]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details
        self.log_error()

    def log_error(self) -> None:
        log_message = f"AppException: {self.message} (Code: {self.error_code})"
        if self.details:
            log_message += f" Details: {self.details}"
        logger.error(log_message)

    def to_dict(self) -> Dict[str, Any]:
        error_dict = {
            "message": self.message,
            "error_code": self.error_code,
        }
        if self.details:
            error_dict["details"] = self.details
        return error_dict


# Child Exceptions
class UserNotFoundException(AppException):
    def __init__(self, user_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"User with ID {user_id} not found."
        )

class UserAlreadyExistsException(AppException):
    def __init__(self, username: str):
        super().__init__(
            error_code=status.HTTP_409_CONFLICT,
            error_message=f"User with username '{username}' already exists."
        )

class InvalidUserCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_401_UNAUTHORIZED,
            error_message="Invalid username or password."
        )

class UserCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create user."
        )

class AuthException(AppException):
    def __init__(self, detail: str = "Authentication failed."):
        super().__init__(
            message=detail,
            error_code=status.HTTP_401_UNAUTHORIZED,
            details="Authentication error occurred."
        )


class VideoNotFoundException(AppException):
    def __init__(self, video_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Video with ID {video_id} not found."
        )


class VideoCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create the video."
        )


class VideoFetchException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to fetch videos."
        )


class VideoDeletionException(AppException):
    def __init__(self, video_id: str):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message=f"Failed to delete video with ID {video_id}."
        )



class CommentNotFoundException(AppException):
    def __init__(self, comment_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Comment with ID {comment_id} not found."
        )

class CommentCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create comment."
        )

class CommentDeletionException(AppException):
    def __init__(self, comment_id: str):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message=f"Failed to delete comment with ID {comment_id}."
        )


class LikeNotFoundException(AppException):
    def __init__(self, user_id: str, video_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Like by user {user_id} on video {video_id} not found."
        )

class LikeAlreadyExistsException(AppException):
    def __init__(self, user_id: str, video_id: str):
        super().__init__(
            error_code=status.HTTP_409_CONFLICT,
            error_message=f"User {user_id} has already liked video {video_id}."
        )

class LikeCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create like."
        )


class TagNotFoundException(AppException):
    def __init__(self, tag_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Tag with ID {tag_id} not found."
        )

class TagAlreadyExistsException(AppException):
    def __init__(self, tag_name: str):
        super().__init__(
            error_code=status.HTTP_409_CONFLICT,
            error_message=f"Tag '{tag_name}' already exists."
        )

class TagCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create tag."
        )


class FollowNotFoundException(AppException):
    def __init__(self, follower_id, followed_id):
        super().__init__(
            message=f"Follow relationship not found between user {follower_id} and {followed_id}",
            error_code=404,
            details=f"The follow relationship between '{follower_id}' and '{followed_id}' does not exist."
        )


class MessageNotFoundException(AppException):
    def __init__(self, message_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Message with ID {message_id} not found."
        )

class MessageCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to send message."
        )

class MessageDeletionException(AppException):
    def __init__(self, message_id: str):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message=f"Failed to delete message with ID {message_id}."
        )

class ConversationNotFoundException(AppException):
    def __init__(self, conversation_id: str):
        super().__init__(
            error_code=status.HTTP_404_NOT_FOUND,
            error_message=f"Conversation with ID {conversation_id} not found."
        )

class ConversationCreationException(AppException):
    def __init__(self):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Failed to create conversation."
        )

class ConversationAlreadyExistsException(AppException):
    def __init__(self, user_a: str, user_b: str):
        super().__init__(
            error_code=status.HTTP_409_CONFLICT,
            error_message=f"Conversation between user '{user_a}' and user '{user_b}' already exists."
        )

class ConversationDeletionException(AppException):
    def __init__(self, conversation_id: str):
        super().__init__(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message=f"Failed to delete conversation with ID {conversation_id}."
        )


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            error_code=401,
            details="Incorrect username or password."
        )


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized access"):
        super().__init__(
            message=message,
            error_code=403,
            details="You are not authorized to perform this action."
        )

class DatabaseConnectionException(AppException):
    def __init__(self):
        super().__init__(
            message="Database connection failed",
            error_code=500,
            details="Unable to connect to the database. Please check configuration and network."
        )

class RecordUpdateFailedException(AppException):
    def __init__(self, record_id: Union[str, int]):
        super().__init__(
            message=f"Failed to update record: {record_id}",
            error_code=500,
            details=f"An error occurred while updating the record with ID '{record_id}'."
        )

class FileUploadFailedException(AppException):
    def __init__(self, filename: str):
        super().__init__(
            message=f"File upload failed: {filename}",
            error_code=500,
            details=f"Could not upload file '{filename}'. Please try again later."
        )

class FileNotFoundException(AppException):
    def __init__(self, filename: str):
        super().__init__(
            message=f"File not found: {filename}",
            error_code=404,
            details=f"The file '{filename}' was not found on the server."
        )

class ResourceAlreadyExistsException(AppException):
    def __init__(self, resource_type: str, identifier: Union[str, int]):
        super().__init__(
            message=f"{resource_type} already exists: {identifier}",
            error_code=409,
            details=f"A {resource_type} with identifier '{identifier}' already exists."
        )

class ResourceCreationFailedException(AppException):
    def __init__(self, resource_type: str):
        super().__init__(
            message=f"Failed to create {resource_type}",
            error_code=500,
            details=f"An error occurred while creating the {resource_type}."
        )

class MissingFieldException(AppException):
    def __init__(self, field: str):
        super().__init__(
            message=f"Missing required field: {field}",
            error_code=400,
            details=f"The field '{field}' is required but was not provided."
        )

class InvalidFieldFormatException(AppException):
    def __init__(self, field: str, expected_format: str):
        super().__init__(
            message=f"Invalid format for field: {field}",
            error_code=400,
            details=f"The field '{field}' must follow the format: {expected_format}."
        )

class TokenExpiredException(AppException):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            error_code=401,
            details="The provided authentication token is no longer valid. Please log in again."
        )

class AccessDeniedException(AppException):
    def __init__(self):
        super().__init__(
            message="Access denied",
            error_code=403,
            details="You do not have permission to access this resource."
        )

class SessionNotFoundException(AppException):
    def __init__(self, session_id: str):
        super().__init__(
            message=f"Session not found: {session_id}",
            error_code=404,
            details=f"The session with id '{session_id}' does not exist or has expired."
        )
