# app/repositories/video/video_interact_repository.py

from app.repositories.video.video_repository import VideoRepository

class VideoInteractRepository:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    # Your like / comment interaction logic here.
