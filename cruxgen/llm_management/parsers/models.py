from pydantic import BaseModel, Field
from typing import List

class QAPair(BaseModel):
   question: str
   answer: str

class ResponseModel(BaseModel):
    qa_pairs: List[QAPair]

class LLMRequest(BaseModel):
    system_prompt: str = Field(..., description="The system prompt for the LLM")
    prompt: str = Field(..., description="The prompt to send to the LLM")
    model: str = Field(default="bedrock/us.meta.llama3-3-70b-instruct-v1:0", description="The model to use for the LLM")