# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg libsndfile1 build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PyTorch (CPU-only) first to leverage caching
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy and install core Python dependencies (excluding tortoise-tts)
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn python-multipart numpy scipy ffmpeg-python pydub soundfile transformers==4.31.0 tokenizers==0.13.3 sentencepiece

# Install tortoise-tts without dependency checks
RUN pip install --no-cache-dir --no-deps git+https://github.com/neonbjb/tortoise-tts.git

# Manually install tortoise-tts dependencies to avoid version conflicts
RUN pip install --no-cache-dir einops inflect librosa progressbar rotary-embedding-torch unidecode

# Copy application source code
COPY . .

# Optionally expose the API port
EXPOSE 8000

# Clean up pip cache to reduce image size
RUN apt-get autoremove -y && apt-get clean && rm -rf /root/.cache

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
