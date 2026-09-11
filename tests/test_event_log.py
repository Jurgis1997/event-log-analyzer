from pathlib import Path

from starter import EventLog, EventSeverity, load_events


PROJECT_ROOT = Path(__file__).parent.parent
LOG_FILE = PROJECT_ROOT / "event_log_sample.csv"


def test_event_severity_ordering():
    assert EventSeverity.INFO < EventSeverity.WARNING
    assert EventSeverity.WARNING < EventSeverity.ERROR


def test_load_events():
    events = load_events(LOG_FILE)

    assert len(events) == 280
    assert events[0].event_number == 10488
    assert events[0].timestamp == "2000-01-01 00:00:01"
    assert events[0].severity == EventSeverity.INFO
    assert events[0].object_name == "BOOT"
    assert events[0].object_id == 63
    assert events[0].event_id == 0
    assert events[0].event_name == "VERSION"


def test_filter_by_severity():
    events = load_events(LOG_FILE)
    log = EventLog(events)

    assert len(log.filter_by_severity(EventSeverity.INFO)) == 280
    assert len(log.filter_by_severity(EventSeverity.WARNING)) == 54
    assert len(log.filter_by_severity(EventSeverity.ERROR)) == 6


def test_count_by_object():
    events = load_events(LOG_FILE)
    log = EventLog(events)

    counts = log.count_by_object()

    assert counts["BOOT"] == 17
    assert counts["OSPERF"] == 7
    assert counts["RADIO_APP"] == 55
    assert counts["SERVICE"] == 70
    assert sum(counts.values()) == 280


def test_error_rate():
    events = load_events(LOG_FILE)
    log = EventLog(events)

    assert log.error_rate == 6 / 280


def test_empty_log_error_rate():
    log = EventLog([])

    assert log.error_rate == 0.0