import uvicorn
import os
from openenv.core.env_server import create_fastapi_app
from models import CalendarSchedulerAction, CalendarSchedulerObservation
from server.calendar_scheduler_environment import CalendarSchedulerEnvironment

# Create app
app = create_fastapi_app(
    CalendarSchedulerEnvironment,
    CalendarSchedulerAction,
    CalendarSchedulerObservation
)

@app.get("/")
def home():
    return {"status": "running"}



def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)



if __name__ == "__main__":
    main()