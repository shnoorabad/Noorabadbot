import openai
import os

print("در حال تست کلید OpenAI...")

# مقداردهی کلید از محیط
openai.api_key = os.environ["OPENAI_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "سلام! حالت چطوره؟"}]
)

reply = response.choices[0].message.content
print("پاسخ دریافت شد:")
print(reply))
