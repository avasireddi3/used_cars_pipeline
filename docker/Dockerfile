FROM apache/airflow:2.10.4
USER root
RUN apt-get update \
    && apt-get install libpq-dev python3-dev -y --no-install-recommends
USER airflow
COPY ../requirements.txt .
RUN pip install -r requirements.txt