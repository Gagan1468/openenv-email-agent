import os
import requests
import time
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
    state = requests.post(f"{BASE_URL}/reset_{task}").json()["state"]
    done = False
    rewards = []

    while not done:
        action = llm_classify(state["email"])
        result = requests.post(
            f"{BASE_URL}/step",
            json={"action": action}
        ).json()

        state = result["state"]
        rewards.append(result["reward"])
        done = result["done"]

    return sum(rewards) / len(rewards)


def main():
    tasks = ["easy", "medium", "hard"]
    scores = []

    for task in tasks:
        score = run_task(task)
        print(f"[TASK] {task} score={score}")
        scores.append(score)

    final = sum(scores) / len(scores)
    print(f"[FINAL SCORE] {final}")


if __name__ == "__main__":
    main()
