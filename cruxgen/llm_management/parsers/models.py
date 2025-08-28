from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    answer: str

class LLMRequest(BaseModel):
    system_prompt: str = Field(..., description="The system prompt for the LLM")
    prompt: str = Field(..., description="The prompt to send to the LLM")
    model: str = Field(default="bedrock/us.meta.llama3-3-70b-instruct-v1:0", description="The model to use for the LLM")