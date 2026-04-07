from fastapi import FastAPI
from env import EmailEnv
import os
from openai import OpenAI
import threading
import time
import requests

app = FastAPI()
env = EmailEnv("hard")


def make_llm_call(label: str = "LLM"):
    base = os.environ.get("API_BASE_URL")
    key = os.environ.get("API_KEY")

    if not base or not key:
        print(f"[{label}] API_BASE_URL or API_KEY not set")
        return None

    try:
        client = OpenAI(base_url=base, api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply OK"}]
        )
        print(f"[{label}] Call succeeded: {response.choices[0].message.content}")
        return response
    except Exception as e:
        print(f"[{label}] Call failed: {e}")
        return None


def startup_llm_trigger():
    time.sleep(3)
    print("ENV CHECK →", {
        "API_BASE_URL": os.environ.get("API_BASE_URL", "NOT SET"),
        "API_KEY": "SET" if os.environ.get("API_KEY") else "NOT SET"
    })
    make_llm_call("startup-trigger")

@app.on_event("startup")
def startup():
    # Fire startup LLM call in background after server is ready
    threading.Thread(target=startup_llm_trigger, daemon=True).start()


@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}


@app.post("/step")
def step(action: dict):
    act = action.get("action")
    state, reward, done, info = env.step(act)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/")
def root():
    base = os.environ.get("API_BASE_URL")
    key = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN")

    print(f"API_BASE_URL: '{base}'")
    print(f"API_KEY present: {bool(key)}")

    if not key:
        print("Missing API_KEY")
        return {"message": "running", "llm": "unavailable"}

    try:
        client = OpenAI(base_url=base, api_key=key)  # base can be None, OpenAI handles it
        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "Reply OK"}]
        )
        print("LLM call succeeded:", response.choices[0].message.content)
        return {"message": "running", "llm": response.choices[0].message.content}

    except BaseException as e:
        print("LLM call failed:", repr(e))
        return {"message": "running", "llm": "unavailable"}

def main():
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
