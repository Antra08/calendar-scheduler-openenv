from openenv.core.env_server import create_fastapi_app
from models import CalendarSchedulerAction, CalendarSchedulerObservation
from .calendar_scheduler_environment import CalendarSchedulerEnvironment

app = create_fastapi_app(
    CalendarSchedulerEnvironment, 
    CalendarSchedulerAction, 
    CalendarSchedulerObservation
)
