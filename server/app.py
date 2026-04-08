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
    difficulty = random.choice(["easy", "medium", "hard"])
    state = random.choice(emails)
    done = False
    return {"state": {**state, "task": difficulty}}

@app.post("/step")
def step(action: Action):
    global state, done

    correct = action.action == state["label"]

    # base reward
    reward = 0.6 if correct else 0.2

    # difficulty bonus
    task_bonus = {
        "easy": 0.05,
        "medium": 0.1,
        "hard": 0.15
    }

    reward += task_bonus.get(state.get("task","easy"),0)

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
