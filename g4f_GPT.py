import g4f

def get_gpt_answer(messages):
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response