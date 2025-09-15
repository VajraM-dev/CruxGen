from cruxgen.configuration.settings import Config
from cruxgen.llm_management.llm_config.config import get_llm_response
from cruxgen.database.crud_functions import create_qa_pair, get_chunks_by_file_id, Session, get_chunk_by_id, delete_qa_pairs_by_file_id, qa_pairs_exist_for_file, get_qa_pairs_by_file_id, update_dataset_generated
from cruxgen.llm_management.parsers.models import LLMRequest
from cruxgen.llm_management.prompts.prompt_loader import load_and_format_prompt
from tenacity import retry, stop_after_attempt, wait_exponential
from cruxgen.pydantic_models.generic_output_model import OutputResponse
from cruxgen.configuration.logging_config import monitor
from typing import Optional

config = Config()

with Session() as session:
    # Create a new session for database operations
    db = session

def get_all_chunk_text(file_id: str):
   chunk_list = get_chunks_by_file_id(db, file_id)
   
   for chunk in chunk_list:
       yield chunk

system_prompt = load_and_format_prompt(
   config.SYSTEM_PROMPT_PATH,
)

def add_qa_pairs_for_each_chunk(chunk_id, result):
    for qa_pair in result:
        create_qa_pair(
            db,
            chunk_id=chunk_id,
            question=qa_pair.question,
            answer=qa_pair.answer
        )

@retry(
   stop=stop_after_attempt(3),
   wait=wait_exponential(multiplier=1, min=4, max=10),
)
def process_chunk(chunk):
    user_prompt = load_and_format_prompt(
        config.USER_PROMPT_PATH,
        chunk_content=chunk.chunk_text
    )

    llm_request_input = LLMRequest(
        system_prompt=system_prompt,
        prompt=user_prompt
    )

    result = get_llm_response(llm_request_input)

    if result.success is True:
        add_qa_pairs_for_each_chunk(
            chunk_id=chunk.chunk_id,
            result=result.response.qa_pairs
        )

    return result

# @monitor
# def process_all_chunks(file_id: str):
#     try:
#         _ = [process_chunk(chunk_text) for chunk_text in get_all_chunk_text(file_id)]

#         return OutputResponse(success=True, message=f"All chunks for file_id: {file_id} are processed")
#     except Exception as e:
#         return OutputResponse(success=False, message=f"Error creating QA pairs for file_id: {file_id}: {e}")

@monitor
def process_chunks(file_id: str, chunk_id: Optional[str] = None):
   try:
       if chunk_id:
            # Process single chunk
            chunk = get_chunk_by_id(db, chunk_id)
            if not chunk or chunk.file_id != file_id:
                return OutputResponse(success=False, message=f"Chunk {chunk_id} not found for file {file_id}")
            
            _ = process_chunk(chunk)
            update_dataset_generated(db, file_id, True)
            message = f"Chunk {chunk_id} processed"
       else:
            # Process all chunks
            _ = [process_chunk(chunk) for chunk in get_all_chunk_text(file_id)]
            message = f"All chunks for file_id: {file_id} processed"
            update_dataset_generated(db, file_id, True)
       return OutputResponse(success=True, message=message)
   except Exception as e:
       return OutputResponse(success=False, message=f"Error processing chunks: {e}")

@monitor
def delete_qa_pairs_for_file(file_id: str):
    try:
        deleted_count = delete_qa_pairs_by_file_id(db, file_id)
        return OutputResponse(success=True, message=f"Deleted {deleted_count} QA pairs for file_id: {file_id}")
    except Exception as e:
        return OutputResponse(success=False, message=f"Error deleting QA pairs for file_id: {file_id}: {e}")

@monitor
def get_all_qa_pairs(file_id: str):
    try:
        if not qa_pairs_exist_for_file(db, file_id):
            return OutputResponse(success=False, message=f"No QA pairs found for file_id: {file_id}")

        qa_pairs = get_qa_pairs_by_file_id(db, file_id)
        return OutputResponse(success=True, message=f"Retrieved {len(qa_pairs)} QA pairs for file_id: {file_id}", output=qa_pairs)
    except Exception as e:
        return OutputResponse(success=False, message=f"Error retrieving QA pairs for file_id: {file_id}: {e}")