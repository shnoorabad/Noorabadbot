import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_KEY"])

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "سلام"}]
)

print(response.choices[0].message.content)
