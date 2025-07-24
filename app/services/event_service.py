from typing import List, Optional
from app.models.event import Event

class EventService:
    def __init__(self):
        self._events: List[Event] = []

    def add_event(self, event: Event) -> Event:
        self._events.append(event)
        return event

    def list_events(self) -> List[Event]:
        return self._events

    def get_event(self, event_id: str) -> Optional[Event]:
        for event in self._events:
            if str(event.id) == str(event_id):
                return event
        return None

event_service = EventService()

