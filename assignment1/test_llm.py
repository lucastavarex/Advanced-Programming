import pytest
from datetime import datetime
from scheduler import SuperFrog, Event

def test_assign_event_no_conflict():
    sf = SuperFrog("João")
    e1 = Event(1, datetime(2025, 5, 10, 14), datetime(2025, 5, 10, 16))
    e2 = Event(2, datetime(2025, 5, 10, 16), datetime(2025, 5, 10, 17))

    assert sf.assign_event(e1) == True
    assert sf.assign_event(e2) == True
    assert len(sf.schedule) == 2

def test_assign_event_with_conflict():
    sf = SuperFrog("Maria")
    e1 = Event(1, datetime(2025, 5, 10, 14), datetime(2025, 5, 10, 16))
    e2 = Event(2, datetime(2025, 5, 10, 15, 30), datetime(2025, 5, 10, 17))

    assert sf.assign_event(e1) == True
    assert sf.assign_event(e2) == False
    assert len(sf.schedule) == 1