import json
from g4f_GPT import get_gpt_answer

def get_gpt_plan(history):
    messages = []
    for msg in history:
        role = msg.get("role")
        text = msg.get("text")
        if role and text:
            messages.append({"role": role, "content": text})

    system_prompt = (
        "Ты — помощник, который помогает создавать презентации. "
        "Отвечай только в формате JSON: [{'title':..., 'text':..., 'image':...}, ...]. "
        "Добавляй картинки к каждому слайду по теме. "
        "Не добавляй пояснений, только JSON!"
    )
    messages = [{"role": "system", "content": system_prompt}] + messages
    plan = get_gpt_answer(messages)
    try:
        plan_data = json.loads(plan)
        if isinstance(plan_data, list):
            slides = []
            for item in plan_data:
                slides.append({
                    "title": str(item.get("title", "")),
                    "text": str(item.get("text", "")),
                    "image": str(item.get("image", "")),
                })
            return slides
        return []
    except Exception:
        return []

def validate_plan(plan):
    if not isinstance(plan, list):
        return False
    for slide in plan:
        if not isinstance(slide, dict):
            return False
        if not all(k in slide for k in ("title", "text", "image")):
            return False
    return True