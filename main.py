from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class DownloadRequest(BaseModel):
    youtube_url: str

@app.post("/download")
async def download_video(req: DownloadRequest):
    try:
        url = req.youtube_url
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "cookiefile": "cookies.txt",
            "noplaylist": True,
            "quiet": True,
            "nocheckcertificate": True,
            "concurrent_fragment_downloads": 1,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "success": True,
            "title": info.get("title"),
            "url": info.get("url"),
            "duration": info.get("duration"),
            "info": info     # Extra details
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
