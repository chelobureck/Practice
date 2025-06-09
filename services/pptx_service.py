import requests
from pptx import Presentation
import aspose.slides as slides
import aspose.pydrawing as drawing
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid
import base64
from services.file_cleanup import cleanup_presentation_files

app = FastAPI()

def make_pptx_file(plan, filename: str = "presentation.pptx") -> str:
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Презентация"
    slide.placeholders[1].text = "Сгенерировано автоматически"
    for item in plan:
        title = item.get("title", "")
        text = item.get("text", "")
        image_url = item.get("image", "")
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        slide.placeholders[1].text = text
        if image_url:
            try:
                img_data = requests.get(image_url, timeout=10).content
                img_path = f"temp_img_{title[:10]}.png"
                with open(img_path, "wb") as f:
                    f.write(img_data)
                left = top = prs.slide_width // 10
                slide.shapes.add_picture(img_path, left, top, width=prs.slide_width // 2)
                os.remove(img_path)
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")
    prs.save(filename)
    return filename

def pptx_to_png(pptx_path, output_dir):
    pres = slides.Presentation(pptx_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    png_files = []
    for i, slide in enumerate(pres.slides):
        out_path = os.path.join(output_dir, f"slide_{i+1}.png")
        image = slide.get_thumbnail(1, 1)
        image.save(out_path, drawing.imaging.ImageFormat.png)
        png_files.append(out_path)
    return png_files

@app.post("/generate_presentation")
async def generate_presentation(request: Request):
    data = await request.json()
    pptx_code = data.get("pptx_code")
    if not pptx_code:
        return JSONResponse({"error": "No pptx code provided"}, status_code=400)

    pres_id = uuid.uuid4().hex
    filename = f"presentation_{pres_id}.pptx"
    pptx_path = make_pptx_file(pptx_code, filename)

    png_dir = f"png_{pres_id}"
    os.makedirs(png_dir, exist_ok=True)
    png_files = pptx_to_png(pptx_path, png_dir)
    images = []
    for png_file in png_files:
        with open(png_file, "rb") as f:
            images.append("data:image/png;base64," + base64.b64encode(f.read()).decode())
    # Удаляем файлы после генерации (асинхронно)
    import threading
    threading.Thread(target=cleanup_presentation_files, args=(pres_id,)).start()
    return JSONResponse({"images": images})