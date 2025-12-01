FROM bitnami/spark:3.5.1

USER root
RUN pip install boto3
USER 1001

WORKDIR /opt/bitnami/spark/app

COPY job ./job

CMD ["/opt/bitnami/spark/bin/spark-submit", "job/streaming_job.py"]
