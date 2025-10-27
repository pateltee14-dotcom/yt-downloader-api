from fastapi import FastAPI, Request
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YouTube Downloader API Ready!"}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("youtube_url")
    ydl_opts = {"format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return {
        "success": True,
        "file": filename,
        "title": info.get("title"),
        "duration": info.get("duration")
    }

# For running on Replit
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
