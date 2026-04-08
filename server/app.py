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

task_list = ["easy", "medium", "hard"]
task_index = 0
@app.post("/reset_easy")
def reset_easy():
    global state, done
    state = random.choice(emails)
    state["task"] = "easy"
    done = False
    return {"state": state}

@app.post("/reset_medium")
def reset_medium():
    global state, done
    state = random.choice(emails)
    state["task"] = "medium"
    done = False
    return {"state": state}

@app.post("/reset_hard")
def reset_hard():
    global state, done
    state = random.choice(emails)
    state["task"] = "hard"
    done = False
    return {"state": state}

@app.post("/step")
def step(action: Action):
    global state, done

    correct = action.action == state["label"]

    base = 0.3 if not correct else 0.7

    bonus = {
        "easy": 0.05,
        "medium": 0.1,
        "hard": 0.15
    }

    reward = base + bonus.get(state["task"], 0)
    reward = min(reward, 0.95)

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
