from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import uuid, tempfile, os
from app.extractor import extract_text

app = FastAPI(title="PDF-to-Text API")

@app.post("/extract", response_class=PlainTextResponse)
async def extract(file: UploadFile = File(...)):
    # sanity check
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "File must be a PDF")

    # persist to tmp and run extractor
    tmp_name = f"/tmp/{uuid.uuid4()}.pdf"
    with open(tmp_name, "wb") as tmp:
        tmp.write(await file.read())

    try:
        text = extract_text(tmp_name)
        return text
    finally:
        os.remove(tmp_name)
