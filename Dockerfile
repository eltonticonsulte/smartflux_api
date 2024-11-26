FROM python

ENV PYTHONUNBUFFERED=True

WORKDIR /home/app/
RUN mkdir /home/app/log

RUN mkdir /home/app/anomaly
RUN mkdir /home/app/prod
RUN mkdir /home/app/release

COPY api ./api
COPY core core
COPY services services
COPY main.py ./
COPY .cz.toml ./.cz.toml
COPY utils ./utils
COPY config_log.py /home/app/

RUN mkdir /home/app/img
RUN mkdir /home/app/backup
RUN chmod -R 777 /home/app
EXPOSE 8002
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8002","-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--timeout" ,"0"]
