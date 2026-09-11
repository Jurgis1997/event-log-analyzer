"""Event Log Analyzer

Fill in the TODOs. Feel free to restructure anything here. this is just a starting point.
"""

import csv
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path


class EventSeverity(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3


@dataclass
class Event:
    event_number: int
    timestamp: str
    severity: EventSeverity
    object_name: str
    object_id: int
    event_id: int
    event_name: str
    description: str
    remedy: str
    readable: str
    raw: str


def load_events(path):
    events = []

    with open(path, "r", encoding="utf-8") as file:
        next(file)
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            severity = EventSeverity[row["Severity"].upper()]

            event = Event(
                event_number=int(row["Event number"]),
                timestamp=row["Timestamp"],
                severity=severity,
                object_name=row["Object name"],
                object_id=int(row["Object ID"]),
                event_id=int(row["Event ID"]),
                event_name=row["Event name"],
                description=row["Description"],
                remedy=row["Remedy"],
                readable=row["Readable"],
                raw=row["Raw"],
            )

            events.append(event)

    return events


class EventLog:
    def __init__(self, events):
        self._events = events

    def filter_by_severity(self, min_severity):
        return [
            event
            for event in self._events
            if event.severity >= min_severity
        ]

    def count_by_object(self):
        counts = {}

        for event in self._events:
            counts[event.object_name] = counts.get(event.object_name, 0) + 1

        return counts

    @property
    def error_rate(self):
        if not self._events:
            return 0.0

        error_count = sum(
            event.severity == EventSeverity.ERROR
            for event in self._events
        )

        return error_count / len(self._events)


if __name__ == "__main__":
    events = load_events(Path(__file__).parent / "event_log_sample.csv")
    log = EventLog(events)
    print(f"Loaded {len(events)} events")