import os
import time

def safe_remove(file_path, attempts=5):
    for _ in range(attempts):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except PermissionError:
            time.sleep(0.5)
    print(f"[ERROR] Не удалось удалить: {file_path}")
    return False

def cleanup_presentation_files(pres_id: str):
    """
    Удаляет pptx-файл и папку с PNG-слайдами по идентификатору презентации.
    """
    pptx_path = f"presentation_{pres_id}.pptx"
    png_dir = f"png_{pres_id}"
    try:
        safe_remove(pptx_path)
        if os.path.exists(png_dir):
            for f in os.listdir(png_dir):
                safe_remove(os.path.join(png_dir, f))
            os.rmdir(png_dir)
    except Exception as e:
        print(f"Ошибка при удалении файлов презентации: {e}")