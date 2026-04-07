import os
from env import EmailEnv
from openai import OpenAI

# MUST use their proxy
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

env = EmailEnv()

state = env.reset()
print("Email:", state)

prompt = f"""
Classify this email into one category:
support, sales, business

Email:
{state}

Only return the category.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

action = response.choices[0].message.content.strip().lower()

print("Agent action:", action)

state, reward, done, _ = env.step(action)

print("Reward:", reward)
