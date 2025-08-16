from fastapi import FastAPI
import uvicorn

# import routers
from cruxgen.document_managment.document_router import router as document_router

app = FastAPI()

# Include routers
app.include_router(document_router, prefix="/document", tags=["Document Management"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)