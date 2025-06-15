from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException, status
from uuid import UUID
from typing import List
from app.models.models import UserProfile, UserProfileUpdate
from app.schemas.user_schema import UserProfileSchema, ProfileResponse, UserData
from app.services.user.user_profile import UserProfileService
from app.services.s3 import S3Service
from app.api.deps import get_user_profile_service, get_s3_service
from app.api.auth.jwt import get_logged_in_user
from app.core.logging import get_logger
import mimetypes

logger = get_logger()

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile: UserProfile,
    service: UserProfileService = Depends(get_user_profile_service)
):
    try:
        new_profile = await service.create_profile(profile)
        return ProfileResponse(data=new_profile)
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create profile")

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: UserData = Depends(get_logged_in_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    try:
        profile = await service.get_profile(current_user.user_id)
        return ProfileResponse(data=profile)
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch profile")

@router.get("/{user_id}", response_model=ProfileResponse)
async def get_other_user_profile(user_id: UUID, service: UserProfileService = Depends(get_user_profile_service)):
    try:
        profile = await service.get_profile(user_id)
        return ProfileResponse(data=profile)
    except Exception as e:
        logger.error(f"Error getting profile {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

@router.patch("/{user_id}", response_model=ProfileResponse)
async def update_my_profile(
    user_id: UUID,
    updates: UserProfileUpdate,
    current_user: UserData = Depends(get_logged_in_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized update attempt")

    try:
        updated_profile = await service.update_profile(user_id, updates.model_dump(exclude_unset=True))
        return ProfileResponse(data=updated_profile)
    except Exception as e:
        logger.error(f"Error updating profile {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update profile")

@router.post("/{user_id}/upload-picture")
async def upload_profile_picture(
    user_id: UUID,
    file: UploadFile = File(...),
    current_user: UserData = Depends(get_logged_in_user),
    s3: S3Service = Depends(get_s3_service),
    service: UserProfileService = Depends(get_user_profile_service)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    # Validate image MIME type
    allowed_types = {"image/jpeg", "image/png", "image/jpg", "image/gif"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    try:
        url = await s3.upload_file(file, folder="profile_pictures")
        await service.update_profile(user_id, {"profile_picture_url": url})
        return {"profile_picture_url": url}
    
    except Exception as e:
        logger.error(f"Failed to upload profile picture: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")

@router.delete("/{user_id}/remove-picture")
async def remove_profile_picture(
    user_id: UUID,
    current_user: UserData = Depends(get_logged_in_user),
    s3: S3Service = Depends(get_s3_service),
    service: UserProfileService = Depends(get_user_profile_service)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    try:
        profile = await service.get_profile(user_id)
        if profile.profile_picture_url:
            await s3.delete_file(profile.profile_picture_url)
        await service.update_profile(user_id, {"profile_picture_url": None})
        return {"detail": "Profile picture removed"}
    
    except Exception as e:
        logger.error(f"Failed to remove profile picture for user_id {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove profile picture")

@router.get("/search")
async def search_profiles(
    q: str = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100), 
    service: UserProfileService = Depends(get_user_profile_service)):
    try:
        results = await service.search_profiles(q, skip=skip, limit=limit)
        return {"results": results}
    except Exception as e:
        logger.error(f"Search failed for query '{q}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Search failed")


# If verify_user() should only be called by an admin
@router.patch("/{user_id}/verify")
async def verify_user(
    user_id: UUID,
    current_user: UserData = Depends(get_logged_in_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    try:
        if not getattr(current_user, "is_admin", False):  # Use a default-safe check
            raise HTTPException(status_code=403, detail="Admin only")
        profile = await service.update_profile(user_id, {"is_verified": True})
        return {"verified": True}
    except Exception as e:
        logger.error(f"Failed to verify user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Verification failed")


