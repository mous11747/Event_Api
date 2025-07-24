from fastapi import APIRouter, HTTPException
from app.models.event import Event
from app.services.event_service import event_service
from app.services.notification_service import notification_service

router = APIRouter()

@router.post("/events")
def create_event(event: Event):
    saved_event = event_service.add_event(event)
    return saved_event

@router.get("/events")
def list_events():
    events = event_service.list_events()
    notifications = notification_service.check_and_notify(events)
    return {
        "events": events,
        "notifications": notifications
    }

@router.get("/events/{event_id}")
def get_event(event_id: str):
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    notifications = notification_service.check_and_notify([event])
    return {
        "event": event,
        "notifications": notifications
    }
