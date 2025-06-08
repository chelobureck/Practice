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
        "Если пользователь исправляет или дополняет презентацию, учитывай всю историю диалога и свои предыдущие ответы, не повторяй уже сгенерированные части, а только исправляй или дополняй."
    )
    messages = [{"role": "system", "content": system_prompt}] + messages
    plan = get_gpt_answer(messages)
    try:
        plan_data = json.loads(plan)
        if isinstance(plan_data, list) and all(isinstance(item, dict) for item in plan_data):
            return plan_data
        else:
            return [{"title": str(item), "text": "", "image": ""} for item in plan_data]
    except Exception:
        return [{"title": line.strip(), "text": "", "image": ""} for line in plan.split('\n') if line.strip()]