from fastapi.middleware.cors import CORSMiddleware
from apps.main import app
import uvicorn as uv

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uv.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        reload=True
        )
