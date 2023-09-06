FROM python:3.10.13-slim-bullseye

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY ticket_control ticket_control
COPY app.py app.py

COPY data data
COPY model.pkl model.pkl

# COPY bvg-controller-a5a989d34b1d.json bvg-controller-a5a989d34b1d.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=bvg-controller-a5a989d34b1d.json
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
