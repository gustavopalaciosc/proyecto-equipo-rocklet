from datetime import datetime
import dateutil.parser


def is_event_valid(event):
    try:
        _ = event["name"]
        date = event["date"]
        dateutil.parser.isoparse(date)
    except:
        return False
    return True


if __name__ == "__main__":
    # Example usage:
    events = [
        {"date": "2023-08-09", "name": "Clases"},
        {"date": "2023-08-09", "name": "Objetivos"},
        {"date": "2023-08-09", "name": "Contenidos"},
        {"date": "2023-08-24T23:59:00.000Z", "name": "Tarea 1"},
        {"date": "2023-09-07T23:59:00.000Z", "name": "Tarea 2"},
        {"date": "2023-10-19T23:59:00.000Z", "name": "Tarea 4"},
        {"date": "2023-10-26T23:59:00.000Z", "name": "Tarea 4"},
        {"date": "2023-11-23T23:59:00.000Z", "name": "Tarea 5"},
        {"date": "2023-11-30T23:59:00.000Z", "name": "Tarea 6"},
        {"date": "2023-09-20T12:00:00.000Z", "name": "Interrogación 1"},
        {"date": "2023-11-06T12:00:00.000Z", "name": "Interrogación 2"},
        {"date": "2023-12-13T12:00:00.000Z", "name": "Examen"},
    ]

    for event in events:
        print(is_event_valid(event))
