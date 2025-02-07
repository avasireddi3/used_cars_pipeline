FROM postgres:13
COPY init.sql docker-entrypoint-initdb.d/
ENV POSTGRES_USER=airflow
ENV POSTGRES_DB=airflow
ENV POSTGRES_PASSWORD=airflow
