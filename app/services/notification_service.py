from datetime import datetime
from app.models.event import Event
import zoneinfo

class NotificationService:
    def __init__(self):
        self._notified_events = set()
    
    def check_and_notify(self, events: list[Event]) -> list[str]:
        """Check events and return notifications for those about to start, preventing duplicates"""
        notifications = []
        
        for event in events:
            if event.id not in self._notified_events and self._should_notify(event):
                notification_msg = self._create_notification(event)
                notifications.append(notification_msg)
                self._notified_events.add(event.id)
                # Still print to console for debugging
                print(f"[Console] {notification_msg}")
        
        return notifications
    
    def _should_notify(self, event: Event) -> bool:
        """Check if an event should trigger a notification (within 5 minutes of start time)"""
        # Set timezone to Europe/Brussels (CEST)
        brussels_tz = zoneinfo.ZoneInfo("Europe/Brussels")
        now = datetime.now(brussels_tz)

        print(f"🔍 Checking notifications at Day {now.date()} Time {now.time().strftime('%H:%M:%S')} ({now.tzinfo})")

        # Assume event.datetime is either already timezone-aware,
        # or comes in naive (no tzinfo) and should be interpreted as CEST
        if event.datetime.tzinfo is None:
            event_dt = event.datetime.replace(tzinfo=brussels_tz)
        else:
            event_dt = event.datetime.astimezone(brussels_tz)

        print(f"📅 Event '{event.title}' is scheduled at Day {event_dt.date()} Time {event_dt.time().strftime('%H:%M:%S')} ({event_dt.tzinfo})")

        delta = (event_dt - now).total_seconds()
        print(f"  ⏱️ Starts in {delta:.2f} seconds")

        # Return True if event starts within the next 5 minutes (300 seconds)
        return 0 <= delta < 300
    
    def _create_notification(self, event: Event) -> str:
        """Create the notification message"""
        return f"🔔 Event '{event.title}' is about to start!"
    
    def reset_notifications(self) -> None:
        """Reset the notification tracking (useful for testing or daily cleanup)"""
        self._notified_events.clear()
        print("🔄 Notification tracking reset")
    
    def get_notified_events(self) -> set:
        """Get the set of events that have already been notified (useful for debugging)"""
        return self._notified_events.copy()

# Create reusable service instance
notification_service = NotificationService()
