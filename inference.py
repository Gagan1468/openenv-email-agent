import os
import requests
from openai import OpenAI

BASE_URL = "http://localhost:7860"

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

def llm_classify(email):
    try:
        resp = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{
                "role": "user",
                "content": f"Classify email into support, sales, business:\n{email}"
            }]
        )
        return resp.choices[0].message.content.strip().lower()
    except:
        return "business"


def run_task(task):
    print(f"[START] task={task}", flush=True)

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
        rewards.append(reward)
        done = result["done"]

        print(f"[STEP] task={task} step={step} reward={reward}", flush=True)

    score = sum(rewards) / len(rewards)
    print(f"[END] task={task} score={score} steps={step}", flush=True)

    return score


def main():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()
