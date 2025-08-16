from minio import Minio
from cruxgen.configuration.settings import Config

config = Config()

# # Initialize MinIO client
client = Minio(
    config.MINIO_ENDPOINT.replace("http://", ""),
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False if config.MINIO_SECURE == "False" else True 
)