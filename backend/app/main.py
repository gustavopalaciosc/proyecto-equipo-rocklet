from typing import Union

from pypdf import PdfReader
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


import os


@app.post("/get_dates/")
def create_upload_file(file: UploadFile):
    reader = PdfReader(file.file)
    for page in reader.pages:
        text = page.extract_text()
        print(text)
    # with open("sample.pdf", "rb") as temp_file:

    # content = file.file.readlines()
    # print(content)
    return {"filename": file.filename}
