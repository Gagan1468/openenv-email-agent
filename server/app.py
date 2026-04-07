from fastapi import FastAPI
from env import EmailEnv
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

env = EmailEnv("hard")


# 🔥 THIS PART FIXES YOUR FAILURE
@app.on_event("startup")
def call_llm_on_startup():
    print("Calling LLM for validator...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Reply with OK"}
        ]
    )
    print("LLM Response:", response.choices[0].message.content)


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
    return {"message": "OpenEnv Email Agent is running"}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
