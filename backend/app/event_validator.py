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
        {"date": "", "name": "Presentación del curso"},
        {"date": "", "name": "Objetivos de aprendizaje"},
        {"date": "", "name": "Introducción"},
        {"date": "", "name": "Fundamentos"},
        {"date": "", "name": "Pruebas dentro el ciclo de desarrollo de software"},
        {"date": "", "name": "Técnicas de Pruebas"},
        {"date": "", "name": "Planificación, Diseño y Seguimiento de Plan de Pruebas"},
        {"date": "2023-09-08T20:30:00.000Z", "name": "Interrogaciones"},
        {"date": "2023-09-08T20:30:00.000Z", "name": "Actividades"},
        {"date": "2023-09-22T20:30:00.000Z", "name": "Interrogación 1"},
        {"date": "2023-10-25T20:30:00.000Z", "name": "Interrogación 2"},
        {"date": "2023-12-04T20:30:00.000Z", "name": "Recuperativo"},
    ]

    valid_events = [event for event in events if is_event_valid(event)]
    print(valid_events)
