FROM python:3.10.13-slim

WORKDIR /app

RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
    libgomp1 \
    git \
    ffmpeg \
    gcc \
    g++ \
    build-essential \
    libsndfile1

# First install some core dependencies to avoid the PyStemmer issue
RUN pip install --upgrade pip && \
    pip install wheel setuptools cython

# Try with the --no-deps flag and then install dependencies separately
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install git+https://github.com/bolna-ai/bolna@master --no-deps && \
    pip install numpy==1.26.4 pandas scikit-learn aiohttp fastapi==0.108.0 uvicorn==0.22.0 redis==5.0.1 \
    requests==2.31.0 openai>=1.10.0 python-dotenv==1.0.0 aiofiles==23.2.1 \
    torch torchaudio==2.6.0 aiobotocore==2.9.0 azure-cognitiveservices-speech==1.38.0 \
    daily-python==0.9.1 fastembed==0.6.1 huggingface-hub==0.24.3 litellm==1.40.20 \
    llama_index==0.10.65 llama-index-vector-stores-lancedb==0.1.7 plivo==4.47.0 \
    pydantic==2.5.3 pydub==0.25.1 pymongo==4.8.0 python-dateutil==2.8.2 tiktoken>=0.6.0 \
    twilio==8.9.0 websockets==15.0.1 onnxruntime>=1.16.3 semantic-router==0.0.46 \
    sentence-transformers==3.0.1 uvloop==0.19.0 tokenizers==0.15.2 lancedb==0.12.0

COPY quickstart_server.py /app/
COPY presets /app/presets
COPY .env /app/

EXPOSE 5001

CMD ["uvicorn", "quickstart_server:app", "--host", "0.0.0.0", "--port", "5001"]