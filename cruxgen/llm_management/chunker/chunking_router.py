from fastapi import APIRouter, status
from cruxgen.pydantic_models.generic_output_model import APIOutputResponse
from cruxgen.llm_management.chunker.document_chunker import DocumentSplitter, ChunkerConfig
from cruxgen.database.crud_functions import delete_chunks_by_file_id, Session, get_chunks_by_file_id
from pydantic import BaseModel, Field

router = APIRouter()

with Session() as session:
    # Create a new session for database operations
    db = session

class CreateChunks(BaseModel):
    file_id: str = Field(description="The file id of the document you want to create chunks.")
    bucket_name: str = Field(description="Name of the bucket where the file is stored.")

@router.post("/create-chunks", 
    response_model=APIOutputResponse,
    summary="Create a new chunks for file",
    description="This endpoint allows you to create a new chunks for the given file id" \
)
async def create_chunks_endpoint(params: CreateChunks):
    try:
        splitter = DocumentSplitter(ChunkerConfig())

        output = splitter.load_and_club(
            file_id = params.file_id,
            bucket_name = params.bucket_name
        )

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

class DeleteChunk(BaseModel):
    file_id: str = Field(description="File Id to delete chunks for")

@router.delete("/delete-chunks", 
    response_model=APIOutputResponse,
    summary="Delete chunks for file",
    description="This endpoint allows you to delete chunks for the given file id" 
)
async def delete_chunks_endpoint(params: DeleteChunk):
    try:
        file_id = params.file_id

        no_of_deleted_chucks = delete_chunks_by_file_id(db, file_id)

        output = {
            "result": no_of_deleted_chucks,
            "success": True,
            "message": "Chunks deleted successfully",
            "output": f"{no_of_deleted_chucks} chunks deleted"
        }

        # Extract the 'result' dictionary from the output
        result_data = output.get('result', {})
        # Use the values directly from the dictionary to build the APIOutputResponse
        success_status = output.get('success', False)
        response_message = output.get('message', 'No message provided')
        response_payload = output.get('output')
        return APIOutputResponse(
            success=success_status,
            message=response_message,
            status_code=status.HTTP_200_OK if success_status else status.HTTP_400_BAD_REQUEST,
            response=response_payload
        )   
    except Exception as e:
        return APIOutputResponse(
            success=False,
            message=f"Error deleting chunks: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        ) 
    
@router.get("/get-chunks", 
    response_model=APIOutputResponse,
    summary="Get chunks for file",
    description="This endpoint allows you to list all the chunks for the given file id" 
)
async def get_chunks_endpoint(file_id: str):
    try:

        chunks = get_chunks_by_file_id(db, file_id)

        output = {
            "result": {},
            "success": True,
            "message": "Retreived chunks successfully",
            "output": [chunk.chunk_text for chunk in chunks]
        }

        # Extract the 'result' dictionary from the output
        result_data = output
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
            message=f"Error getting chunks: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=None
        ) 
