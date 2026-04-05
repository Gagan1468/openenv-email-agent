from env import EmailEnv

env = EmailEnv("hard")

print("[START] task=email env=openenv model=rule-based")

state = env.reset()
done = False
step = 0
rewards = []

while not done:
    step += 1
    email = state["email"]

    if "refund" in email.lower() or "bug" in email.lower():
        action = "support"
    elif "pricing" in email.lower():
        action = "sales"
    else:
        action = "business"

    state, reward, done, info = env.step(action)
    rewards.append(reward)

    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

score = sum(rewards) / len(rewards)

print(f"[END] success=true steps={step} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards)}")
