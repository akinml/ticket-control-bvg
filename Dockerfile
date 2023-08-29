FROM python:3.10.6-buster
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn ticket-control-bvg.api.fast:app --host 0.0.0.0
CMD streamlit run /app/webapp/app.py