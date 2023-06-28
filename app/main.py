import uvicorn
from fastapi import FastAPI
from app.core.config import Settings
from app.routers.endpoints import data_endpoints

app = FastAPI(title=Settings.PROJECT_NAME)

app.include_router(data_endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)