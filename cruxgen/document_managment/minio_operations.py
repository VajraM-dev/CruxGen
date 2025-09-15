from cruxgen.configuration.logging_config import monitor
from cruxgen.document_managment.minio_config import client
from cruxgen.pydantic_models.minio_models import (
    MinioBucket,
    MinioUploadFile,
    MinioListObjects,
    MinioDownloadFile,
    MinioObjectInfo,
    MinioDeleteObject,
    MinioDeleteBucket,
    MinioListBuckets
)
from cruxgen.pydantic_models.generic_output_model import OutputResponse

@monitor
def create_bucket(params: MinioBucket):
    try:
        if not client.bucket_exists(params.bucket_name):
            client.make_bucket(params.bucket_name)
            return OutputResponse(success=True, message=f"Bucket '{params.bucket_name}' created successfully")
        else:
            return OutputResponse(success=True, message=f"Bucket '{params.bucket_name}' already exists")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error creating bucket: {e}")
    
@monitor
def upload_file(params: MinioUploadFile):
    try:
        client.fput_object(params.bucket_name, params.object_name, params.file_path)
        return OutputResponse(success=True, message=f"File '{params.file_path}' uploaded successfully")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error uploading file: {e}")
    
@monitor
def list_objects(params: MinioListObjects):
    try:
        objects = client.list_objects(params.bucket_name, prefix=params.prefix, recursive=params.recursive)
        if not objects:
            return OutputResponse(success=True, message=f"No objects found in bucket '{params.bucket_name}'")
        return OutputResponse(
            success=True,
            message=f"Objects in bucket '{params.bucket_name}' listed successfully",
            output=[obj.object_name for obj in objects]
        )
    except Exception as e:
        return OutputResponse(success=False, message=f"Error listing objects: {e}")
    
@monitor
def download_file(params: MinioDownloadFile):
    try:
        client.fget_object(params.bucket_name, params.object_name, params.file_path)
        return OutputResponse(success=True, message=f"File '{params.object_name}' downloaded successfully")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error downloading file: {e}")    
    
@monitor
def get_object_info(params: MinioObjectInfo):
    try:
        stat = client.stat_object(params.bucket_name, params.object_name)

        stats_dict = {
            "Name": stat.object_name,
            "ETag": stat.etag,
            "Size": f"{stat.size} bytes",
            "Last Modified": stat.last_modified,
            "Content Type": stat.content_type,
            "Tags": stat.tags,
            # "Metadata": stat.metadata.__dict__
        }
        return OutputResponse(
            success=True,
            message=f"Object '{params.object_name}' info retrieved successfully",
            output=stats_dict
        )
    except Exception as e:
        return OutputResponse(success=False, message=f"Error retrieving object info: {e}")
    
@monitor
def delete_object(params: MinioDeleteObject):
    try:
        client.remove_object(params.bucket_name, params.object_name)
        return OutputResponse(success=True, message=f"Object '{params.object_name}' deleted successfully")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error deleting object: {e}")
    
@monitor
def delete_bucket(params: MinioDeleteBucket):
    try:
        client.remove_bucket(params.bucket_name)
        return OutputResponse(success=True, message=f"Bucket '{params.bucket_name}' deleted successfully")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error deleting bucket: {e}")
    
@monitor
def list_buckets(params: MinioListBuckets):
    try:
        buckets = client.list_buckets()
        return OutputResponse(
            success=True,
            message="Buckets listed successfully",
            output=[bucket.name for bucket in buckets]
        )
    except Exception as e:
        return OutputResponse(success=False, message=f"Error listing buckets: {e}")
    
@monitor
def get_object_data(params: MinioObjectInfo):
    try:
        response = client.get_object(params.bucket_name, params.object_name)
        data = response.read()
        response.close()
        response.release_conn()
        return OutputResponse(
            success=True,
            message=f"Data from object '{params.object_name}' retrieved successfully",
            output=data
        )
    except Exception as e:
        return OutputResponse(success=False, message=f"Error getting object data: {e}")