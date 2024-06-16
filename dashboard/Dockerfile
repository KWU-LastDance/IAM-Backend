FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r dashboard/requirements.txt

ENV PATH="${PATH}:/root/.local/bin"

EXPOSE 8501

WORKDIR /app/dashboard

CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.enableCORS=false", \
    "--server.address=0.0.0.0", \
    "server.enableXsrfProtection=false"]
