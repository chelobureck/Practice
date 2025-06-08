from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.chat_history import get_history, add_message, clear_history
from services.gpt_service import get_gpt_plan
from services.pptx_service import make_pptx_file, pptx_to_png
from services.file_service import save_last_pptx_path, get_last_pptx_path, clear_last_pptx_path
import os
import uuid
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_index():
    return FileResponse("static/index.html", media_type="text/html")

@app.get("/style.css")
def read_css():
    return FileResponse("static/style.css", media_type="text/css")

@app.get("/main.js")
def read_js():
    return FileResponse("static/main.js", media_type="application/javascript")

@app.post("/gpt")
async def gpt_pptx(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    history = data.get("history", [])
    if not history:
        return JSONResponse({"error": "No chat history provided"}, status_code=400)

    # Получаем план презентации от GPT
    plan = get_gpt_plan(history)

    # Генерируем pptx и png
    filename = f"presentation_{uuid.uuid4().hex}.pptx"
    pptx_path = make_pptx_file(plan, filename)
    save_last_pptx_path(pptx_path)
    png_dir = f"png_{uuid.uuid4().hex}"
    os.makedirs(png_dir, exist_ok=True)
    png_files = pptx_to_png(pptx_path, png_dir)
    images = []
    for png_file in png_files:
        with open(png_file, "rb") as f:
            images.append("data:image/png;base64," + base64.b64encode(f.read()).decode())
    def cleanup():
        try:
            for f in png_files:
                os.remove(f)
            os.rmdir(png_dir)
        except Exception:
            pass
    background_tasks.add_task(cleanup)
    return JSONResponse({"images": images})

@app.get("/download_last_pptx")
def download_last_pptx():
    pptx_path = get_last_pptx_path()
    if pptx_path and os.path.exists(pptx_path):
        clear_last_pptx_path()
        response = FileResponse(
            path=pptx_path,
            filename="presentation.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        def cleanup():
            try:
                os.remove(pptx_path)
            except Exception:
                pass
        import threading
        threading.Thread(target=cleanup).start()
        return response
    return JSONResponse({"error": "Файл не найден"}, status_code=404)
