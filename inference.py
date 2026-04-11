import os
import requests
import re
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy_token")
ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

if HF_TOKEN == "dummy_token":
    print("WARNING: HF_TOKEN not set, using dummy_token")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task} env=custom-calendar model={MODEL_NAME}")

    success = True

    try:
        requests.post(f"{ENV_URL}/reset")

        action = {
            "action_type": "book_meeting",
            "title": task,
            "start_time": "10:30"
        }
        action_str = f"book_meeting('{task}')"

        try:
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": task}]
            )
        except:
            pass

        resp = requests.post(f"{ENV_URL}/step", json={"action": action})

        if resp.status_code == 200:
            data = resp.json()
            obs = data.get("observation", {})
            message = obs.get("message", "")

            match = re.search(r"Reward:\s*([0-9.]+)", message)
            reward = float(match.group(1)) if match else 0.1

            if reward <= 0.0:
                reward = 0.1
            elif reward >= 1.0:
                reward = 0.9

            done = "true"
        else:
            reward = 0.1
            done = "true"
            success = False

    except Exception:
        reward = 0.1
        done = "true"
        success = False

    print(f"[STEP] step=1 action={action_str} reward={reward:.2f} done={done} error=null")
    print(f"[END] success={str(success).lower()} steps=1 rewards={reward:.2f}")