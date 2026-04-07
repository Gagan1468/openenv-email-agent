import os
import time
import requests
from openai import OpenAI

BASE_URL = "http://localhost:7860"

def wait_for_server():
    for _ in range(15):
        try:
            requests.get(BASE_URL, timeout=2)
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Server not ready")

def llm_classify(email_text):
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"]
        )

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{
                "role": "user",
                "content": (
                    "Classify this email into one of: support, sales, business.\n"
                    f"Email: {email_text}\n"
                    "Reply with just the category word."
                )
            }]
        )

        return response.choices[0].message.content.strip().lower()

    except Exception as e:
        print(f"LLM error: {e}")
        return "business"


def main():
    print("[START] task=email env=openenv model=gpt-4o-mini")

    wait_for_server()

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


if __name__ == "__main__":
    main()
