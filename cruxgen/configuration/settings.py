from cruxgen.configuration.vault_config import read_secret_result

class Config:
    def __init__(self):
        self.environment = read_secret_result['data']['data']['environment']
        self.MINIO_ENDPOINT = read_secret_result['data']['data']['MINIO_URL']
        self.MINIO_ACCESS_KEY = read_secret_result['data']['data']['MINIO_ACCESS_KEY']
        self.MINIO_SECRET_KEY = read_secret_result['data']['data']['MINIO_SECRET_KEY']
        self.MINIO_SECURE = read_secret_result['data']['data']['MINIO_SECURE']
