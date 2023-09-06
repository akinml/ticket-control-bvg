FROM python:3.10.13-slim-bullseye

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY ticket_control ticket_control
COPY app.py app.py
COPY pipeline.py pipeline.py

CMD uvicorn app:app --host 0.0.0.0
