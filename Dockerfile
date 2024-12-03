FROM python:3.10-slim

ENV PYTHONUNBUFFERED=True

WORKDIR /app
RUN mkdir /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN chmod -R 777 /app
EXPOSE 8002
HEALTHCHECK CMD curl --fail http://localhost:8002/_stcore/health
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8002","-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--timeout" ,"0"]
