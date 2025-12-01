FROM apache/airflow:2.9.1

USER root
RUN pip install apache-airflow-providers-amazon apache-airflow-providers-snowflake snowflake-connector-python
USER airflow

COPY dags /opt/airflow/dags
