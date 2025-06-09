import os

def cleanup_presentation_files(pres_id: str):
    """
    Удаляет pptx-файл и папку с PNG-слайдами по идентификатору презентации.
    """
    pptx_path = f"presentation_{pres_id}.pptx"
    png_dir = f"png_{pres_id}"
    if os.path.exists(pptx_path):
        try:
            os.remove(pptx_path)
        except Exception as e:
            print(f"Ошибка удаления pptx: {e}")
    if os.path.exists(png_dir):
        try:
            for f in os.listdir(png_dir):
                os.remove(os.path.join(png_dir, f))
            os.rmdir(png_dir)
        except Exception as e:
            print(f"Ошибка удаления PNG-директории: {e}")