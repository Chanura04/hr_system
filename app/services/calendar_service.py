from datetime import datetime, timedelta
from typing import Dict, Any
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

class CalendarService:
    """
    A service to interact with Google Calendar using the gcsa library.
    """

    @staticmethod
    def check_availability(query: str) -> bool:
        # Placeholder: Real-world logic would verify against existing events
        return True

    @staticmethod
    def sync_event(query: str, category: str) -> Dict[str, Any]:
        try:
            # GoogleCalendar() looks for credentials.json and token.pickle locally
            calendar = GoogleCalendar()

            # Placeholder: Defaults to a 30-min block starting 1 hour from now.
            # In a full implementation, use an LLM node to extract dates from 'query'.
            start = datetime.now() + timedelta(hours=1)
            end = start + timedelta(minutes=30)

            event = Event(
                summary=f"[{category.upper()}] {query[:50]}",
                start=start,
                end=end
            )
            created_event = calendar.add_event(event)
            return {"status": "success", "event_id": created_event.id}
        except Exception as e:
            return {"status": "error", "message": str(e)}