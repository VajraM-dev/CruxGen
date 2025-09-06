import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from cruxgen.llm_management.parsers.models import LLMRequest, ResponseModel
from cruxgen.configuration.settings import Config
from cruxgen.pydantic_models.generic_output_model import APIOutputResponse

config = Config()

client = openai.OpenAI(
    api_key=config.LITELLM_API_KEY,
    base_url=config.LITELLM_URL 
)

@retry(
   stop=stop_after_attempt(3),
   wait=wait_exponential(multiplier=1, min=4, max=10),
)
def get_llm_response(params: LLMRequest) -> APIOutputResponse:
    try:
        response = client.chat.completions.parse(
            model=params.model,
            messages=[
                {"role": "system", "content": params.system_prompt},
                {"role": "user", "content": params.prompt}
            ],
            response_format=ResponseModel,
            temperature=0.3
        )

        parsed = response.choices[0].message.parsed
        if parsed is not None:
            return APIOutputResponse(status_code=200, response=parsed)
        else:
            return APIOutputResponse(status_code=500, response="Receive None as result")

    except Exception as e:
        return APIOutputResponse(status_code=500, response=f"Error in llm calling: {e}")