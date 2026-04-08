import uuid
import os
from typing import Tuple
from openenv.core import Environment
from models import CalendarSchedulerObservation, CalendarSchedulerState
from openai import OpenAI

api_base = os.environ.get("API_BASE_URL")
api_key = os.environ.get("API_KEY")

client = OpenAI(base_url=api_base, api_key=api_key) if api_base and api_key else None


class CalendarSchedulerEnvironment(Environment):
    """Calendar environment with optional LLM-assisted meeting scheduling."""

    def __init__(self):
        super().__init__()
        self.episode_id = str(uuid.uuid4())
        self.reset()

    def reset(self):
        self._state = CalendarSchedulerState(
            episode_id=self.episode_id,
            step_count=0,
            events=[],
            constraints={"earliest": "09:00"}
        )
        return CalendarSchedulerObservation(
            message="Calendar ready",
            available_slots=[
                {"start": "09:30"},
                {"start": "10:30"},
                {"start": "11:30"}
            ],
            current_schedule=[],
            feedback="Ready"
        )

    def step(self, action) -> Tuple[CalendarSchedulerObservation, float, bool, dict]:
        # OpenEnv passes actions as dicts, unwrap if nested
        if isinstance(action, dict) and "action_type" not in action:
            action = action.get("action", action)

        action_type = action.get("action_type")
        title = action.get("title", "Meeting")
        start_time = action.get("start_time", "10:30")

        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a smart calendar scheduling assistant."
                        },
                        {
                            "role": "user",
                            "content": f"Schedule a meeting titled '{title}' at {start_time}. Suggest if this is a good time."
                        }
                    ]
                )
                llm_output = response.choices[0].message.content
            except Exception:
                llm_output = f"Meeting scheduled at {start_time}"
        else:
            llm_output = f"Meeting scheduled at {start_time}"

        reward = 0.4 if action_type == "book_meeting" else -0.1

        self._state.events.append({
            "title": title,
            "start_time": start_time
        })

        obs = CalendarSchedulerObservation(
            message=llm_output,
            available_slots=[
                {"start": "09:30"},
                {"start": "10:30"}
            ],
            current_schedule=self._state.events,
            feedback="Processed"
        )

        return obs, reward, True, {}

    def state(self):
        return self._state