import g4f

def get_gpt_answer(prompt: str) -> str:
    response = g4f.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response