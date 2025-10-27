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
            "format": "best",
            "cookiefile": "cookies.txt"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
        return {
            "success": True,
            "file": filename,
            "title": info.get("title")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
