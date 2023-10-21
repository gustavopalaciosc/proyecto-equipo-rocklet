from typing import List
from ics import Calendar, Event
import datetime


def create_ics_file(event_list: List[Event], output_filename: str):
    # Create a new calendar
    c = Calendar()

    for event in event_list:
        calendar_event = Event()
        calendar_event.name = event.name

        # Parse the date from the input string
        event_date = datetime.datetime.strptime(event.date, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Set the event to last all day
        calendar_event.begin = event_date.date()
        calendar_event.make_all_day()

        c.events.add(calendar_event)

    # Save the calendar to a file
    with open(output_filename, "w") as f:
        f.writelines(c)


if __name__ == "__main__":
    print("AAAAAAAAA")
    event_list = [
        {"name": "DEBUG Tarea 4", "date": "2023-10-19T23:59:00.000Z"},
        {"name": "DEBUG Tarea 4", "date": "2023-10-26T23:59:00.000Z"},
        {"name": "DEBUG Tarea 5", "date": "2023-11-23T23:59:00.000Z"},
    ]

    output_filename = "events.ics"
    create_ics_file(event_list, output_filename)
    print(f"ICS file '{output_filename}' has been created.")
