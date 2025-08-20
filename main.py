from fastapi import FastAPI
import uvicorn
from cruxgen.database.db_config import test_db_connection
# import routers
from cruxgen.document_managment.document_router import router as document_router
from cruxgen.document_managment.minio_config import client as minio_client
from cruxgen.configuration.vault_config import test_vault_connection

app = FastAPI()

# Include routers
app.include_router(document_router, prefix="/document", tags=["Document Management"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health_check():

    # Test Vault connection
    vault_status = test_vault_connection()
    if not vault_status:
        return {"status": "error", "message": "Vault connection failed"}

    database_status = test_db_connection()
    if not database_status:
        return {"status": "error", "message": "Database connection failed"}
    
    # You can add more health checks here, e.g., for MinIO
    try:
        minio_client.list_buckets()  # This will raise an error if the connection fails
    except Exception as e:
        return {"status": "error", "message": f"MinIO connection failed: {str(e)}"}
    
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, 
                host="0.0.0.0", 
                port=8000,
                # log_level="warning"
                )