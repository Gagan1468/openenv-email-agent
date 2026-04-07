from fastapi import FastAPI
from env import EmailEnv
import os
from openai import OpenAI
import threading
import time
import requests

app = FastAPI()

env = EmailEnv("hard")


def trigger_self_call():
    time.sleep(2)
    try:
        requests.get("http://127.0.0.1:7860/")
        print("Self-call triggered")
    except Exception as e:
        print("Self-call failed:", e)


@app.on_event("startup")
def startup():
    threading.Thread(target=trigger_self_call).start()


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
    try:
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL", ""),
            api_key=os.environ.get("API_KEY", "")
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply OK"}]
        )

        print("LLM CALLED")
        return {"message": "running", "llm": response.choices[0].message.content}

    except Exception as e:
        print("LLM call skipped:", str(e))
        return {"message": "running"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
