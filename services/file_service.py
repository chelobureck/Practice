# Простая реализация для одного пользователя (глобальная переменная)
LAST_PPTX_PATH = None

def save_last_pptx_path(path):
    global LAST_PPTX_PATH
    LAST_PPTX_PATH = path

def get_last_pptx_path():
    global LAST_PPTX_PATH
    return LAST_PPTX_PATH

def clear_last_pptx_path():
    global LAST_PPTX_PATH
    LAST_PPTX_PATH = None