FROM python:3.8.12-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY taxifare taxifare
# COPY setup.py setup.py
# RUN pip install .

#COPY Makefile Makefile
#RUN make reset_local_files

#CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT