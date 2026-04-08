import os
import requests
import time

print("[START] Starting baseline inference - Antra Shrivastava")
ENV_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")

tasks = ["easy", "medium", "hard"]
results = []

for task in tasks:
    print(f"[STEP] Running task: {task}")
    requests.post(f"{ENV_URL}/reset")
    
    if task == "easy":
        action = {"action_type": "book_meeting", "title": "Standup", "start_time": "2026-04-09T10:00:00"}
    elif task == "medium":
        action = {"action_type": "book_meeting", "title": "Client Call", "start_time": "2026-04-10T16:00:00"}
    else:
        action = {"action_type": "book_meeting", "title": "Strategy Workshop", "start_time": "2026-04-11T11:00:00"}

    # Wrap in "action" key as expected by the OpenEnv server
    # Inside your inference.py loop
    resp = requests.post(f"{ENV_URL}/step", json={"action": action})

    
    if resp.status_code == 200:
        reward = resp.json().get("reward", 0.0)
        print(f"[STEP] {task} reward = {reward}")
        results.append(reward)
    else:
        print(f"[STEP] {task} failed with status {resp.status_code}")
        results.append(0.0)
    time.sleep(0.5)

avg = sum(results) / len(results) if results else 0.0
print(f"[END] Inference finished. Average score: {avg:.2f}")
