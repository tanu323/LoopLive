# app/repositories/video/video_repository_wrapper.py

from app.repositories.video.video_create_repository import VideoCreateRepository
from app.repositories.video.video_manage_repository import VideoManageRepository
from app.repositories.video.video_explore_repository import VideoExploreRepository
from app.repositories.video.video_interact_repository import VideoInteractRepository

class VideoRepositoryWrapper:
    def __init__(
        self,
        create_repo: VideoCreateRepository,
        manage_repo: VideoManageRepository,
        explore_repo: VideoExploreRepository,
        interact_repo: VideoInteractRepository,
    ):
        self.create_repo = create_repo
        self.manage_repo = manage_repo
        self.explore_repo = explore_repo
        self.interact_repo = interact_repo
