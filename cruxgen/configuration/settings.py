from cruxgen.configuration.vault_config import read_secret_result

class Config:
    def __init__(self):
        self.environment = read_secret_result['data']['data']['environment']
        self.MINIO_ENDPOINT = read_secret_result['data']['data']['MINIO_URL']
        self.MINIO_ACCESS_KEY = read_secret_result['data']['data']['MINIO_ACCESS_KEY']
        self.MINIO_SECRET_KEY = read_secret_result['data']['data']['MINIO_SECRET_KEY']
        self.MINIO_SECURE = read_secret_result['data']['data']['MINIO_SECURE']

        self.POSTGRESQL_HOST = read_secret_result['data']['data']['PORTGRES_HOST']
        self.POSTGRESQL_PORT = read_secret_result['data']['data']['POSTGRES_PORT']
        self.POSTGRESQL_USER = read_secret_result['data']['data']['POSTGRES_USERNAME']
        self.POSTGRESQL_PASSWORD = read_secret_result['data']['data']['POSTGRES_PASSWORD']
        self.POSTGRESQL_DB = read_secret_result['data']['data']['POSTGRES_DATABASE']

        self.LITELLM_URL = read_secret_result['data']['data']['LITELLM_BASE_URL']
        self.LITELLM_API_KEY = read_secret_result['data']['data']['LITELLM_API_KEY']

        self.SYSTEM_PROMPT_PATH = "cruxgen/llm_management/prompts/qa_system.md"
        self.USER_PROMPT_PATH = "cruxgen/llm_management/prompts/qa_user.md"