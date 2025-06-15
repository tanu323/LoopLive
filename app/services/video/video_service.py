from app.repositories.video.video_repository_wrapper import VideoRepositoryWrapper
from app.services.s3 import S3Service
from app.services.video.video_create_service import VideoCreateService
from app.services.video.video_manage_service import VideoManageService
from app.services.video.video_explore_service import VideoExploreService
from app.services.video.video_interact_service import VideoInteractService
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Tuple, Dict
from app.core.logging import get_logger
from app.services.base import BaseService
import logging


logger = get_logger() 

class VideoService(BaseService):
    def __init__(self, video_repo: VideoRepositoryWrapper,  s3_service: S3Service):
        super().__init__(video_repo)
        self.video_repo = video_repo
        self.create_service = VideoCreateService(video_repo.create_repo, s3_service)
        self.manage_service = VideoManageService(video_repo.manage_repo)
        self.explore_service = VideoExploreService(video_repo.explore_repo)
        self.interact_service = VideoInteractService(video_repo.interact_repo)



        