FROM python:3.10-slim

ENV PYTHONUNBUFFERED=True

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY alembic.ini alembic.ini
COPY utils utils
COPY alembic alembic
COPY core core
COPY src src
COPY main.py main.py
RUN chmod -R 777 /app
EXPOSE 8002
HEALTHCHECK CMD curl --fail http://localhost:8002/_stcore/health

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8002"]
#CMD ["uvicorn", "main:app", "-b", "0.0.0.0:8002","-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--timeout" ,"10"]
