from datetime import datetime

class Event:
    def __init__(self, event_id, start_time, end_time):
        self.event_id = event_id
        self.start_time = start_time
        self.end_time = end_time

class SuperFrog:
    def __init__(self, name):
        self.name = name
        self.schedule = []

    def has_conflict(self, new_event):
        for event in self.schedule:
            if not (new_event.end_time <= event.start_time or new_event.start_time >= event.end_time):
                return True
        return False

    def assign_event(self, new_event):
        if self.has_conflict(new_event):
            return False
        self.schedule.append(new_event)
        return True