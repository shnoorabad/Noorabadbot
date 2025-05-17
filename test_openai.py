# فایل تست: test_openai.py
import os
import openai

openai.api_key = os.environ["OPENAI_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "سلام!"}]
)

print("پاسخ از OpenAI:")
print(response["choices"][0]["message"]["content"])
