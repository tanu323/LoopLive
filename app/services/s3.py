import os
from uuid import uuid4
from fastapi import UploadFile
from botocore.exceptions import ClientError
import boto3
from dotenv import load_dotenv
from app.repositories.base import BaseRepository
import logging
logger = logging.getLogger(__name__)

# Load from .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
S3_BASE_URL = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"



class S3Service:
    def __init__(self):
        self.bucket_name = S3_BUCKET_NAME
        self.base_url = S3_BASE_URL
        self.s3_client = boto3.client(
            "s3",
            region_name=self.AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def _generate_key(self, folder: str, filename: str) -> str:
        file_extension = filename.split(".")[-1]
        from pathlib import Path
        return str(Path(folder) / f"{uuid4()}.{file_extension}")


    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        key = self._generate_key(folder, file.filename)

        try:
            file_content = await file.read()
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_content,
                ContentType=file.content_type,
            )
            logger.info(f"File uploaded to S3: {key}")
        except ClientError as e:
            raise Exception(f"S3 upload error: {str(e)}")

        return f"{self.base_url}/{key}"

    def delete_file(self, file_url: str):
        try:
            key = file_url.split(f"{self.base_url}/")[-1]
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"File deleted to S3: {key}")
        except ClientError as e:
            raise Exception(f"S3 deletion error: {str(e)}")

    def generate_presigned_upload_url(self, folder: str, filename: str, content_type: str, expires_in: int = 3600) -> dict:
        key = self._generate_key(folder, filename)

        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )
            logger.info(f"presigned upload url generated to S3: {key}")
            return {"url": url, "key": key}
        except ClientError as e:
            raise Exception(f"S3 presigned upload URL error: {str(e)}")

    def generate_presigned_download_url(self, key: str, expires_in: int = 3600) -> str:
        try:
            return self.s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                },
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            raise Exception(f"S3 presigned download URL error: {str(e)}")