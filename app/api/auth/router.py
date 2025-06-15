from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.services.user.user_auth import UserAuthService
from app.api.deps import get_user_auth_service
from app.schemas.user_schema import UserRegisterRequest, LoginRequest, UserResponse, UserData, TokenResponse, TokenData
from app.core.logging import get_logger

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger()


@router.post("/register_user", response_model=UserResponse)
async def signup(user_data: UserRegisterRequest, auth_service: UserAuthService = Depends(get_user_auth_service)):
    try:
        existing = await auth_service.get_by_field("email", user_data.email)
        if existing:
            logger.warning(f"[Register] Email already registered: {user_data.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        user = await auth_service.register_user(user_data)
        logger.info(f"[Register] User registered with ID: {user.user_id}")
        return UserResponse(data=UserData(user_id=user.user_id, email=user.email, username=user.username))

    except Exception as e:
        logger.error(f"[Register] Registration failed for {user_data.email}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service: UserAuthService = Depends(get_user_auth_service)):
    try:
        user = await auth_service.authenticate(request.email, request.password)
        if not user:
            logger.warning(f"[Login] Failed login attempt for email: {request.email}")
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token, refresh_token = await auth_service.generate_token(user.user_id, request.email)
        logger.info(f"[Login] Login successful for user_id={user.user_id}")
        return TokenResponse(
            data=TokenData(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
        )

    except Exception as e:
        logger.error(f"[Login] Login failed for {request.email}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, auth_service: UserAuthService = Depends(get_user_auth_service)):
    try:
        success = await auth_service.delete_by_user_id(user_id)
        if not success:
            logger.warning(f"[Delete] User not found for user_id={user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"[Delete] User successfully deleted: user_id={user_id}")
        return {"success": True}

    except Exception as e:
        logger.error(f"[Delete] Failed to delete user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")
