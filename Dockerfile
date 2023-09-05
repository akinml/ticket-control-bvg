FROM prefecthq/prefect:2.11.5-python3.10
COPY requirements.txt /opt/prefect/ticket-control-bvg/requirements.txt
RUN python -m pip install -r /opt/prefect/ticket-control-bvg/requirements.txt
COPY . /opt/prefect/ticket-control-bvg/
WORKDIR /opt/prefect/ticket-control-bvg/