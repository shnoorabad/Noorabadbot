import os
import openai

openai.api_key = os.environ["OPENAI_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "سلام! حالت چطوره؟"}
    ]
)

reply = response["choices"][0]["message"]["content"]
print(reply)
