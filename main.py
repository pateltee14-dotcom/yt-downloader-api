from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Request ka model
class DownloadRequest(BaseModel):
    youtube_url: str

@app.get("/")
def home():
    return {"message": "YouTube Downloader API Ready!"}

# Main download endpoint
@app.post("/download")
async def download_video(req: DownloadRequest):
    try:
        url = req.youtube_url
        ydl_opts = {
            "format": "best",
            "cookiefile": "cookies.txt"   # yahi name/upload hai to work karega
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
