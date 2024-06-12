FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

RUN apt-get update && apt-get install -y tzdata
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo "Asia/Seoul" > /etc/timezone

COPY requirements.txt /app/
RUN pip install --cache-dir --upgrade -r requirements.txt

COPY ./app .
WORKDIR /

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]