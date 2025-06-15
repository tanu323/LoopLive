from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.services.user.user_auth import UserAuthService
from app.schemas import UserData
from app.api.deps import get_user_auth_service 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# It fetches the authenticated user's credentials from the UserAuth model
async def get_logged_in_user(
    token: str = Depends(oauth2_scheme),
    auth_service: UserAuthService = Depends(get_user_auth_service),
) -> UserData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = await auth_service.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserData(user_id=user.user_id, email=user.email, username=user.username)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token verification failed"
        )
