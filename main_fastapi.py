from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.chat_history import get_history, add_message, clear_history
from services.gpt_service import get_gpt_plan, validate_plan
from services.pptx_service import make_pptx_file, pptx_to_png
from services.file_service import save_last_pptx_path, get_last_pptx_path, clear_last_pptx_path
from services.file_cleanup import cleanup_presentation_files
import os
import uuid
import base64
import logging
import shutil

logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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
    try:
        data = await request.json()
        history = data.get("history", [])
        if not history:
            return JSONResponse({"error": "No chat history provided"}, status_code=400)

        plan = get_gpt_plan(history)
        if not validate_plan(plan):
            logging.error(f"Invalid plan from GPT: {plan}")
            return JSONResponse({"error": "Invalid structure from GPT"}, status_code=400)

        pres_id = str(uuid.uuid4())
        pres_dir = f"presentations/{pres_id}"
        os.makedirs(pres_dir, exist_ok=True)
        pptx_path = os.path.join(pres_dir, "presentation.pptx")
        make_pptx_file(plan, pptx_path)
        save_last_pptx_path(pptx_path)

        png_dir = os.path.join(pres_dir, "slides")
        os.makedirs(png_dir, exist_ok=True)
        png_files = pptx_to_png(pptx_path, png_dir)
        images = []
        for png_file in png_files:
            with open(png_file, "rb") as f:
                images.append("data:image/png;base64," + base64.b64encode(f.read()).decode())
        # PNG удаляем только после ответа
        background_tasks.add_task(shutil.rmtree, pres_dir, ignore_errors=True)
        return JSONResponse({"images": images, "presentation_id": pres_id})
    except Exception as e:
        logging.error("Ошибка при создании презентации", exc_info=True)
        return JSONResponse({"error": "Failed to create presentation"}, status_code=500)

@app.get("/download_last_pptx")
def download_last_pptx():
    pptx_path = get_last_pptx_path()
    if pptx_path and os.path.exists(pptx_path):
        clear_last_pptx_path()
        pres_id = pptx_path.replace("presentation_", "").replace(".pptx", "")
        response = FileResponse(
            path=pptx_path,
            filename="presentation.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        # Удаляем pptx и PNG после скачивания (асинхронно)
        import threading
        threading.Thread(target=cleanup_presentation_files, args=(pres_id,)).start()
        return response
    return JSONResponse({"error": "Файл не найден"}, status_code=404)

@app.get("/download_pptx/{pres_id}")
def download_pptx(pres_id: str, background_tasks: BackgroundTasks):
    pptx_path = f"presentations/{pres_id}/presentation.pptx"
    if os.path.exists(pptx_path):
        response = FileResponse(
            path=pptx_path,
            filename="presentation.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        # Удаляем всю папку после скачивания
        background_tasks.add_task(shutil.rmtree, f"presentations/{pres_id}", ignore_errors=True)
        return response
    return JSONResponse({"error": "Файл не найден"}, status_code=404)
