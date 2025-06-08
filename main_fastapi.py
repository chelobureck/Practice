from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f_GPT import get_gpt_answer

app = FastAPI()

# Разрешаем CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_index():
    return FileResponse("index.html", media_type="text/html")

@app.get("/style.css")
def read_css():
    return FileResponse("style.css", media_type="text/css")

@app.get("/main.js")
def read_js():
    return FileResponse("main.js", media_type="application/javascript")

@app.post("/gpt")
async def gpt_answer(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    if not prompt:
        return JSONResponse({"error": "No prompt provided"}, status_code=400)
    response = get_gpt_answer(prompt)
    return JSONResponse({"answer": response})
