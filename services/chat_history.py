import threading

_chat_histories = {}
_lock = threading.Lock()

def get_history(session_id):
    with _lock:
        return _chat_histories.get(session_id, []).copy()

def add_message(session_id, role, text):
    with _lock:
        if session_id not in _chat_histories:
            _chat_histories[session_id] = []
        _chat_histories[session_id].append({"role": role, "text": text})

def clear_history(session_id):
    with _lock:
        if session_id in _chat_histories:
            del _chat_histories[session_id]