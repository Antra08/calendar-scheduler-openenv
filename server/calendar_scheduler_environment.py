import uuid
import os
from openenv.core import Environment
from models import CalendarSchedulerObservation, CalendarSchedulerState
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
) if "API_BASE_URL" in os.environ and "API_KEY" in os.environ else None


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

    def step(self, action):
        if isinstance(action, dict):
            if "action_type" not in action:
                action = action.get("action", action)
            action_type = action.get("action_type")
            title = action.get("title", "Meeting")
            start_time = action.get("start_time", "10:30")
        else:
            action_type = action.action_type
            title = action.title or "Meeting"
            start_time = action.start_time or "10:30"

        title_lower = title.lower()

        if action_type != "book_meeting":
            reward = 0.0
        elif "easy" in title_lower:
            reward = 1.0
        elif "medium" in title_lower:
            reward = 0.6
        elif "hard" in title_lower:
            reward = 0.2
        else:
            reward = 0.4

        if client is not None:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a calendar assistant."},
                        {"role": "user", "content": f"Schedule meeting '{title}' at {start_time}"}
                    ]
                )
                llm_output = response.choices[0].message.content
            except Exception:
                llm_output = f"Meeting '{title}' scheduled at {start_time}"
        else:
            llm_output = f"Meeting '{title}' scheduled at {start_time}"

        self._state.events.append({
            "title": title,
            "start_time": start_time
        })

        return CalendarSchedulerObservation(
            message=f"{llm_output} | Reward: {reward:.2f}",
            available_slots=[
                {"start": "09:30"},
                {"start": "10:30"}
            ],
            current_schedule=self._state.events,
            feedback="Processed"
        )

    def state(self):
        return self._state