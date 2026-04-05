from fastapi import FastAPI
from env import EmailEnv

app = FastAPI()
env = EmailEnv("hard")

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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=7860, reload=True)
