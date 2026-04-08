import uvicorn
from openenv.core.env_server import create_fastapi_app
from models import CalendarSchedulerAction, CalendarSchedulerObservation
from server.calendar_scheduler_environment import CalendarSchedulerEnvironment

# Create app
app = create_fastapi_app(
    CalendarSchedulerEnvironment,
    CalendarSchedulerAction,
    CalendarSchedulerObservation
)

# Optional root endpoint
@app.get("/")
def home():
    return {"status": "running"}


# IMPORTANT: main must be VERY SIMPLE
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


# IMPORTANT: must be EXACT
if __name__ == "__main__":
    main()