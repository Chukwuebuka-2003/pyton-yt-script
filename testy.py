from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import uuid
import uvicorn
from typing import Optional

app = FastAPI(title="YouTube Downloader API")

# Create a downloads directory if it doesn't exist
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: HttpUrl
    output_path: Optional[str] = DOWNLOAD_DIR

class DownloadResponse(BaseModel):
    title: str
    filename: str
    download_path: str
    resolution: str

@app.get("/")
def read_root():
    return {"message": "YouTube Downloader API. Use /download/ endpoint with a YouTube URL"}

@app.post("/download/", response_model=DownloadResponse)
def download_video(request: DownloadRequest):
    try:
        # Create a YouTube object
        yt = YouTube(str(request.url), on_progress_callback=on_progress)
        
        # Get the highest resolution stream
        ys = yt.streams.get_highest_resolution()
        
        # Create a unique filename to prevent overwriting
        filename = f"{uuid.uuid4().hex}_{yt.title.replace(' ', '_')}.mp4"
        download_path = os.path.join(request.output_path, filename)
        
        # Download the video
        ys.download(output_path=request.output_path, filename=filename)
        
        return DownloadResponse(
            title=yt.title,
            filename=filename,
            download_path=download_path,
            resolution=f"{ys.resolution}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.get("/download/file")
def download_file(url: str = Query(...), output_path: Optional[str] = DOWNLOAD_DIR):
    """
    Endpoint to directly download a file from a YouTube URL
    """
    try:
        # Create a YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Get the highest resolution stream
        ys = yt.streams.get_highest_resolution()
        
        # Create a unique filename
        filename = f"{uuid.uuid4().hex}_{yt.title.replace(' ', '_')}.mp4"
        download_path = os.path.join(output_path, filename)
        
        # Download the video
        ys.download(output_path=output_path, filename=filename)
        
        # Return the file for direct download
        return FileResponse(
            path=download_path,
            filename=f"{yt.title}.mp4",
            media_type="video/mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("testy:app", host="0.0.0.0", port=8000, reload=True)
