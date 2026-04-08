# Calendar Scheduler by Antra Shrivastava

This is my submission for OpenEnv Round 1.

I made a calendar where an AI can book meetings. It checks for time clashes and doesn't allow meetings before 9 AM.

Tasks:
- Easy: Book 1 meeting
- Medium: Book 3 meetings
- Hard: Book 5 meetings respecting the time rules

Setup:
uv sync
uvicorn server.app:app --reload

I tried to make the reward give partial points as more meetings are booked.

