# app/repositories/video/video_manage_repository.py

from app.repositories.video.video_repository import VideoRepository

class VideoManageRepository:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    # Your edit / delete / privacy / feature logic here.
