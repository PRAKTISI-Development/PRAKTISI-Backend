from fastapi.middleware.cors import CORSMiddleware
from apps.main import app
import uvicorn as uv

if __name__ == "__main__":
    uv.run(
        app, 
        host="127.0.0.1", 
        port=8888,
        reload=True
        )
