import os
import requests
from openai import OpenAI

# Connect to validator's proxy
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

BASE_URL = "http://localhost:7860"

def llm_classify(email_text):
    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[{
            "role": "user",
            "content": f"Classify this email into one of: support, sales, business.\nEmail: {email_text}\nReply with just the category word."
        }]
    )
    return response.choices[0].message.content.strip().lower()

print("[START] task=email env=openenv model=gpt-4o-mini")

# Reset environment
state = requests.post(f"{BASE_URL}/reset").json()["state"]

done = False
step = 0
rewards = []

while not done:
    step += 1
    email = state["email"]

    action = llm_classify(email)

    if action not in ["support", "sales", "business"]:
        action = "business"

    result = requests.post(f"{BASE_URL}/step", json={"action": action}).json()
    state = result["state"]
    reward = result["reward"]
    done = result["done"]
    rewards.append(reward)

    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

score = sum(rewards) / len(rewards)
print(f"[END] success=true steps={step} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards)}")
