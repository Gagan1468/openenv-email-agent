from fastapi import FastAPI
from env import EmailEnv
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("API_KEY", "test")
)

env = EmailEnv("hard")


@app.on_event("startup")
def call_llm_on_startup():
    base = os.environ.get("API_BASE_URL")
    key = os.environ.get("API_KEY")

    # Only call when validator injects keys
    if not base or not key:
        print("LLM env vars not present — skipping startup call")
        return

    print("Calling LLM for validator...")

    client = OpenAI(base_url=base, api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Reply OK"}]
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
    base = os.environ.get("API_BASE_URL")
    key = os.environ.get("API_KEY")

    if base and key:
        client = OpenAI(base_url=base, api_key=key)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Reply OK"}]
            )
            return {
                "message": "OpenEnv Email Agent is running",
                "llm": response.choices[0].message.content
            }
        except Exception as e:
            return {"message": "running", "llm_error": str(e)}

    return {"message": "OpenEnv Email Agent is running"}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
