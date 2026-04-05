import sys
from env import EmailEnv

difficulty = "hard"

if len(sys.argv) > 1:
    difficulty = sys.argv[1]

env = EmailEnv(difficulty)

episodes = 20
total_reward = 0
confused = []

print("Running evaluation...\n")

for i in range(episodes):
    state = env.reset()
    email = state["email"]

    # rule-based agent
    if "refund" in email.lower() or "bug" in email.lower():
        action = "support"
    elif "pricing" in email.lower():
        action = "sales"
    else:
        action = "business"

    _, reward, _, info = env.step(action)
    total_reward += reward

    if reward < 1.0:
        confused.append((email, action, info["correct_label"]))

    print(f"Episode {i+1}")
    print("Email:", email)
    print("Action:", action)
    print("Response:", info["response"])
    print("Reward:", reward)
    print("-" * 30)

accuracy = total_reward / episodes

print("\nEvaluation Summary")
print("=" * 40)
print("Total Episodes:", episodes)
print("Total Reward:", round(total_reward, 2))
print("Average Reward:", round(accuracy, 2))
print("Accuracy (%):", round(accuracy * 100, 2))
print("=" * 40)

print("\nConfused Cases:")
for item in confused:
    print("Email:", item[0])
    print("Predicted:", item[1])
    print("Correct:", item[2])
    print("-" * 20)
