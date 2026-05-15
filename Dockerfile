FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install \
    --default-timeout=1000 \
    --retries=10 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]