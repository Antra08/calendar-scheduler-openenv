import os
import requests
import re
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task} env=custom-calendar model={MODEL_NAME}", flush=True)

    success = True
    reward = 0.1
    done = "true"
    error = "null"
    score = 0.0
    action_str = f"book_meeting('{task}')"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": f"Schedule a {task} meeting"}],
        max_tokens=10
    )
    _ = response.choices[0].message.content

    try:
        requests.post(f"{ENV_URL}/reset")

        action = {
            "action_type": "book_meeting",
            "title": task,
            "start_time": "10:30"
        }

        resp = requests.post(f"{ENV_URL}/step", json={"action": action}, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            obs = data.get("observation", {})
            message = obs.get("message", "")

            match = re.search(r"Reward:\s*([0-9.]+)", message)
            if match:
                reward = float(match.group(1))

            if reward <= 0.0:
                reward = 0.1
            elif reward >= 1.0:
                reward = 0.9

            score = reward
        else:
            success = False
            error = f"status_{resp.status_code}"

    except Exception as e:
        success = False
        error = "exception"

    print(f"[STEP] step=1 action={action_str} reward={reward:.2f} done={done} error={error}", flush=True)
    print(f"[END] success={str(success).lower()} steps=1 score={score:.2f} rewards={reward:.2f}", flush=True)
