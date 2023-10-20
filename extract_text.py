from pypdf import PdfReader

reader = PdfReader("sample.pdf")


def visitor_body(text):
    print(text)


for page in reader.pages:
    text = page.extract_text()
    print(text)
