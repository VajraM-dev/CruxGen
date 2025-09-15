from cruxgen.qa_pipeline.convert_chunks_to_qa import process_chunks, delete_qa_pairs_for_file, get_all_qa_pairs
from fastapi import APIRouter, status
from cruxgen.pydantic_models.generic_output_model import APIOutputResponse
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class CreateQAFromChunks(BaseModel):
    file_id: str = Field(description="The file id of the document you want to create QA pairs from its chunks.")
    chunk_id: Optional[str] = Field(default=None, description="Optional chunk ID to process a specific chunk.")

@router.post("/process-chunks-to-qa",
    response_model=APIOutputResponse,
    summary="Process chunks to generate QA pairs",
    description="This endpoint processes all chunks associated with the given file ID to generate QA pairs."
)
async def process_chunks_endpoint(params: CreateQAFromChunks):
    try:
        output = process_chunks(file_id=params.file_id)

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
            message=f"Error creating chunks: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )
    
class DeleteQAFromChunks(BaseModel):
    file_id: str = Field(description="The file id of the document you want to delete QA pairs from its chunks.")

@router.delete("/delete-qa-pairs",
    response_model=APIOutputResponse,
    summary="Delete QA pairs for file",
    description="This endpoint allows you to delete QA pairs for the given file id"
)
async def delete_qa_pairs_endpoint(params: DeleteQAFromChunks):
    try:
        output = delete_qa_pairs_for_file(file_id=params.file_id)

        result_data = output.get('result', {})
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
            message=f"Error deleting QA pairs: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )
    
class GetQAForFile(BaseModel):
    file_id: str = Field(description="The file id of the document you want to get QA pairs for its chunks.")
    generate_jsonl: Optional[bool] = Field(default=False, description="Set to true if you want the output in JSONL format.")

from fastapi.responses import StreamingResponse
import io
import json

@router.get("/get-qa-pairs/{file_id}",
    response_model=APIOutputResponse,
    summary="Get all QA pairs for file",
    description="This endpoint retrieves all QA pairs associated with the given file id."
)
async def get_qa_pairs_endpoint(file_id: str, generate_jsonl: bool = False):
    try:
        output = get_all_qa_pairs(file_id=file_id)

        result_data = output.get('result', {})
        success_status = result_data.get('success', False)
        response_message = result_data.get('message', 'No message provided')
        response_payload = result_data.get('output')
        if response_payload and isinstance(response_payload, list) and generate_jsonl:
            jsonl_content = "\n".join([json.dumps(qa) for qa in response_payload])
            buffer = io.BytesIO(jsonl_content.encode("utf-8"))
            return StreamingResponse(
                buffer,
                media_type="application/jsonl",
                headers={
                    "Content-Disposition": f"attachment; filename=qa_pairs_{file_id}.jsonl"
                }
            )

        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error retrieving QA pairs: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        )