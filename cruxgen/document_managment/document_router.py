from fastapi import APIRouter, status
from cruxgen.document_managment.minio_operations import (
    create_bucket,
    upload_file,
    list_objects,
    get_object_info,
    delete_object,
    delete_bucket,
    list_buckets
)
from cruxgen.pydantic_models.generic_output_model import APIOutputResponse
from cruxgen.pydantic_models.minio_models import (
    MinioBucket,
    MinioUploadFile,
    MinioListObjects,
    MinioObjectInfo,
    MinioDeleteObject,
    MinioDeleteBucket,
    MinioListBuckets
)
from typing import Optional

from cruxgen.database.crud_functions import (
    create_file,
    get_file_id_by_name,
    delete_file,
    Session
)

router = APIRouter()

with Session() as session:
    # Create a new session for database operations
    db = session
# db = get_database()

@router.post("/create-bucket", 
    response_model=APIOutputResponse,
    summary="Create a new bucket in MinIO",
    description="This endpoint allows you to create a new bucket in the MinIO storage system. " \
    "You need to provide the bucket name in the request body."
)
async def create_bucket_endpoint(params: MinioBucket):
    try:
        output = create_bucket(params)

        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})

        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')

        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_201_CREATED if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error creating bucket: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

@router.post("/upload-file", 
    response_model=APIOutputResponse,
    summary="Upload a file to a MinIO bucket",
    description="This endpoint allows you to upload a file to a specified bucket in MinIO. " \
    "You need to provide the bucket name, object name, and file path in the request body."
)
async def upload_file_endpoint(params: MinioUploadFile):

    try:
        # Check if the file already exists in the database
        existing_file = get_file_id_by_name(db, file_name=params.object_name)
        if existing_file:
            return APIOutputResponse(
                success=False,
                message="File already exists in the database.",
                status_code=status.HTTP_400_BAD_REQUEST,
                response=None
            )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error checking file existence: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )
    
    try:
        # add file to database
        create_file(db, file_name=params.object_name, dataset_generated=False)
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error creating file in database: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

    try:
        output = upload_file(params)

        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})

        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')

        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_201_CREATED if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error uploading file: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

@router.delete("/delete-object",
    response_model=APIOutputResponse,
    summary="Delete an object from a MinIO bucket",
    description="This endpoint allows you to delete an object from a specified bucket in MinIO. " \
    "You need to provide the bucket name and object name in the request body."
)
async def delete_object_endpoint(params: MinioDeleteObject):
    
    try:
        # Delete the file from the database
        # get file_id from database
        file_id = get_file_id_by_name(db, file_name=params.object_name)
        if not file_id:
            return APIOutputResponse(
                success=False,
                message="File ID not found in the database.",
                status_code=status.HTTP_404_NOT_FOUND,
                response=None
            )
        delete_file(db, file_id=file_id.file_id)
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error deleting file from database: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

    try:
        output = delete_object(params)
        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error deleting object: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )
    
@router.delete("/delete-bucket",
    response_model=APIOutputResponse,
    summary="Delete a MinIO bucket",
    description="This endpoint allows you to delete a specified bucket in MinIO. " \
    "You need to provide the bucket name in the request body."
)
async def delete_bucket_endpoint(params: MinioDeleteBucket):
    try:
        output = delete_bucket(params)
        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error deleting bucket: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

@router.get("/list-objects",
    response_model=APIOutputResponse,
    summary="List objects in a MinIO bucket",
    description="This endpoint allows you to list all objects in a specified bucket in MinIO. " \
    "You need to provide the bucket name in the request body."
)
async def list_objects_endpoint(bucket_name: Optional[str] = None,
                                prefix: Optional[str] = None, 
                                recursive: bool = False
):
    try:
        params = MinioListObjects(bucket_name=bucket_name, 
                                prefix=prefix, 
                                recursive=recursive
                                )
        output = list_objects(params)

        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error listing objects: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

@router.post("/list-buckets",
    response_model=APIOutputResponse,
    summary="List all MinIO buckets",
    description="This endpoint allows you to list all buckets in the MinIO storage system."
)
async def list_buckets_endpoint():
    try:
        params = MinioListBuckets()
        output = list_buckets(params)
        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error listing buckets: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )

@router.get("/get-object-info",
    response_model=APIOutputResponse,
    summary="Get information about a MinIO object",
    description="This endpoint allows you to retrieve information about a specific object in a MinIO bucket. " \
    "You need to provide the bucket name and object name in the request body."
)
async def get_object_info_endpoint(bucket_name: str, object_name: str):
    try:
        params = MinioObjectInfo(bucket_name=bucket_name, object_name=object_name)
        output = get_object_info(params)
        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error getting object info: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )