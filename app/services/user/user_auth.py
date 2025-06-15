from uuid import uuid4, UUID
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional, Tuple, Dict
from app.models.user_models import UserAuth, UserAuthCreate
from app.repositories.user import UserAuthRepository
from app.core.exceptions import AuthException
from app.schemas.user_schema import UserRegisterRequest
from app.core.security import verify_password, create_access_token, create_refresh_token, jwt
from app.core.config import settings
from app.core.logging import get_logger
from app.services.base import BaseService

logger = get_logger()

class UserAuthService(BaseService):
    def __init__(self, auth_repo: UserAuthRepository):
        super().__init__(auth_repo)
        self.auth_repo = auth_repo  
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        try:
            hashed = self.pwd_context.hash(password)
            logger.debug("[Hash Password] Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"[Hash Password] Failed to hash password: {e}")
            raise AuthException("Internal error during password hashing")

    def verify_password(self, plain: str, hashed: str) -> bool:
        try:
            result = self.pwd_context.verify(plain, hashed)
            logger.debug(f"[Verify Password] Password verification result: {result}")
            return result
        except Exception as e:
            logger.error(f"[Verify Password] Error comparing password hash: {e}")
            return False

    async def register_user(self, user_data: UserRegisterRequest) -> UserAuth:
        try:
            user = UserAuth(
                id=uuid4(),
                email=user_data.email,
                username=user_data.username,
                hashed_password=self.hash_password(user_data.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            registered_user = await self.auth_repo.register_user(user)
            logger.info(f"[Register User] Successfully registered user: {user.email}")
            return registered_user
        except Exception as e:
            logger.error(f"[Register User] Failed to register user {user_data.email}: {e}")
            raise AuthException("Failed to register user")

    async def authenticate(self, email: str, password: str):
        try:
            user = await self.auth_repo.get_by_email(email)
            if user and self.verify_password(password, user.hashed_password):
                logger.info(f"[Authenticate] Authenticated user: {email}")
                return user
            logger.warning(f"[Authenticate] Authentication failed for user: {email}")
            return None
        except Exception as e:
            logger.error(f"[Authenticate] Error during authentication for {email}: {e}")
            raise AuthException("Authentication failed")

    async def get_by_email(self, email: str):
        try:
            user = await self.get_by_field("email", email)
            if user:
                logger.info(f"[Get By Email] Found user with email: {email}")
            else:
                logger.warning(f"[Get By Email] No user found with email: {email}")
            return user
        except Exception as e:
            logger.error(f"[Get By Email] Failed to retrieve user {email}: {e}")
            raise AuthException("User lookup failed")

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            result = await self.delete_by_user_id(user_id)
            if result:
                logger.info(f"[Delete User] Successfully deleted user_id={user_id}")
            else:
                logger.warning(f"[Delete User] User not found for deletion: user_id={user_id}")
            return result
        except Exception as e:
            logger.error(f"[Delete User] Failed to delete user_id={user_id}: {e}")
            raise AuthException("Failed to delete user")

    async def generate_token(self, user_id: UUID, email: str) -> Tuple[str, str]:
        try:
            data = {"sub": str(user_id), "email": email}
            access_token = create_access_token(data)
            refresh_token = create_refresh_token(data)
            logger.info(f"[Generate Token] Tokens generated for user_id={user_id}")
            return access_token, refresh_token
        except Exception as e:
            logger.error(f"[Generate Token] Failed to generate tokens for user_id={user_id}: {e}")
            raise AuthException("Token generation failed")

    async def verify_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

            # Validate token type
            token_type = payload.get("type")
            if token_type not in ["access", "refresh"]:
                raise ValueError("Invalid token type")

            # Validate expiration
            exp = payload.get("exp")
            if exp is None:
                raise ValueError("Token missing expiration")

            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise ValueError("Token has expired")

            logger.debug("[Verify Token] Token verified successfully")
            return payload

        except (jwt.JWTError, ValueError) as e:
            logger.error(f"[Verify Token] Token verification failed: {e}")
            return None
