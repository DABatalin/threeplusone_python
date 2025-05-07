from typing import BinaryIO
import os
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException, UploadFile

from app.core.config import settings


class S3Service:
    def __init__(self):
        self.client = Minio(
            f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_USE_SSL
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the configured bucket exists, create if it doesn't"""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize S3: {str(e)}")

    async def upload_file(self, file: UploadFile, object_name: str, content_type: str) -> str:
        """Upload a file to S3 and return its URL"""
        try:
            # Читаем содержимое файла в память
            contents = await file.read()
            file_size = len(contents)
            
            # Создаем BytesIO объект из содержимого
            file_data = BytesIO(contents)
            
            # Загружаем файл
            self.client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=file_data,
                length=file_size,
                content_type=content_type
            )
            
            # Возвращаем URL загруженного файла
            return f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}/{settings.MINIO_BUCKET_NAME}/{object_name}"
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
        finally:
            # Возвращаем указатель файла в начало для возможного повторного использования
            await file.seek(0)

    def delete_file(self, object_name: str):
        """Delete a file from S3"""
        try:
            self.client.remove_object(settings.MINIO_BUCKET_NAME, object_name)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")


s3_service = S3Service() 