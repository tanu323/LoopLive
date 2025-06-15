# app/repositories/video/video_explore_repository.py

from app.repositories.video.video_repository import VideoRepository

class VideoExploreRepository:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    # Your search / featured / views logic here.
