from typing import List, Dict, Optional
from pydantic import BaseModel

class CalendarSchedulerAction(BaseModel):
    action_type: str = "book_meeting"
    title: Optional[str] = "Meeting"
    start_time: Optional[str] = "10:00"
    duration: int = 30

class CalendarSchedulerObservation(BaseModel):
    message: str = ""
    available_slots: List[Dict] = []
    current_schedule: List[Dict] = []
    feedback: str = ""
    # Added these for your specific library version
    reward: float = 0.0
    done: bool = False

class CalendarSchedulerState(BaseModel):
    episode_id: str = ""
    step_count: int = 0
    events: List[Dict] = []
