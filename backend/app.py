from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.grade import router
import os


app = FastAPI()

# Path to frontend folder (one level above backend)
frontend_path = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "frontend")

# Mount frontend folder as /frontend
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Root route serves index.html


@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

"""
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # dynamic port for Render
    uvicorn.run(app, host="0.0.0.0", port=port)
"""
