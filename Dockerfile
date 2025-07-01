FROM python:3.11-slim

# --- system deps ---

    
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        poppler-utils tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng \
        && rm -rf /var/lib/apt/lists/*

# --- python deps ---
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- app code ---
COPY app/ ./app
ENV PYTHONPATH=/code
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
