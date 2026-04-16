FROM python:3.12-slim

RUN pip install --no-cache-dir pysam==0.23.3 coverage>=7.0

COPY pysam_harness.py /opt/pysam_harness.py

ENTRYPOINT ["python", "/opt/pysam_harness.py"]
