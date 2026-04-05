import random

class EmailEnv:
    def __init__(self):
        self.emails = [
            {"text": "Refund my order", "label": "support"},
            {"text": "Interested in pricing", "label": "sales"},
            {"text": "Bug in product", "label": "support"},
            {"text": "Partnership request", "label": "business"}
        ]
        self.current = None
        self.done = False

    def reset(self):
        self.current = random.choice(self.emails)
        self.done = False
        return self.state()

    def state(self):
        return self.current["text"]

    def step(self, action):
        correct = action == self.current["label"]
        reward = 1.0 if correct else 0.0
        self.done = True
        return self.state(), reward, self.done, {}
