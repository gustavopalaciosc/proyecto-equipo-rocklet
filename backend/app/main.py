from typing import Union

from pypdf import PdfReader
from fastapi import FastAPI, File, UploadFile
from app.ia_dates import get_events

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from PDF event dates parser!"}


@app.post("/get_dates/")
def create_upload_file(file: UploadFile):
    reader = PdfReader(file.file)

    total_text = ""
    for page in reader.pages:
        text = page.extract_text()
        total_text += text + "\n"

    dates = get_events(total_text)

    return dates
