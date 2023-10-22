from typing import List
from pydantic import BaseModel
from pypdf import PdfReader
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.ia_dates import get_events, get_course_name
from app.events_to_calendar import create_ics_file
import uuid

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "Hello from PDF event dates parser!"}


@app.get("/events")
def dates_example():
    """
    Harcoded events endpoint useful for debugging in front
    """
    return [
        {"id": 0, "name": "Clases", "date": "2023-08-09T00:00:00.000Z"},
        {"id": 1, "name": "Ayudantias", "date": "2023-08-11T00:00:00.000Z"},
        {"id": 2, "name": "Tarea 1", "date": "2023-08-24T23:59:00.000Z"},
        {"id": 3, "name": "Tarea 2", "date": "2023-09-07T23:59:00.000Z"},
        {"id": 4, "name": "Tarea 4", "date": "2023-10-19T23:59:00.000Z"},
        {"id": 5, "name": "Tarea 4", "date": "2023-10-26T23:59:00.000Z"},
        {"id": 6, "name": "Tarea 5", "date": "2023-11-23T23:59:00.000Z"},
        {"id": 7, "name": "Tarea 6", "date": "2023-11-30T23:59:00.000Z"},
        {"id": 8, "name": "Interrogación 1", "date": "2023-09-20T05:00:00.000Z"},
        {"id": 9, "name": "Interrogación 2", "date": "2023-11-06T05:00:00.000Z"},
        {"id": 10, "name": "Examen", "date": "2023-12-13T05:00:00.000Z"},
    ]


class Event(BaseModel):
    name: str
    date: str


@app.post("/calendar")
async def create_calendar(events: List[Event]):
    """
    Receive a list of events and creates the .ics calendar file, returns the link to the file
    """
    print(events)
    id = uuid.uuid4()
    path = f"./static/{id}.ics"
    create_ics_file(events, path)

    file_uri = f"http://localhost:8000/static/{id}.ics"
    return {"link": file_uri}


@app.post("/ai/pdf_events")
def create_upload_file(file: UploadFile):
    """
    Get file upload and return events with name and dates as response
    """
    reader = PdfReader(file.file)

    course_name = get_course_name(reader.pages[0].extract_text())[0]

    total_text = ""
    for page in reader.pages:
        text = page.extract_text()
        total_text += text + "\n"

    events = get_events(total_text)

    for i, event in enumerate(events):
        event["id"] = i
        event["name"] += f" {course_name}"

    return events
