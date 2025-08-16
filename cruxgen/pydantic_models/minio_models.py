from pydantic import BaseModel, Field
from typing import Optional

class MinioBucket(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")

class MinioUploadFile(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")
    object_name: str = Field(..., description="Name of the object in the Minio bucket")
    file_path: str = Field(..., description="Path to the file to be uploaded")

class MinioListObjects(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")
    prefix: Optional[str] = Field(None, description="Prefix to filter objects by")
    recursive: bool = Field(False, description="Whether to list objects recursively")

class MinioDownloadFile(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")
    object_name: str = Field(..., description="Name of the object to be downloaded")
    file_path: Optional[str] = Field(..., description="Path where the file will be saved")

class MinioObjectInfo(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")
    object_name: str = Field(..., description="Name of the object in the Minio bucket")

class MinioDeleteObject(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket")
    object_name: str = Field(..., description="Name of the object to be deleted")

class MinioDeleteBucket(BaseModel):
    bucket_name: str = Field(..., description="Name of the Minio bucket to be deleted")

class MinioListBuckets(BaseModel):
    pass