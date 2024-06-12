FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

COPY requirements.txt /app/
RUN pip install --cache-dir --upgrade -r requirements.txt

COPY ./app .
WORKDIR /

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]