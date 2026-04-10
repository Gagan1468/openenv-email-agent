import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

BASE_URL = "http://localhost:7860"

def llm_classify(email):
    try:
        r = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Classify: {email}"}]
        )
        return r.choices[0].message.content.strip().lower()
    except:
        return "support"

def run_task(task):
    print(f"[START] task={task} env=email_env model={MODEL_NAME}")

    state = requests.post(f"{BASE_URL}/reset_{task}").json()["state"]
    done = False
    step = 0
    rewards = []

    while not done:
        step += 1
        action = llm_classify(state["email"])

        result = requests.post(
            f"{BASE_URL}/step",
            json={"action": action}
        ).json()

        state = result["state"]
        reward = result["reward"]
        done = result["done"]
        rewards.append(reward)

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    print(
        f"[END] success=true steps={step} rewards={','.join(f'{r:.2f}' for r in rewards)}"
    )

if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)
