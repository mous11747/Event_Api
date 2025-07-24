# main.py
from fastapi import FastAPI
import asyncio

from app.controllers.event_controller import router
from app.services.event_service import event_service
from app.services.notification_service import notification_service

app = FastAPI(title="Event API")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Event API is running"}

# Background task
async def periodic_event_check():
    while True:
        print("🕐 Checking for upcoming events...")
        events = event_service.list_events()
        notifications = notification_service.check_and_notify(events)

        if not notifications:
            print("🔕 No upcoming events to notify.")
        await asyncio.sleep(60)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(periodic_event_check())

