from fastapi import APIRouter, status
from cruxgen.document_managment.minio_operations import (
    create_bucket
)
from cruxgen.pydantic_models.generic_output_model import APIOutputResponse
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

router = APIRouter()

@router.post("/create-bucket", 
    response_model=APIOutputResponse,
    summary="Create a new bucket in MinIO",
    description="This endpoint allows you to create a new bucket in the MinIO storage system. " \
    "You need to provide the bucket name in the request body."
)
async def create_bucket_endpoint(params: MinioBucket):
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