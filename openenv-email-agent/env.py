import random

class EmailEnv:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

        # action space (Gym style)
        self.action_space = ["support", "sales", "business"]

        # response templates
        self.responses = {
            "support": "We will resolve your issue shortly.",
            "sales": "Here is our pricing information.",
            "business": "Let's schedule a partnership call."
        }

        self.easy = [
            {"text": "Refund my order", "label": "support"},
            {"text": "Interested in pricing", "label": "sales"},
        ]

        self.medium = [
            {"text": "Bug in product", "label": "support"},
            {"text": "Partnership request", "label": "business"},
        ]

        self.hard = [
            {"text": "Need invoice clarification", "label": "support"},
            {"text": "Enterprise pricing discussion", "label": "sales"},
            {"text": "Collaboration opportunity", "label": "business"},
        ]

        self.current = None

    def reset(self):
        if self.difficulty == "easy":
            pool = self.easy
        elif self.difficulty == "medium":
            pool = self.easy + self.medium
        else:
            pool = self.easy + self.medium + self.hard

        self.current = random.choice(pool)

        # stochastic noise (20% chance)
        if random.random() < 0.2:
            self.current = {
                "text": "Hello there, just checking in",
                "label": "business"
            }

        return self.state()

    def state(self):
        # structured observation
        return {
            "email": self.current["text"],
            "length": len(self.current["text"])
        }

    def step(self, action):
        correct = action == self.current["label"]

        if correct:
            reward = 1.0
        elif action in self.action_space:
            reward = 0.3
        else:
            reward = 0.0

        info = {
            "correct_label": self.current["label"],
            "response": self.responses.get(action, "")
        }

        return self.state(), reward, True, info
