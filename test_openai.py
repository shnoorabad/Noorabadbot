import openai
import os

openai.api_key = os.environ["OPENAI_KEY"]

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "سلام، حال شما چطوره؟"}]
    )
    print("پاسخ OpenAI:")
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print("خطا:", e)
