FROM prefecthq/prefect:2.11.5-python3.10

COPY requirements.txt /opt/prefect/ticket-control-bvg/requirements.txt
RUN python -m pip install -r /opt/prefect/ticket-control-bvg/requirements.txt
COPY . /opt/prefect/ticket-control-bvg/

# Set up credentials (replace with your own service account key if needed)
# COPY bvg-controller-a5a989d34b1d.json /opt/prefect/ticket-control-bvg/bvg-controller-a5a989d34b1d.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/opt/prefect/ticket-control-bvg/bvg-controller-a5a989d34b1d.json
#ENV GOOGLE_APPLICATION_CREDENTIALS=/opt/prefect/ticket-control-bvg/bvg-controller-a5a989d34b1d.json
CMD [ "prefect cloud login -k pnu_7JaOtTvlACdiFwtGVcN7grGPAUeCeR3i5DVg" ]
WORKDIR /opt/prefect/ticket-control-bvg/