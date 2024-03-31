from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/download-exe")
async def download_exe():
    exe_file_path = os.path.join(os.path.dirname(__file__), "dist", "main.exe")
    if not os.path.exists(exe_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(exe_file_path, media_type="application/octet-stream", filename="main.exe")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
