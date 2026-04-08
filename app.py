import uvicorn
from openenv.core.env_server import create_fastapi_app
from models import CalendarSchedulerAction, CalendarSchedulerObservation
from .calendar_scheduler_environment import CalendarSchedulerEnvironment

# Create the standard OpenEnv app
app = create_fastapi_app(
    CalendarSchedulerEnvironment,
    CalendarSchedulerAction,
    CalendarSchedulerObservation
)

#  Optional (removes 404 on /)
@app.get("/")
def home():
    return {"status": "running"}

#  REQUIRED for OpenEnv validation
def main():
    """Main entry point for the server."""
    uvicorn.run(app, host="0.0.0.0", port=7860)


# REQUIRED block
if __name__ == "__main__":
    main()