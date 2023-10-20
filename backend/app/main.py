from typing import Union

from pypdf import PdfReader
from fastapi import FastAPI, File, UploadFile
from app.ia_dates import get_dates

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/get_dates/")
def create_upload_file(file: UploadFile):
    reader = PdfReader(file.file)

    total_text = ""
    for page in reader.pages:
        text = page.extract_text()
        total_text += text + "\n"

    dates = get_dates(total_text)

    return dates
