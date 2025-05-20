import pytest
from datetime import datetime
from scheduler import SuperFrog, Event

def test_assign_multiple_events_without_conflict():
    super_frog = SuperFrog("Lucas")
    event1 = Event(1, datetime(2025, 5, 5, 8), datetime(2025, 5, 5, 10))
    event2 = Event(2, datetime(2025, 5, 5, 10, 30), datetime(2025, 5, 5, 12))
    event3 = Event(3, datetime(2025, 5, 5, 13), datetime(2025, 5, 5, 14))
    
    assert super_frog.assign_event(event1) is True
    assert super_frog.assign_event(event2) is True
    assert super_frog.assign_event(event3) is True
    assert len(super_frog.schedule) == 3

def test_assign_event_with_time_overlap():
    super_frog = SuperFrog("Lucas")
    event1 = Event(1, datetime(2025, 5, 5, 14), datetime(2025, 5, 5, 16))
    event2 = Event(2, datetime(2025, 5, 5, 15, 30), datetime(2025, 5, 5, 17))
    
    assert super_frog.assign_event(event1) is True
    assert super_frog.assign_event(event2) is False
    assert len(super_frog.schedule) == 1