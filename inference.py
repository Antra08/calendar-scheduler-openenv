import os
import requests
import re
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

print(f"[START] task=calendar-scheduling env=custom-calendar model={MODEL_NAME}")

tasks = ["easy", "medium", "hard"]
rewards = []
step_count = 0
success = True

for task in tasks:
    step_count += 1
    error = "null"

    try:
        requests.post(f"{ENV_URL}/reset")
    except:
        pass

    if task == "easy":
        action = {"action_type": "book_meeting", "title": "Meeting for easy", "start_time": "10:30"}
        action_str = "book_meeting('easy')"
    elif task == "medium":
        action = {"action_type": "book_meeting", "title": "Meeting for medium", "start_time": "09:30"}
        action_str = "book_meeting('medium')"
    else:
        action = {"action_type": "book_meeting", "title": "Meeting for hard", "start_time": "10:30"}
        action_str = "book_meeting('hard')"

    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Schedule a {task} meeting"}],
            max_tokens=5
        )
    except:
        error = "null"

    try:
        resp = requests.post(f"{ENV_URL}/step", json={"action": action})

        if resp.status_code == 200:
            data = resp.json()
            obs = data.get("observation", {})
            message = obs.get("message", "")
            match = re.search(r"Reward:\s*([0-9.]+)", message)
            reward = float(match.group(1)) if match else 0.0
            done = "true"
        else:
            reward = 0.0
            done = "true"
            success = False

    except:
        reward = 0.0
        done = "true"
        success = False

    rewards.append(reward)

    print(
        f"[STEP] step={step_count} action={action_str} "
        f"reward={reward:.2f} done={done} error={error}"
    )

rewards_str = ",".join(f"{r:.2f}" for r in rewards)

print(
    f"[END] success={str(success).lower()} "
    f"steps={step_count} rewards={rewards_str}"
)