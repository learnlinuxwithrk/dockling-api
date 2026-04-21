FROM python:3.10

WORKDIR /app

# 🔥 System dependencies (IMPORTANT for Docling + OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip install --no-cache-dir \
    docling \
    fastapi \
    uvicorn \
    python-multipart \
    pillow \
    opencv-python-headless

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]