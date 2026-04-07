from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

emails = [
    {"email": "Refund my order", "label": "support"},
    {"email": "Interested in pricing", "label": "sales"},
    {"email": "Bug in product", "label": "support"},
    {"email": "Partnership request", "label": "business"}
]

state = {}
done = False

class Action(BaseModel):
    action: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    global state, done
    state = random.choice(emails)
    done = False
    return {"state": state}

@app.post("/step")
def step(action: Action):
    global state, done

    correct = action.action == state["label"]
    reward = 1.0 if correct else 0.0
    done = True

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
