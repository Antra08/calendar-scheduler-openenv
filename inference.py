import os
import requests
import time
import re

ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

start_times = {
    "easy":   "10:30",
    "medium": "09:30",
    "hard":   "10:30",
}

results = []

for task, start_time in start_times.items():
    print(f"Running task: {task}")

    requests.post(f"{ENV_URL}/reset")

    step_data = {
        "action": {
            "action_type": "book_meeting",
            "title": f"Meeting for {task}",
            "start_time": start_time,
            "duration": 30
        }
    }

    resp = requests.post(f"{ENV_URL}/step", json=step_data)

    if resp.status_code == 200:
        data = resp.json()
        message = data.get("observation", {}).get("message", "")
        match = re.search(r"Reward:\s*([0-9.]+)", message)
        reward = float(match.group(1)) if match else 0.0
        print(f"{task} reward = {reward}")
        results.append(reward)
    else:
        print(f"{task} failed with status {resp.status_code}: {resp.text}")
        results.append(0.0)

    time.sleep(0.5)

avg = sum(results) / len(results) if results else 0.0
scores = {task: results[i] if i < len(results) else 0.0 for i, task in enumerate(start_times)}

print(f"Inference finished. Average score: {avg:.2f}")
print(f"Scores -> Easy: {scores['easy']:.2f}, Medium: {scores['medium']:.2f}, Hard: {scores['hard']:.2f}")