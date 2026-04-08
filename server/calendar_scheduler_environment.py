import uuid
from datetime import datetime, timedelta
from typing import List, Dict
from openenv.core import Environment
from models import CalendarSchedulerAction, CalendarSchedulerObservation, CalendarSchedulerState

class CalendarSchedulerEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._events = []

    def reset(self) -> CalendarSchedulerObservation:
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._events = []
        return CalendarSchedulerObservation(message="Reset", available_slots=self._get_free_slots())

    def step(self, action) -> CalendarSchedulerObservation:
        self._step_count += 1
        
        # Safe data extraction
        atype = getattr(action, "action_type", "unknown") if not isinstance(action, dict) else action.get("action_type")
        start = getattr(action, "start_time", None) if not isinstance(action, dict) else action.get("start_time")
        title = getattr(action, "title", "Meeting") if not isinstance(action, dict) else action.get("title", "Meeting")

        success = False
        if atype == "book_meeting" and start:
            clean_start = start.split("T")[-1][:5] if "T" in start else start[:5]
            if not any(e['start'] == clean_start for e in self._events):
                self._events.append({"title": title, "start": clean_start})
                success = True

        # Calculate Reward and Done
        reward_val = 0.5 if success else -0.1
        reward_val += (len(self._events) * 0.1)
        is_done = (self._step_count >= 15) or (len(self._events) >= 5)

        # Build Obs and attach data (Fixes the 500 error)
        obs = CalendarSchedulerObservation(
            message="Success" if success else "Failed",
            available_slots=self._get_free_slots(),
            current_schedule=[{"title": e["title"], "start": e["start"]} for e in self._events]
        )
        obs.reward = float(reward_val)
        obs.done = is_done
        
        return obs

    @property
    def state(self) -> CalendarSchedulerState:
        return CalendarSchedulerState(episode_id=self._episode_id, step_count=self._step_count, events=self._events)

    def _get_free_slots(self) -> List[Dict]:
        slots = []
        start_dt = datetime(2026, 4, 8, 9, 0)
        for i in range(8):
            slot = start_dt + timedelta(hours=i)
            slots.append({"start": slot.strftime("%H:%M")})
        return slots
